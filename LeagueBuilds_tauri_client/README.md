# LeagueBuilds Tauri Client

Current version: `1.0.0`

LeagueBuilds Tauri Client is the primary desktop app for LeagueBuilds. It uses:

- Tauri (Rust shell for native desktop packaging)
- React + TypeScript (frontend UI)
- Existing Python backend REST API

## Backend API compatibility

The app uses the backend endpoints:

- `GET <server-base-url>/builds_v1/<championId>/<position?>`
- `GET <server-base-url>/version`

`<server-base-url>` can be either:
- full URL (recommended), for example `https://leaguebuilds.hopto.org`
- host-only fallback, for example `leaguebuilds.hopto.org` (auto-expanded internally)

The client sends a `Summoner` header during build fetches.

## Features

- Fetch builds by champion name or champion ID
- Live champion suggestions while typing (name and ID-aware ranking)
- Optional LCU import/retrigger flow for runes, items, and summoners
- F10 hidden mode for advanced controls
- Server URL and settings persistence with migration for legacy defaults
- Version check and release-page handoff when client is outdated
- Desktop bundles for Windows via MSI and NSIS

## Setup

1. Install prerequisites:
   - Node.js 20+
   - Rust stable toolchain
   - Tauri prerequisites for your OS: https://tauri.app/start/prerequisites/
2. Install dependencies:

```bash
npm install
```

3. Run in development mode:

```bash
npm run tauri dev
```

4. Build desktop bundle:

```bash
npm run tauri build
```

## Release builds

### Windows release build (.exe, .msi, .nsis)

1. Open PowerShell in this folder:

   `<repo-root>/LeagueBuilds_tauri_client`

2. Install dependencies (required when local Tauri CLI is missing):

   npm ci

3. Build release bundles:

   npm run tauri build

4. Output files are generated under:

   - `src-tauri/target/release/leaguebuilds_tauri_client.exe`
   - `src-tauri/target/release/bundle/msi/LeagueBuilds Desktop_<version>_x64_en-US.msi`
   - `src-tauri/target/release/bundle/nsis/LeagueBuilds Desktop_<version>_x64-setup.exe`

### Linux release build from WSL (AppImage/deb/rpm)

Use Ubuntu in WSL and run from this project directory.

Example:

`/path/to/LeagueBuilds/LeagueBuilds_tauri_client`

1. Install system prerequisites (one-time):

   sudo apt update
   sudo apt install -y build-essential pkg-config file patchelf libssl-dev \
     libgtk-3-dev libwebkit2gtk-4.1-dev libayatana-appindicator3-dev librsvg2-dev \
     gcc g++ gcc-x86-64-linux-gnu g++-x86-64-linux-gnu

2. Ensure modern Node.js (recommended: 20.x):

   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs

3. Ensure Rust is installed and Linux host toolchain is active:

   curl https://sh.rustup.rs -sSf | sh -s -- -y
   source "$HOME/.cargo/env"
   rustup default stable
   rustup target add x86_64-unknown-linux-gnu

4. Avoid permission issues on mounted Windows drive by moving Cargo target dir to Linux filesystem:

   mkdir -p "$HOME/.cache/leaguebuilds-target"
   export CARGO_TARGET_DIR="$HOME/.cache/leaguebuilds-target"

5. Install JS dependencies and build:

   npm ci
   npm run tauri build -- --bundles appimage

   Optional all Linux bundles:

   npm run tauri build -- --bundles deb,rpm,appimage

6. Output files:

   - `src-tauri/target/release/bundle/appimage/`
   - `src-tauri/target/release/bundle/deb/`
   - `src-tauri/target/release/bundle/rpm/`

### Linux runtime notes (WSL)

If AppImage starts but prints D-Bus or audio sink warnings in WSL, install runtime packages and launch via dbus-run-session:

   sudo apt install -y dbus-x11 gstreamer1.0-tools gstreamer1.0-plugins-base \
     gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
     gstreamer1.0-libav gstreamer1.0-alsa libasound2-plugins

   dbus-run-session -- ./LeagueBuilds\ Desktop_<version>_amd64.AppImage

### Common build issues

- Error: "tauri command not found" on Windows
  - Fix: run npm ci in LeagueBuilds_tauri_client and retry.

- Error: "invalid value 'appimage' for --bundles [possible values: msi, nsis]"
  - Cause: Windows Tauri CLI is being used.
  - Fix: run build from Linux environment (WSL/Docker) with Linux Node/Rust toolchain.

- Error: "SyntaxError: Unexpected token '.'" in node_modules/@tauri-apps/cli/tauri.js
  - Cause: Node version too old.
  - Fix: upgrade Node to 20+, remove node_modules, run npm ci again.

- Error: "failed to write ... Permission denied (os error 13)" under /mnt/<drive>
  - Fix: set CARGO_TARGET_DIR to a Linux path (example above).

- Error: "failed to find tool x86_64-linux-gnu-gcc"
  - Fix: install gcc-x86-64-linux-gnu and ensure /usr/bin/x86_64-linux-gnu-gcc exists.

## Project structure

- `src/` React frontend
- `src-tauri/` Tauri Rust shell and app config
