use reqwest::Method;
use serde::{Deserialize, Serialize};
use serde::de::DeserializeOwned;
use serde_json::{json, Value};
use std::path::PathBuf;
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Arc, Mutex, OnceLock,
};
use std::time::Duration;

use tokio::time::sleep;

#[derive(Deserialize)]
struct BuildApiResponse {
    #[serde(rename = "championId")]
    champion_id: String,
    runes: String,
    summ: String,
    item: String,
    start_item: String,
    item_build: String,
    boots: String,
    champion: String,
}

#[derive(Clone, Deserialize, Serialize)]
struct RuneLoadout {
    #[serde(rename = "primaryStyle")]
    primary_style: u64,
    #[serde(rename = "primaryPerk1")]
    primary_perk1: u64,
    #[serde(rename = "primaryPerk2")]
    primary_perk2: u64,
    #[serde(rename = "primaryPerk3")]
    primary_perk3: u64,
    #[serde(rename = "primaryPerk4")]
    primary_perk4: u64,
    #[serde(rename = "subStyle")]
    sub_style: u64,
    #[serde(rename = "subPerk1")]
    sub_perk1: u64,
    #[serde(rename = "subPerk2")]
    sub_perk2: u64,
    offense: u64,
    flex: u64,
    defense: u64,
}

#[derive(Clone)]
struct ParsedBuild {
    champion_id: String,
    champion: String,
    runes: Vec<RuneLoadout>,
    summoners: Vec<u64>,
    items: Vec<u64>,
    starter_sets: Vec<Vec<u64>>,
    item_build_paths: Vec<Vec<u64>>,
    boots: Vec<u64>,
}

#[derive(Clone)]
struct BridgeSettings {
    server_ip: String,
    summoner_name: String,
    import_runes: bool,
    import_items: bool,
    import_summoners: bool,
    flash_position: String,
    rune_option_index: usize,
}

struct BridgeState {
    settings: Mutex<BridgeSettings>,
    running: AtomicBool,
    last_applied: Mutex<Option<BridgeAppliedState>>,
}

#[derive(Clone, Serialize)]
pub struct BridgeAppliedState {
    champion_id: String,
    position: String,
    summoner_name: String,
}

struct LockfileInfo {
    port: String,
    password: String,
    protocol: String,
}

struct LcuConnection {
    client: reqwest::Client,
    base_url: String,
    password: String,
}

static BRIDGE_STATE: OnceLock<Arc<BridgeState>> = OnceLock::new();

fn bridge_state() -> Arc<BridgeState> {
    BRIDGE_STATE
        .get_or_init(|| {
            Arc::new(BridgeState {
                settings: Mutex::new(BridgeSettings {
                    server_ip: String::new(),
                    summoner_name: String::new(),
                    import_runes: true,
                    import_items: true,
                    import_summoners: true,
                    flash_position: "d".to_string(),
                    rune_option_index: 0,
                }),
                running: AtomicBool::new(false),
                last_applied: Mutex::new(None),
            })
        })
        .clone()
}

fn candidate_lockfiles() -> Vec<PathBuf> {
    let mut candidates = Vec::new();

    if let Ok(local_app_data) = std::env::var("LOCALAPPDATA") {
        let base = PathBuf::from(local_app_data);
        candidates.push(base.join("Riot Games").join("League of Legends").join("lockfile"));
    }

    if let Ok(program_files) = std::env::var("PROGRAMFILES") {
        candidates.push(PathBuf::from(program_files).join("Riot Games").join("League of Legends").join("lockfile"));
    }

    candidates.push(PathBuf::from(r"C:\Riot Games\League of Legends\lockfile"));

    // Keep Riot Client lockfiles as a last-resort fallback; they do not always expose LoL champ-select endpoints.
    if let Ok(local_app_data) = std::env::var("LOCALAPPDATA") {
        let base = PathBuf::from(local_app_data);
        candidates.push(base.join("Riot Games").join("Riot Client").join("Config").join("lockfile"));
    }

    candidates.push(PathBuf::from(r"C:\Riot Games\Riot Client\Config\lockfile"));

    candidates
}

