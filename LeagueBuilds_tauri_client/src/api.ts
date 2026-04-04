import type {
  BuildApiResponse,
  BridgeAppliedState,
  ParsedBuild,
  RichBuild,
  ChampionMetadata,
  ItemMetadata,
  SummonerMetadata,
  RuneStyleMetadata,
  RuneMetadata
} from "./types";
import { invoke } from "@tauri-apps/api/core";

type DataDragonChampion = {
  id: string;
  key: string;
  name: string;
  title: string;
  blurb: string;
  image: { full: string };
  passive: { name: string; image: { full: string }; description: string };
  spells: Array<{ name: string; image: { full: string }; description: string }>;
};

type DataDragonItem = {
  id: string;
  name: string;
  description: string;
  plaintext: string;
  image: { full: string };
  gold: string;
  stats: string;
};

type DataDragonSummoner = {
  name: string;
  description: string;
  tooltip: string;
  image: { full: string };
  cooldown: string;
  cooldownBurn: string;
  id: string;
  key: string;
};

type DataDragonRuneStyle = {
  id: number;
  icon: string;
  key: string;
  name: string;
  slots: Array<{
    runes: Array<{
      id: number;
      icon: string;
      key: string;
      longDesc: string;
      name: string;
      shortDesc: string;
    }>;
  }>;
};

function safeJsonParse<T>(raw: string, fallback: T): T {
  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

function parseRunes(raw: string): ParsedBuild["runes"] {
  // Server may return Python-style dict strings with single quotes or a single object.
  const normalized = raw.replace(/'/g, '"');
  const parsed = safeJsonParse<unknown>(normalized, []);

  if (!Array.isArray(parsed)) {
    if (parsed !== null && typeof parsed === "object") {
      return [parsed as ParsedBuild["runes"][number]];
    }

    return [];
  }

  return parsed.filter((entry): entry is ParsedBuild["runes"][number] => {
    return entry !== null && typeof entry === "object";
  }) as ParsedBuild["runes"];
}

function formatMetric(value: number | null | undefined): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "-";
  }

  return String(value);
}

export async function fetchBuild(params: {
  serverIp: string;
  championId: string;
  position?: string;
  summonerName?: string;
}): Promise<ParsedBuild> {
  const { serverIp, championId, position = "", summonerName = "INCOGNITO" } = params;
  const data = await invoke<BuildApiResponse>("fetch_build", {
    serverIp,
    championId,
    position,
    summonerName
  });

  return {
    championId: data.championId,
    champion: data.champion,
    position: data.position,
    runes: parseRunes(data.runes),
    summoners: safeJsonParse<number[]>(data.summ, []),
    items: safeJsonParse<number[]>(data.item, []),
    starterSets: safeJsonParse<number[][]>(data.start_item, []),
    itemBuildPaths: safeJsonParse<number[][]>(data.item_build, []),
    skillOrder: safeJsonParse<number[]>(data.skill_order, []),
    boots: safeJsonParse<number[]>(data.boots, []),
    championWinrate: formatMetric(data.champ_winrate),
    championPickrate: formatMetric(data.champ_pickrate)
  };
}

export async function fetchServerVersion(serverIp: string): Promise<string> {
  return invoke<string>("fetch_version", { serverIp });
}

export async function startLcuBridge(settings: {
  serverIp: string;
  summonerName: string;
  importRunes: boolean;
  importItems: boolean;
  importSummoners: boolean;
  flashPosition: "d" | "f";
  runeOptionIndex: number;
}): Promise<string> {
  return invoke<string>("start_lcu_bridge", settings);
}

export async function updateLcuBridgeSettings(settings: {
  serverIp: string;
  summonerName: string;
  importRunes: boolean;
  importItems: boolean;
  importSummoners: boolean;
  flashPosition: "d" | "f";
  runeOptionIndex: number;
}): Promise<void> {
  await invoke("update_lcu_bridge_settings", settings);
}

export async function getLcuBridgeLastApplied(): Promise<BridgeAppliedState | null> {
  return invoke<BridgeAppliedState | null>("get_lcu_bridge_last_applied");
}

export async function getLcuCurrentSummonerName(): Promise<string | null> {
  return invoke<string | null>("get_lcu_current_summoner_name");
}

export async function retriggerLcuImport(settings: {
  serverIp: string;
  summonerName: string;
  importRunes: boolean;
  importItems: boolean;
  importSummoners: boolean;
  flashPosition: "d" | "f";
  runeOptionIndex: number;
}): Promise<string> {
  return invoke<string>("retrigger_lcu_import", settings);
}

export async function retriggerLcuImportForChampion(settings: {
  serverIp: string;
  summonerName: string;
  championId: string;
  position?: string;
  importRunes: boolean;
  importItems: boolean;
  importSummoners: boolean;
  flashPosition: "d" | "f";
  runeOptionIndex: number;
}): Promise<string> {
  return invoke<string>("retrigger_lcu_import_for_champion", settings);
}

