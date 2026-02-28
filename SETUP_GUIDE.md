Vortexi Repository Setup Guide
================================

This repository contains a Roblox-like game server ecosystem with multiple interconnected components.

Repository Structure Overview
-----------------------------

vortexi-src/
├── vortexiwebsite/          # Flask backend & website
├── vortexigameserver/       # Python RCC wrapper (Windows-only)
├── vortexibootstrap2/       # Rust bootstrapper client
├── vortexidiscordbot/       # Discord bot integration
├── Clients/                 # Historical Roblox clients (2016, 2018)
├── FFlags/                  # Feature flags for different versions
├── SETUP_GUIDE.md           # Official setup documentation
└── readme.md                # Main readme

1. BACKEND & WEBSITE SETUP (vortexiwebsite)
-------------------------------------------

Directory Structure
```
vortexiwebsite/
├── app/
│   ├── __init__.py                  # Flask app initialization
│   ├── build_version.py             # Version info
│   ├── extensions.py                # Flask extensions (DB, Redis, etc.)
│   ├── shell_commands.py            # CLI commands for admin setup
│   ├── models/                      # SQLAlchemy database models
│   ├── routes/                      # API blueprints
│   ├── pages/                       # Website pages & Jinja2 templates
│   ├── services/                    # Business logic (economy, membership, etc.)
│   ├── static/                      # Frontend assets (CSS, JS, images)
│   ├── util/                        # Authentication, S3, signing utilities
│   ├── enums/                       # Enumeration definitions
│   └── files/                       # Server-side file storage (keys, scripts)
├── config.py                        # Configuration file
├── requirements.txt                 # Python dependencies
├── README.md                        # Backend setup instructions
├── start.sh                         # Production startup script
├── debug.sh                         # Development startup script
├── tools/                           # Utility scripts (RSA key generation)
└── logs/                            # Log directory
```

Prerequisites
- Python 3.12+
- PostgreSQL (database)
- Redis (sessions, scheduling, rate limiting)
- FFmpeg (asset processing)

Installation Steps

Step 1: Install Dependencies

```bash
pip install -r vortexiwebsite/requirements.txt
```

Step 2: Generate RSA Keys

```bash
cd vortexiwebsite/tools
python3 generate_new_keys.py
```

Private keys → `vortexiwebsite/app/files/`
Public keys → `vortexigameserver/`

Step 3: Configure Environment

Edit `vortexiwebsite/config.py`:

```py
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/vortexi"
FLASK_LIMITED_STORAGE_URI = "redis://localhost:6379"
BaseDomain = "yourdomain.com"  # e.g., kronus.co
USE_LOCAL_STORAGE = True  # For development (bypasses S3)
```

Step 4: Initialize Database

```bash
export FLASK_APP=app
cd vortexiwebsite
flask shell
>>> db.create_all()
>>> from app.shell_commands import create_admin_user
>>> create_admin_user()
```

Key Files & Their Purpose
- `app/__init__.py`: Flask app initialization, route registration
- `app/extensions.py`: Database, Redis, APScheduler, rate limiting setup
- `app/models/`: User, game, economy models (SQLAlchemy)
- `app/routes/`: API endpoints (presence, marketplace, gameservers)
- `app/pages/`: Website UI (login, home, profile pages)
- `app/services/`: Economy logic, membership handling
- `app/util/`: Authentication helpers, S3 integration, RSA signing
- `app/static/css/global.css`: Main stylesheet
- `config.py`: Database, Redis, domain configuration

2. GAMESERVER SETUP (vortexigameserver)
-------------------------------------

Directory Structure
```
vortexigameserver/
├── main.py                          # Main server entry point
├── config.py                        # Configuration file
├── ProcessController.py             # Manages RCC processes
├── ClientController.py              # Handles client communication
├── SOAPFormats.py                   # SOAP protocol formatting
├── UDPProxy.py                      # UDP proxy for game traffic
├── requirements.txt                 # Python dependencies
├── rsa_public_gameserver.pub        # Public key for request verification
├── gameserver.txt                   # Gameserver configuration
├── quilkin.exe                      # Game proxy executable
├── TeeShirtTemplate.png             # T-shirt rendering template
├── Player2014/                      # 2014 player character files
├── RCCService/                      # 2014/2016 RCC binary container
├── RCCService2018/
├── RCCService2020/
├── RCCService2021/
├── Scripts/                         # Lua injection scripts
└── readme.md
```

Setup (Windows-only)

Step 1: Set Registry Access Key

Create a `.reg` file with the provided keys and import it into Windows Registry. The server expects `AccessKey` and `SettingsKey` under Roblox registry locations.

Step 2: Patch RCC Binaries

Replace all hardcoded domain strings in RCC binaries (e.g., `kronus.co`, `kronus.co`, `kronus.co`) with your domain.