fn find_lockfile_path() -> Option<PathBuf> {
    candidate_lockfiles().into_iter().find(|candidate| candidate.exists())
}

fn read_lockfile(path: &PathBuf) -> Result<LockfileInfo, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|error| format!("failed to read LCU lockfile: {error}"))?;
    let parts: Vec<&str> = content.trim().split(':').collect();

    if parts.len() < 5 {
        return Err("invalid LCU lockfile format".to_string());
    }

    Ok(LockfileInfo {
        port: parts[2].to_string(),
        password: parts[3].to_string(),
        protocol: parts[4].to_string(),
    })
}

fn build_lcu_connection(lockfile: &LockfileInfo) -> Result<LcuConnection, String> {
    let client = reqwest::Client::builder()
        // Match common LCU client libraries: trust loopback endpoint and rely on lockfile auth.
        .danger_accept_invalid_certs(true)
        .build()
        .map_err(|error| format!("failed to create LCU client: {error}"))?;

    Ok(LcuConnection {
        client,
        base_url: format!("{}://127.0.0.1:{}", lockfile.protocol, lockfile.port),
        password: lockfile.password.clone(),
    })
}

async fn lcu_request(
    connection: &LcuConnection,
    method: Method,
    path: &str,
    body: Option<Value>,
) -> Result<reqwest::Response, String> {
    let url = format!("{}/{}", connection.base_url, path.trim_start_matches('/'));
    let mut request = connection
        .client
        .request(method, url)
        .basic_auth("riot", Some(connection.password.as_str()));

    if let Some(body) = body {
        request = request.json(&body);
    }

    request
        .send()
        .await
        .map_err(|error| format!("LCU request failed: {error}"))
}

async fn lcu_get_json(connection: &LcuConnection, path: &str) -> Result<Value, String> {
    let response = lcu_request(connection, Method::GET, path, None).await?;

    if !response.status().is_success() {
        return Err(format!("LCU GET {} failed with {}", path, response.status()));
    }

    response
        .json::<Value>()
        .await
        .map_err(|error| format!("invalid LCU JSON response: {error}"))
}

async fn lcu_send_json(
    connection: &LcuConnection,
    method: Method,
    path: &str,
    body: Option<Value>,
) -> Result<(), String> {
    let response = lcu_request(connection, method, path, body).await?;

    if !response.status().is_success() {
        return Err(format!("LCU request {} failed with {}", path, response.status()));
    }

    Ok(())
}

fn parse_jsonish<T: DeserializeOwned>(raw: &str) -> Result<T, String> {
    let normalized = raw.replace('\'', "\"");
    serde_json::from_str::<T>(&normalized).map_err(|error| format!("failed to parse build payload: {error}"))
}

async fn request_build(
    server_ip: &str,
    champion_id: &str,
    position: &str,
    summoner_name: &str,
) -> Result<ParsedBuild, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(server_ip)?;
    let mut endpoint = format!("{}/builds_v1/{}", base_url, champion_id.trim());

    if !position.trim().is_empty() {
        endpoint.push('/');
        endpoint.push_str(&position.trim().to_lowercase());
    }

    let response = client
        .get(&endpoint)
        .header("Summoner", summoner_name.trim())
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("build request failed with {}", response.status()));
    }

    let response = response
        .json::<BuildApiResponse>()
        .await
        .map_err(|error| format!("invalid build response: {error}"))?;

    Ok(ParsedBuild {
        champion_id: response.champion_id,
        champion: response.champion,
        runes: parse_jsonish::<Vec<RuneLoadout>>(&response.runes)?,
        summoners: parse_jsonish::<Vec<u64>>(&response.summ)?,
        items: parse_jsonish::<Vec<u64>>(&response.item)?,
        starter_sets: parse_jsonish::<Vec<Vec<u64>>>(&response.start_item)?,
        item_build_paths: parse_jsonish::<Vec<Vec<u64>>>(&response.item_build)?,
        boots: parse_jsonish::<Vec<u64>>(&response.boots)?,
    })
}

