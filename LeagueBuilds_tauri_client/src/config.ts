import type { ClientSettings } from "./types";

const STORAGE_KEY = "leaguebuilds.settings.v1";

const LEGACY_SERVER_DEFAULTS = new Set([
  "leaguebuilds.hopto.org",
  "http://leaguebuilds.hopto.org:12345"
]);

export const defaultSettings: ClientSettings = {
  serverIp: "https://leaguebuilds.hopto.org",
  summonerName: "INCOGNITO",
  importRunes: true,
  importItems: true,
  importSummoners: true,
  flashPosition: "d",
  runeOptionIndex: 0,
  incognitoOverride: false
};

function normalizeServerUrl(value: string | undefined): string {
  const trimmed = value?.trim() || "";
  if (!trimmed) {
    return defaultSettings.serverIp;
  }

  if (LEGACY_SERVER_DEFAULTS.has(trimmed.toLowerCase())) {
    return defaultSettings.serverIp;
  }

  return trimmed;
}

export function loadSettings(): ClientSettings {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return defaultSettings;
  }

  try {
    const parsed = JSON.parse(raw) as Partial<ClientSettings>;
    return {
      serverIp: normalizeServerUrl(parsed.serverIp),
      summonerName: defaultSettings.summonerName,
      importRunes: typeof parsed.importRunes === "boolean" ? parsed.importRunes : defaultSettings.importRunes,
      importItems: typeof parsed.importItems === "boolean" ? parsed.importItems : defaultSettings.importItems,
      importSummoners:
        typeof parsed.importSummoners === "boolean" ? parsed.importSummoners : defaultSettings.importSummoners,
      flashPosition: parsed.flashPosition === "f" ? "f" : "d",
      runeOptionIndex:
        Number.isInteger(parsed.runeOptionIndex) && (parsed.runeOptionIndex as number) >= 0
          ? (parsed.runeOptionIndex as number)
          : defaultSettings.runeOptionIndex,
      incognitoOverride:
        typeof parsed.incognitoOverride === "boolean"
          ? parsed.incognitoOverride
          : defaultSettings.incognitoOverride
    };
  } catch {
    return defaultSettings;
  }
}

export function saveSettings(settings: ClientSettings): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
}
