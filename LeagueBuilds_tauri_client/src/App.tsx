import {
  CSSProperties,
  FormEvent,
  Fragment,
  ReactNode,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState
} from "react";
import { getVersion as getTauriClientVersion } from "@tauri-apps/api/app";
import { invoke } from "@tauri-apps/api/core";
import {
  fetchBuild,
  fetchServerVersion,
  enrichBuildWithMetadata,
  fetchDataDragonVersion,
  startLcuBridge,
  updateLcuBridgeSettings,
  getLcuBridgeLastApplied,
  getLcuCurrentSummonerName,
  retriggerLcuImport,
  retriggerLcuImportForChampion
} from "./api";
import { defaultSettings, loadSettings, saveSettings } from "./config";
import type { RichBuild } from "./types";

const positions = ["", "top", "jungle", "middle", "bottom", "utility"];
const LATEST_RELEASE_URL = "https://github.com/CookieDecide/LeagueBuilds/releases/latest";
const FALLBACK_CLIENT_VERSION = "0.7.7";
const INCOGNITO_TOGGLE_KEY = "F10";

function parseVersionParts(version: string): [number, number, number] | null {
  const normalized = version.trim().replace(/^v/i, "");
  const match = normalized.match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!match) {
    return null;
  }

  return [Number(match[1]), Number(match[2]), Number(match[3])];
}

function compareSemver(a: string, b: string): number {
  const left = parseVersionParts(a);
  const right = parseVersionParts(b);

  if (!left || !right) {
    return 0;
  }

  for (let i = 0; i < 3; i += 1) {
    if (left[i] > right[i]) {
      return 1;
    }
    if (left[i] < right[i]) {
      return -1;
    }
  }

  return 0;
}

const statShardMeta: Record<number, { icon: string; label: string }> = {
  5008: { icon: "perk-images/StatMods/StatModsAdaptiveForceScalingIcon.png", label: "Adaptive Force" },
  5002: { icon: "perk-images/StatMods/StatModsArmorIcon.png", label: "Armor" },
  5003: { icon: "perk-images/StatMods/StatModsMagicResIcon.png", label: "Magic Resist" },
  5005: { icon: "perk-images/StatMods/StatModsAttackSpeedIcon.png", label: "Attack Speed" },
  5007: { icon: "perk-images/StatMods/StatModsCDRScalingIcon.png", label: "Scaling CDR" },
  5001: { icon: "perk-images/StatMods/StatModsHealthPlusIcon.png", label: "Health" },
  5011: { icon: "perk-images/StatMods/StatModsHealthScalingIcon.png", label: "Health Scaling" },
  5010: { icon: "perk-images/StatMods/StatModsMovementSpeedIcon.png", label: "Move Speed" },
  5013: { icon: "perk-images/StatMods/StatModsTenacityIcon.png", label: "Tenacity" },
  1: { icon: "perk-images/StatMods/StatModsAdaptiveForceScalingIcon.png", label: "Adaptive Force" }
};
function getChampionSplashUrl(championId: string): string {
  return `https://ddragon.leagueoflegends.com/cdn/img/champion/loading/${championId}_0.jpg`;
}

function extractImageFull(image: unknown): string | undefined {
  if (!image) {
    return undefined;
  }

  if (typeof image === "string") {
    const trimmed = image.trim();
    try {
      const parsed = JSON.parse(trimmed.replace(/'/g, '"')) as { full?: string };
      if (parsed && typeof parsed.full === "string") {
        return parsed.full;
      }
    } catch {
      const fullMatch = trimmed.match(/'full':\s*'([^']+)'/);
      if (fullMatch?.[1]) {
        return fullMatch[1];
      }
      if (trimmed.endsWith(".png") || trimmed.endsWith(".jpg")) {
        return trimmed;
      }
    }

    return undefined;
  }

  if (typeof image === "object") {
    const record = image as { full?: unknown };
    return typeof record.full === "string" ? record.full : undefined;
  }

  return undefined;
}

function getSummonerSpellUrl(image: unknown, version: string): string {
  const full = extractImageFull(image);
  if (!full) return "";
  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/spell/${full}`;
}

function getItemImageUrl(image: unknown, itemId: number | string, version: string): string {
  const full = extractImageFull(image);
  if (full) {
    return `https://ddragon.leagueoflegends.com/cdn/${version}/img/item/${full}`;
  }

  return `https://ddragon.leagueoflegends.com/cdn/${version}/img/item/${itemId}.png`;
}

function getRuneIconUrl(iconPath: string | undefined): string {
  if (!iconPath) return "";
  return `https://ddragon.leagueoflegends.com/cdn/img/${iconPath}`;
}

function getRuneStyleIconUrl(icon: string | undefined): string {
  if (!icon) return "";
  return `https://ddragon.leagueoflegends.com/cdn/img/${icon}`;
}

function stripHtml(value: string | undefined): string {
  if (!value) return "";
  return value.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function formatPercent(value: string): string {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return "-";
  }

  const normalized = parsed <= 1 ? parsed * 100 : parsed;
  return `${normalized.toFixed(2)}%`;
}

function orderSummonersByFlashPreference(
  summoners: number[],
  flashPosition: "d" | "f"
): Array<{ spellId: number; slot: "D" | "F" | null }> {
  if (summoners.length === 0) {
    return [];
  }

  const flashId = 4;
  let spell1Id = summoners[0];
  let spell2Id = summoners[1] ?? summoners[0];

  if (summoners.includes(flashId)) {
    const otherSpell = summoners.find((spellId) => spellId !== flashId) ?? spell2Id;
    if (flashPosition === "d") {
      spell1Id = flashId;
      spell2Id = otherSpell;
    } else {
      spell1Id = otherSpell;
      spell2Id = flashId;
    }
  }

  return [
    { spellId: spell1Id, slot: "D" },
    { spellId: spell2Id, slot: "F" }
  ];
}

function mixChannel(start: number, end: number, amount: number): number {
  return Math.round(start + (end - start) * amount);
}

function mixHexColor(start: string, end: string, amount: number): string {
  const startValue = start.replace("#", "");
  const endValue = end.replace("#", "");
  const startRed = Number.parseInt(startValue.slice(0, 2), 16);
  const startGreen = Number.parseInt(startValue.slice(2, 4), 16);
  const startBlue = Number.parseInt(startValue.slice(4, 6), 16);
  const endRed = Number.parseInt(endValue.slice(0, 2), 16);
  const endGreen = Number.parseInt(endValue.slice(2, 4), 16);
  const endBlue = Number.parseInt(endValue.slice(4, 6), 16);

  const red = mixChannel(startRed, endRed, amount);
  const green = mixChannel(startGreen, endGreen, amount);
  const blue = mixChannel(startBlue, endBlue, amount);

  return `rgb(${red}, ${green}, ${blue})`;
}