fn resolve_server_base_url(server_input: &str) -> Result<String, String> {
    let trimmed = server_input.trim().trim_end_matches('/');
    if trimmed.is_empty() {
        return Err("server URL is empty".to_string());
    }

    if trimmed.starts_with("http://") || trimmed.starts_with("https://") {
        return Ok(trimmed.to_string());
    }

    Ok(format!("http://{}:12345", trimmed))
}

async fn fetch_current_champion(connection: &LcuConnection) -> Result<Option<u64>, String> {
    // Prefer my-selection for earlier detection (before final lock-in).
    let my_selection_response = lcu_request(connection, Method::GET, "/lol-champ-select/v1/session/my-selection", None).await?;

    if my_selection_response.status().is_success() {
        let payload = my_selection_response
            .json::<Value>()
            .await
            .map_err(|error| format!("invalid my-selection response: {error}"))?;

        if let Some(champion_id) = payload.get("championId").and_then(Value::as_u64).filter(|value| *value != 0) {
            return Ok(Some(champion_id));
        }

        if let Some(champion_pick_intent) = payload
            .get("championPickIntent")
            .and_then(Value::as_u64)
            .filter(|value| *value != 0)
        {
            return Ok(Some(champion_pick_intent));
        }
    }

    // Fall back to session actions to catch local picks that are selected but not yet locked.
    let session_response = lcu_request(connection, Method::GET, "/lol-champ-select/v1/session", None).await?;
    if session_response.status().is_success() {
        let session = session_response
            .json::<Value>()
            .await
            .map_err(|error| format!("invalid session response: {error}"))?;

        if let Some(local_cell_id) = session.get("localPlayerCellId").and_then(Value::as_i64) {
            if let Some(actions) = session.get("actions").and_then(Value::as_array) {
                for action_set in actions {
                    let Some(action_entries) = action_set.as_array() else {
                        continue;
                    };

                    for action in action_entries {
                        let actor_cell_id = action.get("actorCellId").and_then(Value::as_i64).unwrap_or(-1);
                        let action_type = action.get("type").and_then(Value::as_str).unwrap_or("");
                        let champion_id = action.get("championId").and_then(Value::as_u64).unwrap_or(0);

                        if actor_cell_id == local_cell_id && action_type == "pick" && champion_id != 0 {
                            return Ok(Some(champion_id));
                        }
                    }
                }
            }
        }
    }

    let response = lcu_request(connection, Method::GET, "/lol-champ-select/v1/current-champion", None).await?;

    if !response.status().is_success() {
        return Ok(None);
    }

    let payload = response
        .json::<Value>()
        .await
        .map_err(|error| format!("invalid champion response: {error}"))?;

    Ok(payload.as_u64().filter(|value| *value != 0))
}

async fn fetch_position(connection: &LcuConnection) -> Result<String, String> {
    let session = lcu_get_json(connection, "/lol-champ-select/v1/session").await?;

    let allow_battle_boost = session
        .get("allowBattleBoost")
        .and_then(Value::as_bool)
        .unwrap_or(false);
    let allow_rerolling = session
        .get("allowRerolling")
        .and_then(Value::as_bool)
        .unwrap_or(false);
    let bench_enabled = session
        .get("benchEnabled")
        .and_then(Value::as_bool)
        .unwrap_or(false);

    if allow_battle_boost && allow_rerolling && bench_enabled {
        return Ok("aram".to_string());
    }

    let local_player_cell_id = session
        .get("localPlayerCellId")
        .and_then(Value::as_i64)
        .ok_or_else(|| "missing localPlayerCellId from LCU session".to_string())?;

    let summoner = lcu_get_json(
        connection,
        &format!("/lol-champ-select/v1/summoners/{local_player_cell_id}"),
    )
    .await?;

    Ok(summoner
        .get("assignedPosition")
        .and_then(Value::as_str)
        .unwrap_or("")
        .to_string())
}

