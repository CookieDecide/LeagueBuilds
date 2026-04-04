export type BuildApiResponse = {
  championId: string;
  runes: string;
  summ: string;
  item: string;
  start_item: string;
  item_build: string;
  skill_order: string;
  position: string;
  boots: string;
  champion: string;
  champ_winrate?: number | null;
  champ_pickrate?: number | null;
};

export type DataDragonImage = {
  full: string;
  sprite?: string;
  group?: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
};

export type ChampionMetadata = {
  id: string;
  name: string;
  title: string;
  blurb: string;
  image_full: string;
  spell_name_passive: string;
  spell_name_q: string;
  spell_name_w: string;
  spell_name_e: string;
  spell_name_r: string;
  spell_image_passive: string;
  spell_image_q: string;
  spell_image_w: string;
  spell_image_e: string;
  spell_image_r: string;
  spell_text_passive: string;
  spell_text_q: string;
  spell_text_w: string;
  spell_text_e: string;
  spell_text_r: string;
};

export type ItemMetadata = {
  id: string;
  name: string;
  description: string;
  plaintext: string;
  image: DataDragonImage;
  gold: string;
  stats: string;
};

export type SummonerMetadata = {
  name: string;
  description: string;
  tooltip: string;
  image: DataDragonImage;
  cooldown: string;
  cooldownBurn: string;
};

export type RuneStyleMetadata = {
  id: number;
  icon: string;
  key: string;
  name: string;
};

export type RuneMetadata = {
  id: number;
  name: string;
  icon: string;
  shortDesc: string;
  longDesc: string;
  key: string;
};

export type RuneLoadout = {
  primaryStyle: number;
  primaryPerk1: number;
  primaryPerk2: number;
  primaryPerk3: number;
  primaryPerk4: number;
  subStyle: number;
  subPerk1: number;
  subPerk2: number;
  defense: number;
  flex: number;
  offense: number;
};

export type ParsedBuild = {
  championId: string;
  champion: string;
  position: string;
  runes: RuneLoadout[];
  summoners: number[];
  items: number[];
  starterSets: number[][];
  itemBuildPaths: number[][];
  skillOrder: number[];
  boots: number[];
  championWinrate: string;
  championPickrate: string;
};

export type RichBuild = ParsedBuild & {
  championMeta?: ChampionMetadata;
  itemMetadata?: Record<string, ItemMetadata>;
  summonerMetadata?: Record<string, SummonerMetadata>;
  runeStyleMetadata?: Record<string, RuneStyleMetadata>;
  runeMetadata?: Record<string, RuneMetadata>;
};

export type ClientSettings = {
  serverIp: string;
  summonerName: string;
  importRunes: boolean;
  importItems: boolean;
  importSummoners: boolean;
  flashPosition: "d" | "f";
  runeOptionIndex: number;
  incognitoOverride: boolean;
};

export type BridgeAppliedState = {
  champion_id: string;
  position: string;
  summoner_name: string;
};