function getWinrateColor(value: string): string {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return "var(--ink-soft)";
  }

  const normalized = parsed <= 1 ? parsed * 100 : parsed;

  if (normalized >= 50) {
    const amount = Math.min((normalized - 50) / 10, 1);
    return mixHexColor("#ffffff", "#4fe39b", amount);
  }

  if (normalized >= 40) {
    const amount = (normalized - 40) / 10;
    return mixHexColor("#ff7a7a", "#ffd66b", amount);
  }

  return "#ff7a7a";
}

function getSpellVideoUrl(championId: string, spellKey: string): string {
  const cleanedChampionId = championId.replace(/\D/g, "").padStart(4, "0");
  const normalizedKey = spellKey.toLowerCase();
  const suffixMap: Record<string, string> = {
    passive: "P1",
    q: "Q1",
    w: "W1",
    e: "E1",
    r: "R1"
  };
  const suffix = suffixMap[normalizedKey] ?? "Q1";
  return `https://d28xe8vt774jo5.cloudfront.net/champion-abilities/${cleanedChampionId}/ability_${cleanedChampionId}_${suffix}.webm`;
}

function normalizeChampionToken(value: string): string {
  return value.trim().toLowerCase().replace(/[^a-z0-9]/g, "");
}

type TooltipTileProps = {
  title: string;
  description?: string;
  htmlDescription?: string;
  videoUrl?: string;
  className?: string;
  placement?: "auto" | "top" | "bottom";
  children: ReactNode;
};

function TooltipTile({
  title,
  description,
  htmlDescription,
  videoUrl,
  className = "",
  placement = "auto",
  children
}: TooltipTileProps) {
  const tileRef = useRef<HTMLDivElement | null>(null);
  const panelRef = useRef<HTMLDivElement | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [panelStyle, setPanelStyle] = useState<CSSProperties>({});

  const updatePanelPosition = useCallback(() => {
    const tileElement = tileRef.current;
    const panelElement = panelRef.current;

    if (!tileElement || !panelElement || typeof window === "undefined") {
      return;
    }

    const margin = 8;
    const gap = 8;
    const tileRect = tileElement.getBoundingClientRect();
    const panelRect = panelElement.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    const minLeft = margin - tileRect.left;
    const maxLeft = viewportWidth - margin - tileRect.left - panelRect.width;
    const minTop = margin - tileRect.top;
    const maxTop = viewportHeight - margin - tileRect.top - panelRect.height;

    let left = tileRect.width / 2 - panelRect.width / 2;
    left = Math.min(Math.max(left, minLeft), maxLeft);

    const openAbove = placement === "top" || (placement === "auto" && tileRect.top >= panelRect.height + gap + margin);
    let top = openAbove ? -panelRect.height - gap : tileRect.height + gap;

    if (placement === "top" && tileRect.top + top < margin) {
      top = tileRect.height + gap;
    }

    if (placement === "bottom" && tileRect.bottom + panelRect.height + gap > viewportHeight - margin) {
      top = -panelRect.height - gap;
    }
    top = Math.min(Math.max(top, minTop), maxTop);

    setPanelStyle({
      left,
      top,
      maxWidth: `min(260px, calc(100vw - ${margin * 2}px))`,
      maxHeight: `calc(100vh - ${margin * 2}px)`
    });
  }, []);

  useLayoutEffect(() => {
    if (!isOpen) {
      return;
    }

    updatePanelPosition();

    const handleViewportChange = () => {
      updatePanelPosition();
    };

    const resizeObserver =
      typeof ResizeObserver === "undefined" || !panelRef.current
        ? null
        : new ResizeObserver(() => {
            updatePanelPosition();
          });

    if (resizeObserver && panelRef.current) {
      resizeObserver.observe(panelRef.current);
    }

    window.addEventListener("resize", handleViewportChange);
    window.addEventListener("scroll", handleViewportChange, true);

    return () => {
      resizeObserver?.disconnect();
      window.removeEventListener("resize", handleViewportChange);
      window.removeEventListener("scroll", handleViewportChange, true);
    };
  }, [isOpen, title, description, htmlDescription, videoUrl, updatePanelPosition]);

  return (
    <div
      ref={tileRef}
      className={`tooltip-tile ${className}`.trim()}
      tabIndex={0}
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
      onFocus={() => setIsOpen(true)}
      onBlur={() => setIsOpen(false)}
    >
      {children}
      <div
        ref={panelRef}
        className={`tooltip-panel ${isOpen ? "is-open" : ""}`.trim()}
        style={panelStyle}
      >
        <strong>{title}</strong>
        {htmlDescription ? (
          <p dangerouslySetInnerHTML={{ __html: htmlDescription }} />
        ) : description ? (
          <p>{description}</p>
        ) : null}
        {videoUrl ? (
          <video
            className="tooltip-video"
            src={videoUrl}
            autoPlay
            muted
            loop
            playsInline
            preload="none"
          />
        ) : null}
      </div>
    </div>
  );
}