async fn fetch_current_summoner_name(connection: &LcuConnection) -> Result<String, String> {
    let payload = lcu_get_json(connection, "/lol-summoner/v1/current-summoner").await?;
    let display_name = payload.get("displayName").and_then(Value::as_str).unwrap_or("");
    let game_name = payload.get("gameName").and_then(Value::as_str).unwrap_or("");
    let internal_name = payload.get("internalName").and_then(Value::as_str).unwrap_or("");

    if !display_name.is_empty() {
        Ok(display_name.to_string())
    } else if !game_name.is_empty() {
        Ok(game_name.to_string())
    } else if !internal_name.is_empty() {
        Ok(internal_name.to_string())
    } else {
        Ok(payload
            .get("summonerId")
            .and_then(Value::as_i64)
            .map(|value| value.to_string())
            .unwrap_or_else(|| "INCOGNITO".to_string()))
    }
}

async fn fetch_account_and_summoner_ids(connection: &LcuConnection) -> Result<(i64, i64), String> {
    let payload = lcu_get_json(connection, "/lol-summoner/v1/current-summoner/account-and-summoner-ids").await?;
    let account_id = payload
        .get("accountId")
        .and_then(Value::as_i64)
        .ok_or_else(|| "missing accountId from LCU response".to_string())?;
    let summoner_id = payload
        .get("summonerId")
        .and_then(Value::as_i64)
        .ok_or_else(|| "missing summonerId from LCU response".to_string())?;

    Ok((account_id, summoner_id))
}

fn build_itemset_body(
    champion_id: &str,
    champion_name: &str,
    starter_sets: &[Vec<u64>],
    item_build_paths: &[Vec<u64>],
    core_items: &[u64],
    boots: &[u64],
) -> Value {
    let mut blocks = Vec::new();

    for (index, start_set) in starter_sets.iter().enumerate() {
        blocks.push(json!({
            "type": format!("Start Items {}", index + 1),
            "items": start_set.iter().map(|item_id| json!({"count": 1, "id": item_id.to_string()})).collect::<Vec<_>>(),
            "hideIfSummonerSpell": "",
            "showIfSummonerSpell": ""
        }));
    }

    if !boots.is_empty() {
        blocks.push(json!({
            "type": "Boots",
            "items": boots.iter().map(|item_id| json!({"count": 1, "id": item_id.to_string()})).collect::<Vec<_>>(),
            "hideIfSummonerSpell": "",
            "showIfSummonerSpell": ""
        }));
    }

    for (index, path) in item_build_paths.iter().enumerate() {
        blocks.push(json!({
            "type": format!("Build {}", index + 1),
            "items": path.iter().map(|item_id| json!({"count": 1, "id": item_id.to_string()})).collect::<Vec<_>>(),
            "hideIfSummonerSpell": "",
            "showIfSummonerSpell": ""
        }));
    }

    if !core_items.is_empty() {
        blocks.push(json!({
            "type": "Core Items",
            "items": core_items.iter().map(|item_id| json!({"count": 1, "id": item_id.to_string()})).collect::<Vec<_>>(),
            "hideIfSummonerSpell": "",
            "showIfSummonerSpell": ""
        }));
    }

    json!({
        "associatedChampions": [champion_id],
        "associatedMaps": [],
        "blocks": blocks,
        "map": "any",
        "mode": "any",
        "preferredItemSlots": [],
        "sortrank": 1,
        "startedFrom": "blank",
        "title": champion_name,
        "type": "custom",
        "uid": "1"
    })
}

async fn delete_current_perks_page(connection: &LcuConnection) -> Result<(), String> {
    let current_page_response = lcu_request(connection, Method::GET, "/lol-perks/v1/currentpage", None).await?;

    if !current_page_response.status().is_success() {
        return lcu_send_json(connection, Method::DELETE, "/lol-perks/v1/pages", None).await;
    }

    let current_page = current_page_response
        .json::<Value>()
        .await
        .map_err(|error| format!("invalid perk page response: {error}"))?;

    if current_page
        .get("isTemporary")
        .and_then(Value::as_bool)
        .unwrap_or(false)
    {
        lcu_send_json(connection, Method::DELETE, "/lol-perks/v1/pages", None).await
    } else if let Some(page_id) = current_page.get("id").and_then(Value::as_i64) {
        lcu_send_json(connection, Method::DELETE, &format!("/lol-perks/v1/pages/{page_id}"), None).await
    } else {
        lcu_send_json(connection, Method::DELETE, "/lol-perks/v1/pages", None).await
    }
}

