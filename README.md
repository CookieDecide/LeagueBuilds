# LeagueBuilds

LeagueBuilds provides League of Legends build recommendations (runes, items, summoner spells, skill order) through a Python backend and desktop clients.

Current stable versions:
- Client: `V0.7.7`
- Server: `V0.7.7`

## Repository Layout

- `LeagueBuilds_tauri_client/` - Main desktop client (Tauri + React + TypeScript)
- `LeagueBuilds_server/` - Backend API and data update/sorting pipeline (Python)
- `LeagueBuilds_client/` - Legacy Python desktop client (still present)

## Current Production Stack

- Desktop app: Tauri (`LeagueBuilds_tauri_client`)
- Backend: Flask/Flask-RESTful + Waitress (`LeagueBuilds_server`)
- Recommended public backend URL default in Tauri client: `https://leaguebuilds.hopto.org`

## Quick Start (Tauri Client + Local/Remote Server)

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