export async function fetchDataDragonVersion(): Promise<string> {
  const response = await fetch("https://ddragon.leagueoflegends.com/api/versions.json");
  if (!response.ok) {
    throw new Error(`failed to fetch Data Dragon versions: ${response.status}`);
  }

  const versions = (await response.json()) as string[];
  return versions[0] ?? "16.7.1";
}

export async function enrichBuildWithMetadata(
  dataDragonVersion: string,
  build: ParsedBuild
): Promise<RichBuild> {
  const [championMeta, itemMetadata, summonerMetadata, runeMaps] = await Promise.all([
    fetchDataDragonChampionMetadata(dataDragonVersion, build.champion),
    fetchDataDragonItemMap(dataDragonVersion),
    fetchDataDragonSummonerMap(dataDragonVersion),
    fetchDataDragonRuneMaps(dataDragonVersion)
  ]);

  const { runeMetadata, runeStyleMetadata } = runeMaps;

  return {
    ...build,
    championMeta: championMeta || undefined,
    itemMetadata,
    summonerMetadata,
    runeStyleMetadata,
    runeMetadata
  };
}

async function fetchDataDragonChampionMetadata(
  version: string,
  championName: string
): Promise<ChampionMetadata | null> {
  const response = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion/${championName}.json`);
  if (!response.ok) {
    return null;
  }

  const payload = (await response.json()) as { data: Record<string, DataDragonChampion> };
  const champion = payload.data[championName] ?? Object.values(payload.data)[0];

  if (!champion) {
    return null;
  }

  const metadata = {
    id: champion.id,
    name: champion.name,
    title: champion.title,
    blurb: champion.blurb,
    image_full: champion.image?.full ?? "",
    spell_name_passive: champion.passive?.name ?? "Passive",
    spell_name_q: champion.spells?.[0]?.name ?? "Q",
    spell_name_w: champion.spells?.[1]?.name ?? "W",
    spell_name_e: champion.spells?.[2]?.name ?? "E",
    spell_name_r: champion.spells?.[3]?.name ?? "R",
    spell_image_passive: champion.passive?.image?.full ?? "",
    spell_image_q: champion.spells?.[0]?.image?.full ?? "",
    spell_image_w: champion.spells?.[1]?.image?.full ?? "",
    spell_image_e: champion.spells?.[2]?.image?.full ?? "",
    spell_image_r: champion.spells?.[3]?.image?.full ?? "",
    spell_text_passive: champion.passive?.description ?? "",
    spell_text_q: champion.spells?.[0]?.description ?? "",
    spell_text_w: champion.spells?.[1]?.description ?? "",
    spell_text_e: champion.spells?.[2]?.description ?? "",
    spell_text_r: champion.spells?.[3]?.description ?? ""
  };

  return metadata;
}

async function fetchDataDragonItemMap(version: string): Promise<Record<string, ItemMetadata>> {
  const response = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/item.json`);
  if (!response.ok) {
    return {};
  }

  const payload = (await response.json()) as { data: Record<string, DataDragonItem> };
  const metadata: Record<string, ItemMetadata> = {};

  Object.entries(payload.data).forEach(([itemId, item]) => {
    metadata[itemId] = {
      id: item.id,
      name: item.name,
      description: item.description,
      plaintext: item.plaintext,
      image: item.image ?? { full: "" },
      gold: item.gold,
      stats: item.stats
    };
  });

  return metadata;
}

async function fetchDataDragonSummonerMap(version: string): Promise<Record<string, SummonerMetadata>> {
  const response = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/summoner.json`);
  if (!response.ok) {
    return {};
  }

  const payload = (await response.json()) as { data: Record<string, DataDragonSummoner> };
  const metadata: Record<string, SummonerMetadata> = {};

  Object.values(payload.data).forEach((summoner) => {
    metadata[summoner.key] = {
      name: summoner.name,
      description: summoner.description,
      tooltip: summoner.tooltip,
      image: summoner.image ?? { full: "" },
      cooldown: summoner.cooldown,
      cooldownBurn: summoner.cooldownBurn
    };
    metadata[summoner.id] = metadata[summoner.key];
  });

  return metadata;
}

async function fetchDataDragonRuneMaps(version: string): Promise<{
  runeMetadata: Record<string, RuneMetadata>;
  runeStyleMetadata: Record<string, RuneStyleMetadata>;
}> {
  const response = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/runesReforged.json`);
  if (!response.ok) {
    return { runeMetadata: {}, runeStyleMetadata: {} };
  }

  const styles = (await response.json()) as DataDragonRuneStyle[];
  const runeMetadata: Record<string, RuneMetadata> = {};
  const runeStyleMetadata: Record<string, RuneStyleMetadata> = {};

  styles.forEach((style) => {
    runeStyleMetadata[String(style.id)] = {
      id: style.id,
      icon: style.icon,
      key: style.key,
      name: style.name
    };

    style.slots.forEach((slot) => {
      slot.runes.forEach((rune) => {
        runeMetadata[String(rune.id)] = {
          id: rune.id,
          name: rune.name,
          icon: rune.icon,
          shortDesc: rune.shortDesc,
          longDesc: rune.longDesc,
          key: rune.key
        };
      });
    });
  });

  return { runeMetadata, runeStyleMetadata };
}