async fn set_perks(connection: &LcuConnection, champion_id: u64, rune: &RuneLoadout, champion_name: &str) -> Result<(), String> {
    let body = json!({
        "name": champion_name,
        "primaryStyleId": rune.primary_style,
        "subStyleId": rune.sub_style,
        "selectedPerkIds": [
            rune.primary_perk1,
            rune.primary_perk2,
            rune.primary_perk3,
            rune.primary_perk4,
            rune.sub_perk1,
            rune.sub_perk2,
            rune.offense,
            rune.flex,
            rune.defense,
        ],
        "quickPlayChampionIds": [champion_id],
        "current": true
    });

    lcu_send_json(connection, Method::POST, "/lol-perks/v1/pages", Some(body)).await
}

async fn set_summoners(connection: &LcuConnection, summoners: &[u64], flash_position: &str) -> Result<(), String> {
    if summoners.len() < 2 {
        return Ok(());
    }

    let flash_id = 4_u64;
    let prefer_flash_on_d = flash_position.eq_ignore_ascii_case("d");
    let mut spell1_id = summoners[0];
    let mut spell2_id = summoners[1];

    if summoners.contains(&flash_id) {
        let fallback_other = if spell1_id == flash_id {
            spell2_id
        } else if spell2_id == flash_id {
            spell1_id
        } else {
            summoners
                .iter()
                .copied()
                .find(|spell_id| *spell_id != flash_id)
                .unwrap_or(spell2_id)
        };

        if prefer_flash_on_d {
            spell1_id = flash_id;
            spell2_id = fallback_other;
        } else {
            spell1_id = fallback_other;
            spell2_id = flash_id;
        }
    }

    let body = json!({
        "spell1Id": spell1_id,
        "spell2Id": spell2_id
    });

    lcu_send_json(
        connection,
        Method::PATCH,
        "/lol-champ-select/v1/session/my-selection",
        Some(body),
    )
    .await
}

async fn set_itemset(
    connection: &LcuConnection,
    account_id: i64,
    summoner_id: i64,
    champion_id: &str,
    champion_name: &str,
    starter_sets: &[Vec<u64>],
    item_build_paths: &[Vec<u64>],
    core_items: &[u64],
    boots: &[u64],
) -> Result<(), String> {
    let body = json!({
        "accountId": account_id,
        "itemSets": [build_itemset_body(champion_id, champion_name, starter_sets, item_build_paths, core_items, boots)],
        "timestamp": 0
    });

    lcu_send_json(
        connection,
        Method::PUT,
        &format!("/lol-item-sets/v1/item-sets/{summoner_id}/sets"),
        Some(body),
    )
    .await
}

async fn apply_build_to_lcu(
    connection: &LcuConnection,
    champion_id: u64,
    build: &ParsedBuild,
    summoner_name: &str,
    import_runes: bool,
    import_items: bool,
    import_summoners: bool,
    flash_position: &str,
    rune_option_index: usize,
) -> Result<(), String> {
    let rune = build
        .runes
        .get(rune_option_index)
        .or_else(|| build.runes.first())
        .ok_or_else(|| "no rune loadout found in build payload".to_string())?;

    if rune_option_index >= build.runes.len() && !build.runes.is_empty() {
        eprintln!(
            "LeagueBuilds LCU bridge rune option {} out of range ({} options); using option 1.",
            rune_option_index + 1,
            build.runes.len()
        );
    }

    let active_champion_name = if build.champion.is_empty() {
        champion_id.to_string()
    } else {
        build.champion.clone()
    };

    let (account_id, summoner_id) = fetch_account_and_summoner_ids(connection).await?;

    if import_runes {
        let _ = delete_current_perks_page(connection).await;
        set_perks(connection, champion_id, rune, &active_champion_name).await?;
    }

    if import_summoners {
        if let Err(error) = set_summoners(connection, &build.summoners, flash_position).await {
            // Outside champ select this endpoint is commonly unavailable; keep importing other configured data.
            eprintln!("LeagueBuilds LCU bridge could not set summoner spells (continuing): {error}");
        }
    }

    if import_items {
        set_itemset(
            connection,
            account_id,
            summoner_id,
            &build.champion_id,
            &active_champion_name,
            &build.starter_sets,
            &build.item_build_paths,
            &build.items,
            &build.boots,
        )
        .await?;
    } else {
        let _ = (account_id, summoner_id);
    }

    if !import_runes && !import_summoners && !import_items {
        eprintln!("LeagueBuilds LCU bridge import skipped: all import options are disabled.");
        return Ok(());
    }

    let _ = summoner_name;
    Ok(())
}

