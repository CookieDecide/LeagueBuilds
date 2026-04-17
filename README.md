# LeagueBuilds

LeagueBuilds provides League of Legends build recommendations (runes, items, summoner spells, skill order) through a Python backend and desktop clients.

## Normal use case (recommended)

The public LeagueBuilds server is hosted and maintained by the project owner.

If you only want to use LeagueBuilds:

1. Go to the GitHub Releases page.
2. Download the latest Windows client release asset.
3. Start the client and use it directly with the hosted backend.

Release downloads:
- https://github.com/CookieDecide/LeagueBuilds/releases

You do not need to run the server or provide your own Riot API key for this normal user flow.

## Advanced use only

The following sections are only relevant if you want to:

- build your own client binary
- run your own server instance
- use your own Riot API key

## Repository Layout

- `LeagueBuilds_tauri_client/` - Main desktop client (Tauri + React + TypeScript)
- `LeagueBuilds_server/` - Backend API and data update/sorting pipeline (Python)
- `LeagueBuilds_client/` - Legacy Python desktop client (still present)

## Current Production Stack

- Desktop app: Tauri (`LeagueBuilds_tauri_client`)
- Backend: Flask/Flask-RESTful + Waitress (`LeagueBuilds_server`)
- Recommended public backend URL default in Tauri client: `https://leaguebuilds.hopto.org`

## How LeagueBuilds works

### Server responsibilities

The server continuously builds and refreshes recommendation data, then exposes it through a REST API.

Core server flow:

1. Query Riot data sources for master+ player match data.
2. Pull recent games for relevant players.
3. Keep only games from the current patch for build generation.
4. Sort and score builds, including timeline-based evaluation of decisions across the match.
5. Calculate aggregate metrics such as winrate and pickrate.
6. Persist processed data in local SQLite databases via Peewee models.
7. Serve build and version data through REST endpoints consumed by clients.

Main server technologies:

- Flask + Flask-RESTful API layer
- Waitress production WSGI server
- Peewee ORM
- SQLite databases for statics, dynamics, builds, and logs

### Client responsibilities

The client is a desktop app that fetches and displays prepared builds, and can apply them to the League client.

Core client flow:

1. Provide a standalone build viewer UI for champion builds.
2. Query the LeagueBuilds REST API for build and version information.
3. Render build details in the GUI (runes, summoners, items, skill order, stats).
4. Use an LCU bridge to communicate with the local League Client when import actions are requested.
5. Support normal standalone browsing even without active LCU import usage.

Main client technologies:

- Tauri desktop shell
- React + TypeScript frontend GUI
- REST API integration with hosted LeagueBuilds server
- LCU bridge for optional in-client import actions

## Self-hosting and local development

### 1. Run backend server

```bash
cd LeagueBuilds_server
pip install -r requirements.txt
cd src
python main_server.py
```

### 2. Run Tauri client in development

```bash
cd LeagueBuilds_tauri_client
npm install
npm run tauri dev
```

### 3. Build Tauri release

```bash
cd LeagueBuilds_tauri_client
npm run tauri build
```

Release outputs are generated under:
- `LeagueBuilds_tauri_client/src-tauri/target/release/bundle/msi/`
- `LeagueBuilds_tauri_client/src-tauri/target/release/bundle/nsis/`

## Server Notes

- Server runs in production via Waitress by default.
- Reverse proxy setups (for example Nginx) are supported.
- Forwarded client IP logging is enabled when proxied through a trusted local reverse proxy.

For Ubuntu auto-update/deploy scripts, see:
- `LeagueBuilds_server/deploy/README.md`

## Privacy

- Privacy policy: `PRIVACY.md`

## Code signing policy

Free code signing provided by SignPath.io, certificate by SignPath Foundation.

Project roles:
- Committers and reviewers: CookieDecide
- Approvers: CookieDecide

Signing rules:
- Only release artifacts built from this repository are signed.
- Only binaries produced by the LeagueBuilds build pipeline are included in signed packages.
- Version numbers must match across all signed binaries in a release.
- Third-party libraries may be included as unsigned upstream components when required by the package format.

Privacy policy:
- See [PRIVACY.md](PRIVACY.md)

Release page snippet:

Free code signing provided by SignPath.io, certificate by SignPath Foundation.
Privacy policy: [PRIVACY.md](PRIVACY.md)
Project roles:
- Committers and reviewers: CookieDecide
- Approvers: CookieDecide

## Legacy Client

`LeagueBuilds_client` is the older Python desktop client. The Tauri client is the current primary desktop app.

## Feedback / Help

- Discord: https://discord.gg/MPFR7NpDaC
- Issues: https://github.com/CookieDecide/LeagueBuilds/issues