export default function App() {
  const initialSettings = useMemo(() => loadSettings(), []);
  const [serverIp, setServerIp] = useState(initialSettings.serverIp);
  const [summonerName, setSummonerName] = useState(defaultSettings.summonerName);
  const [importRunes, setImportRunes] = useState(initialSettings.importRunes);
  const [importItems, setImportItems] = useState(initialSettings.importItems);
  const [importSummoners, setImportSummoners] = useState(initialSettings.importSummoners);
  const [flashPosition, setFlashPosition] = useState<"d" | "f">(initialSettings.flashPosition);
  const [runeOptionIndex, setRuneOptionIndex] = useState(initialSettings.runeOptionIndex);
  const [championId, setChampionId] = useState("22");
  const [position, setPosition] = useState("");
  const [build, setBuild] = useState<RichBuild | null>(null);
  const [dataDragonVersion, setDataDragonVersion] = useState("16.7.1");
  const [clientVersion, setClientVersion] = useState<string>(FALLBACK_CLIENT_VERSION);
  const [version, setVersion] = useState<string>("-");
  const [updateNotice, setUpdateNotice] = useState<string>("");
  const [loadingBuild, setLoadingBuild] = useState(false);
  const [loadingVersion, setLoadingVersion] = useState(false);
  const [loadingRetriggerImport, setLoadingRetriggerImport] = useState(false);
  const [loadingSyncRefresh, setLoadingSyncRefresh] = useState(false);
  const [incognitoOverride, setIncognitoOverride] = useState(initialSettings.incognitoOverride);
  const [championLookup, setChampionLookup] = useState<Record<string, string>>({});
  const [championIdToName, setChampionIdToName] = useState<Record<string, string>>({});
  const [championEntries, setChampionEntries] = useState<Array<{ id: string; name: string }>>([]);
  const [championNames, setChampionNames] = useState<string[]>([]);
  const [error, setError] = useState<string>("");
  const lastBridgeAppliedKeyRef = useRef<string>("");
  const hasAutoFilledSummonerRef = useRef(false);
  const hasOpenedReleasePageRef = useRef(false);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const isToggleKey = event.code === INCOGNITO_TOGGLE_KEY || event.key === INCOGNITO_TOGGLE_KEY;
      if (!isToggleKey || event.repeat) {
        return;
      }

      event.preventDefault();
      event.stopPropagation();
      setIncognitoOverride((previous) => !previous);
    };

    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
    };
  }, []);

  useEffect(() => {
    if (incognitoOverride) {
      hasAutoFilledSummonerRef.current = true;
      setSummonerName(defaultSettings.summonerName);
      return;
    }

    hasAutoFilledSummonerRef.current = false;
  }, [incognitoOverride]);

  const checkClientOutdated = useCallback((serverVersionRaw: string) => {
    if (!clientVersion || clientVersion === "-" || !serverVersionRaw || serverVersionRaw === "-") {
      return;
    }

    if (compareSemver(clientVersion, serverVersionRaw) < 0) {
      setUpdateNotice(`Client ${clientVersion} is older than server ${serverVersionRaw}. Opening latest release page.`);

      if (!hasOpenedReleasePageRef.current) {
        hasOpenedReleasePageRef.current = true;
        window.open(LATEST_RELEASE_URL, "_blank", "noopener,noreferrer");
      }
    } else {
      setUpdateNotice("");
    }
  }, [clientVersion]);

  useEffect(() => {
    let cancelled = false;

    const loadClientVersion = async () => {
      try {
        const currentVersion = await getTauriClientVersion();
        if (!cancelled) {
          setClientVersion(currentVersion?.trim() || FALLBACK_CLIENT_VERSION);
        }
      } catch {
        if (!cancelled) {
          setClientVersion(FALLBACK_CLIENT_VERSION);
        }
      }
    };

    void loadClientVersion();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    const loadChampionLookup = async () => {
      try {
        const response = await fetch(
          `https://ddragon.leagueoflegends.com/cdn/${dataDragonVersion}/data/en_US/champion.json`
        );

        if (!response.ok) {
          return;
        }

        const payload = (await response.json()) as {
          data?: Record<string, { id: string; key: string; name: string }>;
        };

        const nextLookup: Record<string, string> = {};
        const nextIdToName: Record<string, string> = {};
        const nextEntries: Array<{ id: string; name: string }> = [];
        const nextNames: string[] = [];

        for (const champion of Object.values(payload.data ?? {})) {
          const championKey = champion.key?.trim();
          const championName = champion.name?.trim();
          if (!championKey) {
            continue;
          }

          nextLookup[normalizeChampionToken(champion.id)] = championKey;
          if (championName) {
            nextLookup[normalizeChampionToken(championName)] = championKey;
            nextNames.push(championName);
            nextEntries.push({ id: championKey, name: championName });
          }
          nextIdToName[championKey] = championName || champion.id;
        }

        if (!cancelled) {
          setChampionLookup(nextLookup);
          setChampionIdToName(nextIdToName);
          setChampionEntries(nextEntries);
          setChampionNames(nextNames.sort((a, b) => a.localeCompare(b)));
        }
      } catch {
        if (!cancelled) {
          setChampionLookup({});
          setChampionIdToName({});
          setChampionEntries([]);
          setChampionNames([]);
        }
      }
    };

    void loadChampionLookup();

    return () => {
      cancelled = true;
    };
  }, [dataDragonVersion]);

  const resolveChampionId = useCallback((input: string): string | null => {
    const trimmed = input.trim();
    if (!trimmed) {
      return null;
    }

    if (/^\d+$/.test(trimmed)) {
      return trimmed;
    }

    const resolvedId = championLookup[normalizeChampionToken(trimmed)];
    return resolvedId || null;
  }, [championLookup]);

  const championSuggestions = useMemo(() => {
    if (championNames.length === 0) {
      return [];
    }

    const trimmedQuery = championId.trim();
    const query = normalizeChampionToken(trimmedQuery);
    if (!query) {
      return championNames.slice(0, 20).map((name) => ({ value: name, label: name }));
    }

    if (/^\d+$/.test(trimmedQuery)) {
      return championEntries
        .filter((entry) => entry.id.startsWith(trimmedQuery))
        .sort((left, right) => {
          if (left.id.length !== right.id.length) {
            return left.id.length - right.id.length;
          }

          const leftNumeric = Number(left.id);
          const rightNumeric = Number(right.id);
          if (!Number.isNaN(leftNumeric) && !Number.isNaN(rightNumeric) && leftNumeric !== rightNumeric) {
            return leftNumeric - rightNumeric;
          }

          return left.name.localeCompare(right.name);
        })
        .map((entry) => ({ value: entry.id, label: entry.name }))
        .slice(0, 20);
    }

    return championNames
      .filter((name) => normalizeChampionToken(name).includes(query))
      .sort((left, right) => {
        const leftToken = normalizeChampionToken(left);
        const rightToken = normalizeChampionToken(right);
        const leftStarts = leftToken.startsWith(query);
        const rightStarts = rightToken.startsWith(query);

        if (leftStarts !== rightStarts) {
          return leftStarts ? -1 : 1;
        }

        return left.localeCompare(right);
      })
      .map((name) => ({ value: name, label: name }))
      .slice(0, 20);
  }, [championId, championEntries, championNames]);

  const onChampionInputChange = useCallback((nextValue: string) => {
    setChampionId(nextValue);
  }, []);

  const onChampionInputBlur = useCallback(() => {
    const trimmed = championId.trim();
    if (/^\d+$/.test(trimmed)) {
      const resolvedName = championIdToName[trimmed];
      if (resolvedName) {
        setChampionId(resolvedName);
      }
    }
  }, [championId, championIdToName]);

  useEffect(() => {
    let cancelled = false;

    const loadDataDragonVersion = async () => {
      try {
        const nextVersion = await fetchDataDragonVersion();
        if (!cancelled) {
          setDataDragonVersion(nextVersion);
        }
      } catch {
        if (!cancelled) {
          setDataDragonVersion("16.7.1");
        }
      } finally {
      }
    };

    void loadDataDragonVersion();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    const syncLoggedInSummoner = async () => {
      if (cancelled || hasAutoFilledSummonerRef.current || incognitoOverride) {
        return;
      }

      try {
        const loggedInSummonerName = await getLcuCurrentSummonerName();
        const trimmedName = loggedInSummonerName?.trim();

        if (!cancelled && trimmedName) {
          setSummonerName(trimmedName);
          hasAutoFilledSummonerRef.current = true;
        }
      } catch {
        // Keep retrying until the client is available.
      }
    };

    void syncLoggedInSummoner();
    const interval = window.setInterval(() => {
      void syncLoggedInSummoner();
    }, 5000);

    return () => {
      cancelled = true;
      window.clearInterval(interval);
    };
  }, [incognitoOverride]);

  useEffect(() => {
    const initializeLcuBridge = async () => {
      try {
        await startLcuBridge({
          serverIp: initialSettings.serverIp,
          summonerName: defaultSettings.summonerName,
          importRunes: initialSettings.importRunes,
          importItems: initialSettings.importItems,
          importSummoners: initialSettings.importSummoners,
          flashPosition: initialSettings.flashPosition,
          runeOptionIndex: initialSettings.runeOptionIndex
        });
      } catch (error) {
        console.error("Failed to start LCU bridge", error);
      }
    };

    void initializeLcuBridge();
  }, [
    initialSettings.serverIp,
    initialSettings.importRunes,
    initialSettings.importItems,
    initialSettings.importSummoners,
    initialSettings.flashPosition,
    initialSettings.runeOptionIndex
  ]);

  useEffect(() => {
    const handle = window.setTimeout(() => {
      void updateLcuBridgeSettings({
        serverIp: serverIp.trim() || defaultSettings.serverIp,
        summonerName: summonerName.trim() || defaultSettings.summonerName,
        importRunes,
        importItems,
        importSummoners,
        flashPosition,
        runeOptionIndex
      }).catch((error) => {
        console.error("Failed to update LCU bridge settings", error);
      });
    }, 250);

    return () => {
      window.clearTimeout(handle);
    };
  }, [serverIp, summonerName, importRunes, importItems, importSummoners, flashPosition, runeOptionIndex]);

  useEffect(() => {
    saveSettings({
      serverIp: serverIp.trim() || defaultSettings.serverIp,
      summonerName: defaultSettings.summonerName,
      importRunes,
      importItems,
      importSummoners,
      flashPosition,
      runeOptionIndex,
      incognitoOverride
    });
  }, [serverIp, importRunes, importItems, importSummoners, flashPosition, runeOptionIndex, incognitoOverride]);

  useEffect(() => {
    if (!build || build.runes.length === 0) {
      return;
    }

    if (runeOptionIndex >= build.runes.length) {
      setRuneOptionIndex(0);
    }
  }, [build, runeOptionIndex]);

  const syncFromBridge = useCallback(async (force = false) => {
    const lastApplied = await getLcuBridgeLastApplied();
    if (!lastApplied) {
      return;
    }

    const normalizedPosition = (lastApplied.position || "").toLowerCase();
    const appliedKey = [lastApplied.champion_id, normalizedPosition].join(":");
    if (!force && appliedKey === lastBridgeAppliedKeyRef.current) {
      return;
    }

    const previousAppliedKey = lastBridgeAppliedKeyRef.current;
    const isNewBuild = appliedKey !== previousAppliedKey;

    lastBridgeAppliedKeyRef.current = appliedKey;
    setChampionId(championIdToName[lastApplied.champion_id] || lastApplied.champion_id);
    setPosition(normalizedPosition);

    const loggedInSummonerName = await getLcuCurrentSummonerName().catch(() => null);
    const effectiveSummoner = incognitoOverride
      ? defaultSettings.summonerName
      : (loggedInSummonerName || summonerName || defaultSettings.summonerName).trim() || defaultSettings.summonerName;

    if (!incognitoOverride && effectiveSummoner !== summonerName) {
      setSummonerName(effectiveSummoner);
    }

    const effectiveServerIp = serverIp.trim() || defaultSettings.serverIp;

    const baseBuild = await fetchBuild({
      serverIp: effectiveServerIp,
      championId: lastApplied.champion_id,
      position: normalizedPosition,
      summonerName: effectiveSummoner
    });

    const richBuild = await enrichBuildWithMetadata(dataDragonVersion, baseBuild);
    setBuild(richBuild);
    if (isNewBuild) {
      setRuneOptionIndex(0);
    }
    setError("");
  }, [dataDragonVersion, serverIp, summonerName, incognitoOverride, championIdToName]);

  useEffect(() => {
    let cancelled = false;

    const runSync = async () => {
      try {
        await syncFromBridge(false);
      } catch (bridgeSyncError) {
        if (!cancelled) {
          console.error("Failed to sync build from LCU bridge", bridgeSyncError);
        }
      }
    };

    void runSync();
    const interval = window.setInterval(() => {
      void runSync();
    }, 2000);

    return () => {
      cancelled = true;
      window.clearInterval(interval);
    };
  }, [syncFromBridge]);

  useEffect(() => {
    let cancelled = false;

    const loadServerVersion = async () => {
      setLoadingVersion(true);

      try {
        const effectiveServerIp = serverIp.trim() || defaultSettings.serverIp;
        const result = await fetchServerVersion(effectiveServerIp);
        if (!cancelled) {
          setVersion(result);
          checkClientOutdated(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unable to fetch server version.");
        }
      } finally {
        if (!cancelled) {
          setLoadingVersion(false);
        }
      }
    };

    void loadServerVersion();

    return () => {
      cancelled = true;
    };
  }, [checkClientOutdated]);

  const persistSettings = (nextIp: string) => {
    saveSettings({
      serverIp: nextIp.trim() || defaultSettings.serverIp,
      summonerName: defaultSettings.summonerName,
      importRunes,
      importItems,
      importSummoners,
      flashPosition,
      runeOptionIndex,
      incognitoOverride
    });
  };

  const onCheckVersion = async () => {
    setError("");
    setLoadingVersion(true);

    try {
      const result = await fetchServerVersion(serverIp.trim());
      setVersion(result);
      checkClientOutdated(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to fetch server version.");
    } finally {
      setLoadingVersion(false);
    }
  };

  const onOpenLatestRelease = async (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();

    try {
      await invoke("open_external_url", { url: LATEST_RELEASE_URL });
    } catch {
      window.open(LATEST_RELEASE_URL, "_blank", "noopener,noreferrer");
    }
  };

  const onFetchBuild = async (event: FormEvent) => {
    event.preventDefault();
    setLoadingBuild(true);
    setError("");

    persistSettings(serverIp);

    try {
      const resolvedChampionId = resolveChampionId(championId);
      if (!resolvedChampionId) {
        throw new Error("Unknown champion. Enter a valid champion name or numeric champion ID.");
      }

      const baseBuild = await fetchBuild({
        serverIp: serverIp.trim(),
        championId: resolvedChampionId,
        position,
        summonerName: summonerName.trim() || "INCOGNITO"
      });
      const richBuild = await enrichBuildWithMetadata(dataDragonVersion, baseBuild);
      setBuild(richBuild);
      setRuneOptionIndex(0);
    } catch (err) {
      setBuild(null);
      setError(err instanceof Error ? err.message : "Unable to fetch build.");
    } finally {
      setLoadingBuild(false);
    }
  };

  const retriggerImportWithRuneOption = useCallback(async (
    nextRuneOptionIndex: number,
    nextFlashPosition: "d" | "f" = flashPosition
  ) => {
    const effectiveServerIp = serverIp.trim() || defaultSettings.serverIp;
    const effectiveSummoner = summonerName.trim() || defaultSettings.summonerName;

    try {
      await retriggerLcuImport({
        serverIp: effectiveServerIp,
        summonerName: effectiveSummoner,
        importRunes,
        importItems,
        importSummoners,
        flashPosition: nextFlashPosition,
        runeOptionIndex: nextRuneOptionIndex
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      const noChampionSelected = message.toLowerCase().includes("no selected champion");

      if (!noChampionSelected) {
        throw err;
      }

      const fallbackChampionInput = (build?.championId || championId || "").trim();
      const fallbackChampionId = resolveChampionId(fallbackChampionInput) || fallbackChampionInput;
      const fallbackPosition = (build?.position || position || "").trim();

      // Requested behavior: if no champ selected in League and no build selected in Tauri, do nothing.
      if (!build && !fallbackChampionId) {
        return;
      }

      if (!fallbackChampionId) {
        return;
      }

      await retriggerLcuImportForChampion({
        serverIp: effectiveServerIp,
        summonerName: effectiveSummoner,
        championId: fallbackChampionId,
        position: fallbackPosition,
        importRunes,
        importItems,
        importSummoners,
        flashPosition: nextFlashPosition,
        runeOptionIndex: nextRuneOptionIndex
      });
    }

    await syncFromBridge(true);
  }, [
    serverIp,
    summonerName,
    importRunes,
    importItems,
    importSummoners,
    flashPosition,
    build,
    championId,
    resolveChampionId,
    position,
    syncFromBridge
  ]);

  const onRetriggerImport = async () => {
    setError("");
    setLoadingRetriggerImport(true);

    try {
      await retriggerImportWithRuneOption(runeOptionIndex);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to retrigger import.");
    } finally {
      setLoadingRetriggerImport(false);
    }
  };

  const onSelectRuneOption = async (index: number) => {
    if (index === runeOptionIndex) {
      return;
    }

    setRuneOptionIndex(index);
    setError("");
    setLoadingRetriggerImport(true);

    try {
      await retriggerImportWithRuneOption(index);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to import selected rune option.");
    } finally {
      setLoadingRetriggerImport(false);
    }
  };

  const onFlashPositionChange = async (nextFlashPosition: "d" | "f") => {
    if (nextFlashPosition === flashPosition) {
      return;
    }

    setFlashPosition(nextFlashPosition);

    // Only auto-reimport on flash change when a build is currently loaded in the client UI.
    if (!build) {
      return;
    }

    setError("");
    setLoadingRetriggerImport(true);

    try {
      await retriggerImportWithRuneOption(runeOptionIndex, nextFlashPosition);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to reimport after flash key change.");
    } finally {
      setLoadingRetriggerImport(false);
    }
  };

  const onRetriggerSync = async () => {
    setError("");
    setLoadingSyncRefresh(true);

    try {
      await syncFromBridge(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to retrigger sync.");
    } finally {
      setLoadingSyncRefresh(false);
    }
  };

  const championAbilities = build?.championMeta
    ? [
        {
          key: "passive",
          label: "Passive",
          title: build.championMeta.spell_name_passive,
          image: build.championMeta.spell_image_passive,
          endpoint: "passive",
          description: build.championMeta.spell_text_passive
        },
        {
          key: "q",
          label: "Q",
          title: build.championMeta.spell_name_q,
          image: build.championMeta.spell_image_q,
          endpoint: "spell",
          description: build.championMeta.spell_text_q
        },
        {
          key: "w",
          label: "W",
          title: build.championMeta.spell_name_w,
          image: build.championMeta.spell_image_w,
          endpoint: "spell",
          description: build.championMeta.spell_text_w
        },
        {
          key: "e",
          label: "E",
          title: build.championMeta.spell_name_e,
          image: build.championMeta.spell_image_e,
          endpoint: "spell",
          description: build.championMeta.spell_text_e
        },
        {
          key: "r",
          label: "R",
          title: build.championMeta.spell_name_r,
          image: build.championMeta.spell_image_r,
          endpoint: "spell",
          description: build.championMeta.spell_text_r
        }
      ]
    : [];

  const displayedCoreItems = build ? build.items.slice(0, 6) : [];
  const hiddenCoreItemsCount = build ? Math.max(0, build.items.length - displayedCoreItems.length) : 0;
  const displayedStarterSets = build ? build.starterSets.slice(0, 2) : [];
  const hiddenStarterSetsCount = build ? Math.max(0, build.starterSets.length - displayedStarterSets.length) : 0;
  const displayedRuneLoadouts = build ? build.runes.slice(0, 3) : [];
  const hiddenRuneLoadoutsCount = build ? Math.max(0, build.runes.length - displayedRuneLoadouts.length) : 0;
  const displayedBuildPaths = build ? build.itemBuildPaths.slice(0, 3) : [];
  const hiddenBuildPathsCount = build ? Math.max(0, build.itemBuildPaths.length - displayedBuildPaths.length) : 0;
  const displayedSummoners = build
    ? orderSummonersByFlashPreference(build.summoners, flashPosition)
    : [];

  return (
    <main className="app-shell">
      <aside className="import-sidebar">
        <h2>Import Options</h2>
        <label>
          <input
            type="checkbox"
            checked={importRunes}
            onChange={(e) => setImportRunes(e.target.checked)}
          />
          Import Runes
        </label>
        <label>
          <input
            type="checkbox"
            checked={importItems}
            onChange={(e) => setImportItems(e.target.checked)}
          />
          Import Items
        </label>
        <label>
          <input
            type="checkbox"
            checked={importSummoners}
            onChange={(e) => setImportSummoners(e.target.checked)}
          />
          Import Summoners
        </label>
        <label>
          Flash Key
          <select
            value={flashPosition}
            onChange={(e) => {
              void onFlashPositionChange(e.target.value as "d" | "f");
            }}
            disabled={loadingRetriggerImport}
          >
            <option value="d">D</option>
            <option value="f">F</option>
          </select>
        </label>
      </aside>

      <div className="main-content">
        <section className="hero">
          <p className="eyebrow">LeagueBuilds Desktop</p>
          <h1>Build Optimizer</h1>
          <p className="lead">Find the perfect build for your League of Legends champion</p>
        </section>

        <section className="panel">
          <form className="lookup-form" onSubmit={onFetchBuild}>
          {incognitoOverride ? (
            <>
              <label>
                Server URL
                <div className="input-with-inline-action">
                  <input
                    value={serverIp}
                    onChange={(e) => setServerIp(e.target.value)}
                    placeholder="https://leaguebuilds.hopto.org"
                    required
                  />
                  <button
                    type="button"
                    className="inline-action-button"
                    onClick={() => setServerIp(defaultSettings.serverIp)}
                    disabled={serverIp.trim() === defaultSettings.serverIp}
                    aria-label="Reset server host to default"
                    title="Reset to default"
                  >
                    Reset
                  </button>
                </div>
              </label>

              <label>
                Summoner Header
                <span className="secret-override-chip">INCOGNITO Override</span>
                <input
                  value={summonerName}
                  placeholder="INCOGNITO"
                  readOnly
                />
              </label>
            </>
          ) : null}

          <label>
            Champion (Name or ID)
            <input
              value={championId}
              onChange={(e) => onChampionInputChange(e.target.value)}
              onBlur={onChampionInputBlur}
              placeholder="Ashe or 22"
              list="champion-name-suggestions"
              autoComplete="off"
              required
            />
            <datalist id="champion-name-suggestions">
              {championSuggestions.map((entry) => (
                <option key={`${entry.value}-${entry.label}`} value={entry.value} label={entry.label} />
              ))}
            </datalist>
          </label>

          <label>
            Position
            <select value={position} onChange={(e) => setPosition(e.target.value)}>
              {positions.map((entry) => (
                <option key={entry || "all"} value={entry}>
                  {entry || "(overall)"}
                </option>
              ))}
            </select>
          </label>

          <div className="actions">
            <button type="submit" disabled={loadingBuild}>
              {loadingBuild ? "Loading build..." : "Fetch Build"}
            </button>
            {incognitoOverride ? (
              <>
                <button type="button" onClick={onCheckVersion} disabled={loadingVersion}>
                  {loadingVersion ? "Checking..." : "Check Server Version"}
                </button>
                <button type="button" onClick={onRetriggerImport} disabled={loadingRetriggerImport}>
                  {loadingRetriggerImport ? "Importing..." : "Retrigger Import"}
                </button>
                <button type="button" onClick={onRetriggerSync} disabled={loadingSyncRefresh}>
                  {loadingSyncRefresh ? "Syncing..." : "Retrigger Sync"}
                </button>
              </>
            ) : null}
          </div>
        </form>

        {incognitoOverride ? (
          <aside className="status-card">
            <h2>Server Status</h2>
            <p>
              Current version: <strong>{version}</strong> (Client {clientVersion})
            </p>
            <p>Backend endpoint: {serverIp || defaultSettings.serverIp}</p>
          </aside>
        ) : null}
        </section>

        {updateNotice ? (
          <section className="update-banner" role="status" aria-live="polite">
            {updateNotice} <a href={LATEST_RELEASE_URL} target="_blank" rel="noreferrer" onClick={onOpenLatestRelease}>Latest release</a>
          </section>
        ) : null}

        {error ? <section className="error-box">{error}</section> : null}

        {build ? (
          <section className="build-display dashboard-grid">
          {/* Champion Section */}
          {build.championMeta && (
            <article className="champion-card">
              <div className="champion-header">
                <TooltipTile
                  title={build.championMeta.name}
                  description={build.championMeta.title}
                  htmlDescription={build.championMeta.blurb}
                  className="champion-splash-wrap"
                >
                  <img
                    src={getChampionSplashUrl(build.championMeta.id)}
                    alt={build.championMeta.name}
                    className="champion-splash"
                  />
                </TooltipTile>
                <div className="champion-info">
                  <div className="champion-top-row">
                    <div className="champion-heading">
                      <h2>{build.championMeta.name}</h2>
                      <p className="champion-title">{build.championMeta.title}</p>
                    </div>
                    {displayedSummoners.length > 0 ? (
                      <div
                        className={`champion-summoners${importSummoners ? "" : " import-disabled"}`}
                        aria-label="Summoner spells"
                      >
                        <div className="champion-summoners-container">
                          <p className="champion-summoners-title">Summoner Spells</p>
                          <div className="champion-summoner-icons">
                            {displayedSummoners.map(({ spellId: summonerId, slot }) => {
                              const meta = build.summonerMetadata?.[String(summonerId)];

                              return (
                                <TooltipTile
                                  key={`champion-summoner-${slot}-${summonerId}`}
                                  title={meta?.name || `Summoner ${summonerId}`}
                                  description={meta?.description || meta?.tooltip}
                                  className="champion-summoner-item"
                                >
                                  <span className="summoner-slot-label">{slot}</span>
                                  {meta?.image ? (
                                    <img
                                      src={getSummonerSpellUrl(meta.image, dataDragonVersion)}
                                      alt={meta.name}
                                      className="champion-summoner-icon"
                                    />
                                  ) : (
                                    <div className="summoner-icon-placeholder">{summonerId}</div>
                                  )}
                                </TooltipTile>
                              );
                            })}
                          </div>
                        </div>
                      </div>
                    ) : null}
                  </div>
                  <div className="stats-row">
                    <div className="stat">
                      <span className="label">Winrate</span>
                      <span className="value" style={{ color: getWinrateColor(build.championWinrate) }}>
                        {formatPercent(build.championWinrate)}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="label">Pickrate</span>
                      <span className="value">{formatPercent(build.championPickrate)}</span>
                    </div>
                    <div className="stat">
                      <span className="label">Position</span>
                      <span className="value">{build.position || "Overall"}</span>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          )}

          {build.championMeta && championAbilities.length > 0 && (
            <article className="abilities-card">
              <div className="abilities-subcontainer">
                <h3>Skills</h3>
                <div className="ability-grid">
                  {championAbilities.map((ability) => (
                    <TooltipTile
                      key={ability.key}
                      title={ability.title}
                      description={ability.description}
                      videoUrl={getSpellVideoUrl(build.championId, ability.key)}
                      className="ability-tile"
                      placement="bottom"
                    >
                      <img
                        src={`https://ddragon.leagueoflegends.com/cdn/${dataDragonVersion}/img/${ability.endpoint}/${ability.image}`}
                        alt={ability.label}
                        className="ability-icon"
                      />
                      <span className={`spell-letter spell-${ability.key === "passive" ? "p" : ability.key}`}>
                        {ability.label}
                      </span>
                    </TooltipTile>
                  ))}
                </div>
              </div>
              {build.skillOrder.length > 0 && (
                <div className="abilities-bottom-section">
                  <div className="abilities-subcontainer">
                    <h3 className="skill-order-title">Skill Upgrade Order</h3>
                    <div className="skill-order">
                      {build.skillOrder.map((skillLevel, index) => {
                        const spellKey = ["q", "w", "e", "r"][skillLevel - 1] || "q";
                        const spellLabel = ["Q", "W", "E", "R"][skillLevel - 1] || `Skill ${skillLevel}`;

                        return (
                          <div key={index} className="skill-level">
                            <span className="level">Level {index + 1}</span>
                            <span className={`skill-id spell-letter spell-${spellKey}`}>{spellLabel}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}
            </article>
          )}

          {/* Items + Boots Section */}
          {(build.items.length > 0 || build.boots.length > 0) && (
            <article className={`items-card${importItems ? "" : " import-disabled"}`}>
              {build.boots.length > 0 && (
                <div className="items-top-section">
                  <div className="items-subcontainer">
                    <h3>Boot Options</h3>
                    <div className="boots-grid">
                      {build.boots.map((bootId, bootIndex) => {
                        const meta = build.itemMetadata?.[String(bootId)];
                        return (
                          <TooltipTile
                            key={`boot-${bootIndex}-${bootId}`}
                            title={meta?.name || `Boot ${bootId}`}
                            description={meta?.plaintext || stripHtml(meta?.description)}
                            className="boot-item"
                          >
                            <img
                              src={getItemImageUrl(meta?.image, bootId, dataDragonVersion)}
                              alt={meta?.name || `Boot ${bootId}`}
                            />
                            <h4>{meta?.name || `Boot ${bootId}`}</h4>
                          </TooltipTile>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}

              {build.items.length > 0 && (
                <div className={build.boots.length > 0 ? "items-bottom-section" : undefined}>
                  <div className="items-subcontainer">
                    <h3 className={build.boots.length > 0 ? "items-subtitle" : undefined}>Core Items</h3>
                    {hiddenCoreItemsCount > 0 ? (
                      <p className="core-items-hint">Showing top {displayedCoreItems.length} items</p>
                    ) : null}
                    <div className="items-grid">
                      {displayedCoreItems.map((itemId, itemIndex) => {
                        const meta = build.itemMetadata?.[String(itemId)];
                        return (
                          <TooltipTile
                            key={`item-${itemIndex}-${itemId}`}
                            title={meta?.name || `Item ${itemId}`}
                            description={meta?.plaintext || stripHtml(meta?.description)}
                            className="item-card"
                          >
                            <img
                              src={getItemImageUrl(meta?.image, itemId, dataDragonVersion)}
                              alt={meta?.name || `Item ${itemId}`}
                              className="item-icon"
                            />
                            <h4>{meta?.name || `Item ${itemId}`}</h4>
                          </TooltipTile>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}
            </article>
          )}

          {/* Starter Items Section */}
          {build.starterSets.length > 0 && (
            <article className={`starter-items-card${importItems ? "" : " import-disabled"}`}>
              <h3>Starting Items</h3>
              {hiddenStarterSetsCount > 0 ? (
                <p className="core-items-hint">Showing top {displayedStarterSets.length} options</p>
              ) : null}
              <div className="starter-sets">
                {displayedStarterSets.map((set, index) => (
                  <div key={`starter-set-${index}`} className="starter-set">
                    <p className="set-label">Option {index + 1}:</p>
                    <div className="items-row">
                      {set.map((itemId, itemIndex) => (
                        <TooltipTile
                          key={`starter-${index}-${itemIndex}-${itemId}`}
                          title={build.itemMetadata?.[String(itemId)]?.name || `Item ${itemId}`}
                          description={build.itemMetadata?.[String(itemId)]?.plaintext || stripHtml(build.itemMetadata?.[String(itemId)]?.description)}
                          className="small-item"
                        >
                          <img
                            src={getItemImageUrl(build.itemMetadata?.[String(itemId)]?.image, itemId, dataDragonVersion)}
                            alt={build.itemMetadata?.[String(itemId)]?.name || `Item ${itemId}`}
                            onError={(e) => { e.currentTarget.style.display = 'none'; }}
                          />
                        </TooltipTile>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </article>
          )}

          {/* Runes Section */}
          {build.runes.length > 0 && (
            <article className={`runes-card${importRunes ? "" : " import-disabled"}`}>
              <h3>Runes</h3>
              {hiddenRuneLoadoutsCount > 0 ? (
                <p className="core-items-hint">Showing top {displayedRuneLoadouts.length} rune options</p>
              ) : null}
              <div className="runes-grid">
                {displayedRuneLoadouts.map((loadout, index) => {
                  const isSelectedRuneOption = runeOptionIndex === index;
                  const primaryStyleMeta = build.runeStyleMetadata?.[String(loadout.primaryStyle)];
                  const subStyleMeta = build.runeStyleMetadata?.[String(loadout.subStyle)];
                  const primaryPerks = [loadout.primaryPerk1, loadout.primaryPerk2, loadout.primaryPerk3, loadout.primaryPerk4]
                    .map((perkId) => ({ perkId, meta: build.runeMetadata?.[String(perkId)] }))
                    .filter(({ perkId }) => typeof perkId === "number");
                  const secondaryPerks = [loadout.subPerk1, loadout.subPerk2]
                    .map((perkId) => ({ perkId, meta: build.runeMetadata?.[String(perkId)] }))
                    .filter(({ perkId }) => typeof perkId === "number");
                  const statShards = [loadout.offense, loadout.flex, loadout.defense]
                    .map((perkId) => ({ perkId, meta: statShardMeta[perkId] }))
                    .filter(({ perkId }) => typeof perkId === "number");

                  return (
                    <div
                      key={`rune-loadout-${index}`}
                      className={`rune-item rune-loadout${isSelectedRuneOption ? " rune-loadout-selected" : ""}`}
                    >
                      <div className="rune-option-row">
                        <p className="set-label">Option {index + 1}:</p>
                        <button
                          type="button"
                          className={`rune-option-button${isSelectedRuneOption ? " selected" : ""}`}
                          onClick={() => {
                            void onSelectRuneOption(index);
                          }}
                          disabled={loadingRetriggerImport}
                        >
                          {isSelectedRuneOption ? "Selected for Import" : "Select for Import"}
                        </button>
                      </div>
                      <div className="rune-loadout-header">
                        <TooltipTile
                          title={primaryStyleMeta?.name || `Primary ${loadout.primaryStyle}`}
                          description="Primary rune tree"
                          className="rune-tree"
                        >
                          {primaryStyleMeta?.icon ? (
                            <img
                              src={getRuneStyleIconUrl(primaryStyleMeta.icon)}
                              alt={primaryStyleMeta.name}
                              className="rune-tree-icon"
                            />
                          ) : null}
                          <div>
                            <h4>{primaryStyleMeta?.name || `Primary ${loadout.primaryStyle}`}</h4>
                          </div>
                        </TooltipTile>

                        <TooltipTile
                          title={subStyleMeta?.name || `Secondary ${loadout.subStyle}`}
                          description="Secondary rune tree"
                          className="rune-tree"
                        >
                          {subStyleMeta?.icon ? (
                            <img
                              src={getRuneStyleIconUrl(subStyleMeta.icon)}
                              alt={subStyleMeta.name}
                              className="rune-tree-icon"
                            />
                          ) : null}
                          <div>
                            <h4>{subStyleMeta?.name || `Secondary ${loadout.subStyle}`}</h4>
                          </div>
                        </TooltipTile>
                      </div>

                      <div className="rune-perk-columns">
                        <div className="rune-perk-column">
                          <div className="rune-perks-grid rune-perks-grid-primary">
                            {primaryPerks.map(({ perkId, meta }) => (
                              <TooltipTile
                                key={`primary-perk-${index}-${perkId}`}
                                title={meta?.name || `Rune ${perkId}`}
                                description={stripHtml(meta?.shortDesc || meta?.longDesc)}
                                className="rune-perk"
                              >
                                {meta?.icon ? (
                                  <img
                                    src={getRuneIconUrl(meta.icon)}
                                    alt={meta.name}
                                    className="rune-icon"
                                  />
                                ) : (
                                  <div className="rune-icon-placeholder">{perkId}</div>
                                )}
                                <span>{meta?.name || perkId}</span>
                              </TooltipTile>
                            ))}
                          </div>
                        </div>

                        <div className="rune-perk-column">
                          <div className="rune-perks-grid rune-perks-grid-secondary">
                            {secondaryPerks.map(({ perkId, meta }) => (
                              <TooltipTile
                                key={`secondary-perk-${index}-${perkId}`}
                                title={meta?.name || `Rune ${perkId}`}
                                description={stripHtml(meta?.shortDesc || meta?.longDesc)}
                                className="rune-perk"
                              >
                                {meta?.icon ? (
                                  <img
                                    src={getRuneIconUrl(meta.icon)}
                                    alt={meta.name}
                                    className="rune-icon"
                                  />
                                ) : (
                                  <div className="rune-icon-placeholder">{perkId}</div>
                                )}
                                <span>{meta?.name || perkId}</span>
                              </TooltipTile>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="rune-perk-group">
                        <p className="set-label">Stat Shards</p>
                        <div className="rune-perks-row">
                          {statShards.map(({ perkId, meta }, shardIndex) => (
                            <TooltipTile
                              key={`shard-${index}-${shardIndex}-${perkId}`}
                              title={meta?.label || `Shard ${perkId}`}
                              description="Stat shard"
                              className="rune-perk"
                            >
                              {meta?.icon ? (
                                <img
                                  src={getRuneIconUrl(meta.icon)}
                                  alt={meta.label}
                                  className="rune-icon"
                                />
                              ) : (
                                <div className="rune-icon-placeholder">{perkId}</div>
                              )}
                              <span>{meta?.label || perkId}</span>
                            </TooltipTile>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </article>
          )}
          {build.itemBuildPaths.length > 0 && (
            <article className={`build-paths-card${importItems ? "" : " import-disabled"}`}>
              <h3>Build Paths</h3>
              <p className="core-items-hint">Suggested build sequences</p>
              {hiddenBuildPathsCount > 0 ? (
                <p className="core-items-hint">Showing top 3 paths</p>
              ) : null}
              <div className="build-paths-grid">
                {displayedBuildPaths.map((path, pathIndex) => (
                  <div key={`build-path-${pathIndex}`} className="build-path-option">
                    <p className="set-label">Option {pathIndex + 1}:</p>
                    <div className="build-path-row">
                      {path.map((itemId, itemIndex) => {
                        const meta = build.itemMetadata?.[String(itemId)];
                        return (
                          <Fragment key={`build-path-${pathIndex}-${itemIndex}-${itemId}`}>
                            <TooltipTile
                              title={meta?.name || `Item ${itemId}`}
                              description={meta?.plaintext || stripHtml(meta?.description)}
                              className="build-path-item"
                            >
                              <img
                                src={getItemImageUrl(meta?.image, itemId, dataDragonVersion)}
                                alt={meta?.name || `Item ${itemId}`}
                              />
                            </TooltipTile>
                            {itemIndex < path.length - 1 ? <span className="path-arrow">&rarr;</span> : null}
                          </Fragment>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </article>
          )}
          </section>
        ) : null}
      </div>
    </main>
  );
}