async fn run_lcu_bridge(state: Arc<BridgeState>) {
    let mut last_champion: Option<u64> = None;
    let mut last_lockfile_path: Option<String> = None;

    loop {
        let settings = state.settings.lock().unwrap().clone();

        if let Some(lockfile_path) = find_lockfile_path() {
            let lockfile_path_string = lockfile_path.to_string_lossy().to_string();
            if last_lockfile_path.as_deref() != Some(lockfile_path_string.as_str()) {
                eprintln!("LeagueBuilds LCU bridge using lockfile: {}", lockfile_path_string);
                last_lockfile_path = Some(lockfile_path_string);
            }

            match read_lockfile(&lockfile_path).and_then(|lockfile| build_lcu_connection(&lockfile)) {
                Ok(connection) => {
                    match fetch_current_champion(&connection).await {
                        Ok(Some(champion_id)) if Some(champion_id) != last_champion => {
                            let position = fetch_position(&connection).await.unwrap_or_default();
                            let summoner_name = if settings.summoner_name.trim().is_empty() {
                                fetch_current_summoner_name(&connection)
                                    .await
                                    .unwrap_or_else(|_| "INCOGNITO".to_string())
                            } else {
                                settings.summoner_name.clone()
                            };

                            match request_build(
                                &settings.server_ip,
                                &champion_id.to_string(),
                                &position,
                                &summoner_name,
                            )
                            .await
                            {
                                Ok(parsed_build) => {
                                    eprintln!(
                                        "LeagueBuilds LCU bridge applying build for champion {} (position: {})",
                                        champion_id,
                                        if position.is_empty() { "unknown" } else { position.as_str() }
                                    );
                                    if let Err(error) = apply_build_to_lcu(
                                        &connection,
                                        champion_id,
                                        &parsed_build,
                                        &summoner_name,
                                        settings.import_runes,
                                        settings.import_items,
                                        settings.import_summoners,
                                        settings.flash_position.as_str(),
                                        settings.rune_option_index,
                                    )
                                    .await
                                    {
                                        eprintln!("LeagueBuilds LCU bridge failed to apply build: {error}");
                                    } else {
                                        last_champion = Some(champion_id);
                                        if let Ok(mut last_applied) = state.last_applied.lock() {
                                            *last_applied = Some(BridgeAppliedState {
                                                champion_id: champion_id.to_string(),
                                                position: position.to_lowercase(),
                                                summoner_name: summoner_name.clone(),
                                            });
                                        }
                                        eprintln!("LeagueBuilds LCU bridge successfully applied build.");
                                    }
                                }
                                Err(error) => {
                                    eprintln!("LeagueBuilds LCU bridge failed to fetch build: {error}");
                                }
                            }
                        }
                        Ok(Some(_)) => {}
                        Ok(None) => {
                            last_champion = None;
                        }
                        Err(error) => {
                            eprintln!("LeagueBuilds LCU bridge could not read current champion: {error}");
                            last_champion = None;
                        }
                    }
                }
                Err(error) => {
                    eprintln!("LeagueBuilds LCU bridge could not connect to the client: {error}");
                    last_champion = None;
                }
            }
        } else {
            eprintln!("LeagueBuilds LCU bridge could not find a League lockfile.");
            last_champion = None;
            last_lockfile_path = None;
        }

        sleep(Duration::from_secs(2)).await;
    }
}