Step 3: Configure Gameserver

Edit `vortexigameserver/config.py` to match domain, ports, and RCC service paths.

Step 4: Run Gameserver

```bash
python main.py
```

Key Files & Purpose
- `main.py`: Main loop, RCC process management
- `ProcessController.py`: Spawns/monitors RCC processes
- `ClientController.py`: Handles client/backend requests
- `SOAPFormats.py`: SOAP message formatting
- `UDPProxy.py`: Game traffic proxying
- `rsa_public_gameserver.pub`: Verifies backend signatures
- `RCCService*/`: RCC binaries for different versions

3. BOOTSTRAPPER SETUP (vortexibootstrap2)
--------------------------------------

Directory Structure
```
vortexibootstrap2/
├── src/                             # Rust source code
│   └── main.rs                      # Contains hardcoded domain strings
├── Cargo.toml
├── build.rs
├── assets/
├── tools/
├── win-build-release.bat
└── readme.md
```

Build Instructions

For Windows:
```bash
cd vortexibootstrap2
win-build-release.bat
```

For Linux:
```bash
cd vortexibootstrap2
cargo build --release
```

Before building, update `src/main.rs` and remove/replace any hardcoded domain strings with your domain.

Output
- Release binary: `target/release/vortexibootstrap2.exe` (Windows) or `target/release/vortexibootstrap2` (Linux)

4. DISCORD BOT SETUP (vortexidiscordbot)
---------------------------------------

Directory Structure
```
vortexidiscordbot/
├── main.py                          # Discord bot entry point
└── README.md
```

Setup
```bash
pip install -r vortexidiscordbot/requirements.txt  # or pip install discord.py
```

Edit `main.py` and set your bot token:

```py
bot.run("YOUR_DISCORD_BOT_TOKEN")
```

Run:
```bash
python main.py
```

5. CLIENT VERSIONS (Clients/)
-----------------------------

Historical Roblox client versions are available under `Clients/2016/` and `Clients/2018/` for compatibility testing.

6. FEATURE FLAGS (FFlags/)
-------------------------

Files under `FFlags/` provide JSON feature flag sets for different client versions. Example files include `2016_RCCService.json`, `2018_RCCService.json`, `2020RCCService.json`, etc.

Quick Start Summary
-------------------

For First-Time Setup:

Backend:
```bash
pip install -r vortexiwebsite/requirements.txt
cd vortexiwebsite/tools && python3 generate_new_keys.py
cd .. && flask shell && db.create_all()
```

Configure:
- Edit `vortexiwebsite/config.py` (DB, Redis, domain)
- Edit `vortexigameserver/config.py`
- Update domain strings in `vortexibootstrap2/src/main.rs`

Build Bootstrapper:
```bash
cd vortexibootstrap2 && cargo build --release
```

Set Registry (Windows Gameserver):
- Import the `.reg` file with your access key
- Patch RCC binaries with your domain

Run Components:
```bash
# Terminal 1: Backend
cd vortexiwebsite && ./start.sh

# Terminal 2: Gameserver (Windows only)
cd vortexigameserver && python main.py

# Terminal 3: Discord Bot (optional)
cd vortexidiscordbot && python main.py
```

Important Notes
- Thumbnail Rendering: Handled by gameserver using `TeeShirtTemplate.png` and screenshot utilities
- RSA Key Exchange: Critical for backend-gameserver communication security
- Domain Hardcoding: Remember to update all domain references before deployment
- Windows Requirement: Gameserver only runs on Windows due to RCC binary availability
- Local Storage: Set `USE_LOCAL_STORAGE=True` in development to avoid S3 dependency

Architecture & Reference
------------------------

The repository contains detailed implementations for:
- Database models and schema (`app/models/`)
- Authentication system and token negotiation (`app/routes/authentication.py`, `app/util/auth.py`)
- Complete game join flow (`app/routes/gamejoin.py`)
- Cryptographic utilities and key generation (`tools/generate_new_keys.py`, `app/util/signscript.py`)
- Game server (RCC) communication and SOAP formats (`vortexigameserver/SOAPFormats.py`, `ProcessController.py`)
- Thumbnail rendering scripts and job submission (`vortexigameserver` internalscripts)
- Place server management and player verification (client-side scripts in `app/files/`)

For complete, line-level references and deeper explanations, see the source files under `vortexiwebsite/`, `vortexigameserver/`, and `vortexibootstrap2/`.

If you'd like, I can:
- Add environment examples (`.env.example`) for the backend and gameserver
- Create a small script to replace hardcoded domain strings across the repo
- Run a quick verification that `vortexiwebsite` starts in a dev container (if you want me to run it)

---
Generated and added to repository by project assistant.
