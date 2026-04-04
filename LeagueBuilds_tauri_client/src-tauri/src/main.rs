#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod lcu_bridge;

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct BuildApiResponse {
    #[serde(rename = "championId")]
    champion_id: String,
    runes: String,
    summ: String,
    item: String,
    start_item: String,
    item_build: String,
    skill_order: String,
    position: String,
    boots: String,
    champion: String,
    #[serde(rename = "champ_winrate")]
    champ_winrate: Option<f64>,
    #[serde(rename = "champ_pickrate")]
    champ_pickrate: Option<f64>,
}

#[derive(Serialize, Deserialize)]
struct ChampionMetadata {
    name: String,
    title: String,
    blurb: String,
    image_full: String,
    spell_image_passive: String,
    spell_image_q: String,
    spell_image_w: String,
    spell_image_e: String,
    spell_image_r: String,
    spell_text_passive: String,
    spell_text_q: String,
    spell_text_w: String,
    spell_text_e: String,
    spell_text_r: String,
}

#[derive(Serialize, Deserialize)]
struct ItemMetadata {
    id: String,
    name: String,
    description: String,
    plaintext: String,
    image: String,
    gold: String,
    stats: String,
}

#[derive(Serialize, Deserialize)]
struct SummonerMetadata {
    name: String,
    description: String,
    tooltip: String,
    image: String,
    cooldown: String,
    #[serde(rename = "cooldownBurn")]
    cooldown_burn: String,
}

#[derive(Serialize, Deserialize)]
struct RuneMetadata {
    id: i32,
    name: String,
    icon: String,
    #[serde(rename = "shortDesc")]
    short_desc: String,
    #[serde(rename = "longDesc")]
    long_desc: String,
    key: String,
}

#[tauri::command]
async fn fetch_build(
    server_ip: String,
    champion_id: String,
    position: Option<String>,
    summoner_name: Option<String>,
) -> Result<BuildApiResponse, String> {
    let client = reqwest::Client::new();
    let position = position.unwrap_or_default();
    let summoner_name = summoner_name.unwrap_or_else(|| "INCOGNITO".to_string());
    let base_url = resolve_server_base_url(&server_ip)?;

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

    response
        .json::<BuildApiResponse>()
        .await
        .map_err(|error| format!("invalid build response: {error}"))
}

#[tauri::command]
async fn fetch_version(server_ip: String) -> Result<String, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(&server_ip)?;
    let endpoint = format!("{}/version", base_url);

    let response = client
        .get(&endpoint)
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("version request failed with {}", response.status()));
    }

    response
        .json::<String>()
        .await
        .map_err(|error| format!("invalid version response: {error}"))
}

#[tauri::command]
async fn fetch_champion_metadata(
    server_ip: String,
    champion_id: String,
) -> Result<ChampionMetadata, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(&server_ip)?;
    let endpoint = format!(
        "{}/metadata/champion/{}",
        base_url,
        champion_id.trim()
    );

    let response = client
        .get(&endpoint)
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("champion metadata request failed with {}", response.status()));
    }

    response
        .json::<ChampionMetadata>()
        .await
        .map_err(|error| format!("invalid champion metadata response: {error}"))
}

#[tauri::command]
async fn fetch_item_metadata(
    server_ip: String,
    item_id: String,
) -> Result<ItemMetadata, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(&server_ip)?;
    let endpoint = format!(
        "{}/metadata/item/{}",
        base_url,
        item_id.trim()
    );

    let response = client
        .get(&endpoint)
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("item metadata request failed with {}", response.status()));
    }

    response
        .json::<ItemMetadata>()
        .await
        .map_err(|error| format!("invalid item metadata response: {error}"))
}

#[tauri::command]
async fn fetch_summoner_metadata(
    server_ip: String,
    summoner_id: String,
) -> Result<SummonerMetadata, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(&server_ip)?;
    let endpoint = format!(
        "{}/metadata/summoner/{}",
        base_url,
        summoner_id.trim()
    );

    let response = client
        .get(&endpoint)
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("summoner metadata request failed with {}", response.status()));
    }

    response
        .json::<SummonerMetadata>()
        .await
        .map_err(|error| format!("invalid summoner metadata response: {error}"))
}

#[tauri::command]
async fn fetch_rune_metadata(
    server_ip: String,
    rune_id: String,
) -> Result<RuneMetadata, String> {
    let client = reqwest::Client::new();
    let base_url = resolve_server_base_url(&server_ip)?;
    let endpoint = format!(
        "{}/metadata/rune/{}",
        base_url,
        rune_id.trim()
    );

    let response = client
        .get(&endpoint)
        .send()
        .await
        .map_err(|error| format!("request failed: {error}"))?;

    if !response.status().is_success() {
        return Err(format!("rune metadata request failed with {}", response.status()));
    }

    response
        .json::<RuneMetadata>()
        .await
        .map_err(|error| format!("invalid rune metadata response: {error}"))
}

#[tauri::command]
async fn open_external_url(url: String) -> Result<(), String> {
    let trimmed = url.trim();
    if !(trimmed.starts_with("http://") || trimmed.starts_with("https://")) {
        return Err("only http/https URLs are supported".to_string());
    }

    webbrowser::open(trimmed)
        .map(|_| ())
        .map_err(|error| format!("failed to open external URL: {error}"))
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

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            lcu_bridge::start_lcu_bridge,
            lcu_bridge::update_lcu_bridge_settings,
            lcu_bridge::get_lcu_bridge_last_applied,
            lcu_bridge::get_lcu_current_summoner_name,
            lcu_bridge::retrigger_lcu_import,
            lcu_bridge::retrigger_lcu_import_for_champion,
            fetch_build,
            fetch_version,
            open_external_url,
            fetch_champion_metadata,
            fetch_item_metadata,
            fetch_summoner_metadata,
            fetch_rune_metadata
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