async fn apply_current_selection_once(state: &Arc<BridgeState>) -> Result<String, String> {
    let settings = state
        .settings
        .lock()
        .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?
        .clone();

    let lockfile_path = find_lockfile_path().ok_or_else(|| "could not find a League lockfile".to_string())?;
    let connection = read_lockfile(&lockfile_path).and_then(|lockfile| build_lcu_connection(&lockfile))?;

    let champion_id = fetch_current_champion(&connection)
        .await?
        .ok_or_else(|| "no selected champion found in champ select".to_string())?;

    let position = fetch_position(&connection).await.unwrap_or_default();
    let summoner_name = if settings.summoner_name.trim().is_empty() {
        fetch_current_summoner_name(&connection)
            .await
            .unwrap_or_else(|_| "INCOGNITO".to_string())
    } else {
        settings.summoner_name.clone()
    };

    let parsed_build = request_build(
        &settings.server_ip,
        &champion_id.to_string(),
        &position,
        &summoner_name,
    )
    .await?;

    apply_build_to_lcu(
        &connection,
        champion_id,
        &parsed_build,
        &summoner_name,
        settings.import_runes,
        settings.import_items,
        settings.import_summoners,
        settings.flash_position.as_str(),
        settings.rune_option_index,
    )
    .await?;

    let mut last_applied = state
        .last_applied
        .lock()
        .map_err(|_| "failed to acquire LCU bridge state lock".to_string())?;
    *last_applied = Some(BridgeAppliedState {
        champion_id: champion_id.to_string(),
        position: position.to_lowercase(),
        summoner_name,
    });

    Ok(format!("Applied build for champion {champion_id}"))
}

async fn apply_specific_champion_once(
    state: &Arc<BridgeState>,
    champion_id: u64,
    position: String,
) -> Result<String, String> {
    let settings = state
        .settings
        .lock()
        .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?
        .clone();

    let lockfile_path = find_lockfile_path().ok_or_else(|| "could not find a League lockfile".to_string())?;
    let connection = read_lockfile(&lockfile_path).and_then(|lockfile| build_lcu_connection(&lockfile))?;

    let normalized_position = position.trim().to_lowercase();
    let summoner_name = if settings.summoner_name.trim().is_empty() {
        fetch_current_summoner_name(&connection)
            .await
            .unwrap_or_else(|_| "INCOGNITO".to_string())
    } else {
        settings.summoner_name.clone()
    };

    let parsed_build = request_build(
        &settings.server_ip,
        &champion_id.to_string(),
        &normalized_position,
        &summoner_name,
    )
    .await?;

    apply_build_to_lcu(
        &connection,
        champion_id,
        &parsed_build,
        &summoner_name,
        settings.import_runes,
        settings.import_items,
        settings.import_summoners,
        settings.flash_position.as_str(),
        settings.rune_option_index,
    )
    .await?;

    let mut last_applied = state
        .last_applied
        .lock()
        .map_err(|_| "failed to acquire LCU bridge state lock".to_string())?;
    *last_applied = Some(BridgeAppliedState {
        champion_id: champion_id.to_string(),
        position: normalized_position,
        summoner_name,
    });

    Ok(format!("Applied build for champion {champion_id}"))
}

#[tauri::command]
pub async fn start_lcu_bridge(
    server_ip: String,
    summoner_name: String,
    import_runes: Option<bool>,
    import_items: Option<bool>,
    import_summoners: Option<bool>,
    flash_position: Option<String>,
    rune_option_index: Option<usize>,
) -> Result<String, String> {
    let state = bridge_state();

    eprintln!(
        "LeagueBuilds LCU bridge start requested (server_ip: '{}', summoner_name: '{}')",
        server_ip,
        summoner_name
    );

    {
        let mut settings = state
            .settings
            .lock()
            .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?;
        settings.server_ip = server_ip;
        settings.summoner_name = summoner_name;
        settings.import_runes = import_runes.unwrap_or(true);
        settings.import_items = import_items.unwrap_or(true);
        settings.import_summoners = import_summoners.unwrap_or(true);
        settings.flash_position = flash_position.unwrap_or_else(|| "d".to_string()).to_lowercase();
        settings.rune_option_index = rune_option_index.unwrap_or(0);
    }

    if !state.running.swap(true, Ordering::SeqCst) {
        eprintln!("LeagueBuilds LCU bridge background task started.");
        let bridge_state = state.clone();
        tauri::async_runtime::spawn(async move {
            run_lcu_bridge(bridge_state).await;
        });
    } else {
        eprintln!("LeagueBuilds LCU bridge already running; settings updated.");
    }

    Ok("LCU bridge initialized".to_string())
}

#[tauri::command]
pub async fn update_lcu_bridge_settings(
    server_ip: String,
    summoner_name: String,
    import_runes: Option<bool>,
    import_items: Option<bool>,
    import_summoners: Option<bool>,
    flash_position: Option<String>,
    rune_option_index: Option<usize>,
) -> Result<(), String> {
    let state = bridge_state();
    let mut settings = state
        .settings
        .lock()
        .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?;
    settings.server_ip = server_ip;
    settings.summoner_name = summoner_name;
    settings.import_runes = import_runes.unwrap_or(true);
    settings.import_items = import_items.unwrap_or(true);
    settings.import_summoners = import_summoners.unwrap_or(true);
    settings.flash_position = flash_position.unwrap_or_else(|| "d".to_string()).to_lowercase();
    settings.rune_option_index = rune_option_index.unwrap_or(0);
    Ok(())
}

#[tauri::command]
pub async fn get_lcu_bridge_last_applied() -> Result<Option<BridgeAppliedState>, String> {
    let state = bridge_state();
    let snapshot = state
        .last_applied
        .lock()
        .map_err(|_| "failed to acquire LCU bridge state lock".to_string())?
        .clone();
    Ok(snapshot)
}

#[tauri::command]
pub async fn get_lcu_current_summoner_name() -> Result<Option<String>, String> {
    let lockfile_path = find_lockfile_path().ok_or_else(|| "could not find a League lockfile".to_string())?;
    let connection = read_lockfile(&lockfile_path).and_then(|lockfile| build_lcu_connection(&lockfile))?;

    let summoner_name = fetch_current_summoner_name(&connection).await?;
    let trimmed = summoner_name.trim();

    if trimmed.is_empty() {
        Ok(None)
    } else {
        Ok(Some(trimmed.to_string()))
    }
}

#[tauri::command]
pub async fn retrigger_lcu_import(
    server_ip: String,
    summoner_name: String,
    import_runes: Option<bool>,
    import_items: Option<bool>,
    import_summoners: Option<bool>,
    flash_position: Option<String>,
    rune_option_index: Option<usize>,
) -> Result<String, String> {
    let state = bridge_state();

    {
        let mut settings = state
            .settings
            .lock()
            .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?;
        settings.server_ip = server_ip;
        settings.summoner_name = summoner_name;
        settings.import_runes = import_runes.unwrap_or(true);
        settings.import_items = import_items.unwrap_or(true);
        settings.import_summoners = import_summoners.unwrap_or(true);
        settings.flash_position = flash_position.unwrap_or_else(|| "d".to_string()).to_lowercase();
        settings.rune_option_index = rune_option_index.unwrap_or(0);
    }

    apply_current_selection_once(&state).await
}

#[tauri::command]
pub async fn retrigger_lcu_import_for_champion(
    server_ip: String,
    summoner_name: String,
    champion_id: String,
    position: Option<String>,
    import_runes: Option<bool>,
    import_items: Option<bool>,
    import_summoners: Option<bool>,
    flash_position: Option<String>,
    rune_option_index: Option<usize>,
) -> Result<String, String> {
    let state = bridge_state();

    {
        let mut settings = state
            .settings
            .lock()
            .map_err(|_| "failed to acquire LCU bridge settings lock".to_string())?;
        settings.server_ip = server_ip;
        settings.summoner_name = summoner_name;
        settings.import_runes = import_runes.unwrap_or(true);
        settings.import_items = import_items.unwrap_or(true);
        settings.import_summoners = import_summoners.unwrap_or(true);
        settings.flash_position = flash_position.unwrap_or_else(|| "d".to_string()).to_lowercase();
        settings.rune_option_index = rune_option_index.unwrap_or(0);
    }

    let champion_id_parsed = champion_id
        .trim()
        .parse::<u64>()
        .map_err(|_| "invalid champion_id provided for fallback import".to_string())?;

    apply_specific_champion_once(&state, champion_id_parsed, position.unwrap_or_default()).await
}
