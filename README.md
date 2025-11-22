<<<<<<< HEAD
# adb_ctrl
Control Android tablets via ADB over WiFi - web UI &amp; CLI for media playback, volume, and YouTube playlist management
=======
# ADB Tablet Controller

Control your Android tablet via ADB over WiFi with a web interface and CLI client.

*Created by vibe coding with Claude Sonnet 4.5*

## Why This Exists

I created this project because I wanted to keep a list of YouTube videos and play them on my Android tablet. Since NewPipe doesn't support queueing videos via intents, this project manages a playlist and sends videos one at a time to the tablet.

## Quick Start

### 1. Install Dependencies

**Option A: Direct install**
```bash
pip install -r requirements.txt
```

**Option B: Using venv (recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

**Option C: Using uv (fastest)**
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install (one command!)
uv venv && uv pip install -r requirements.txt

# Run without activating
uv run server.py
uv run cli_client.py
```

### 2. Connect to Tablet
```bash
# Enable Wireless Debugging on tablet (Settings → Developer Options)
adb connect 10.0.90.22:5555
```

### 3. Start Server
```bash
python3 server.py
# Server runs on http://localhost:5000
```

### 4. Use Controls

**Web UI:**
- Open: http://localhost:5000

**CLI Client:**
```bash
# In another terminal
python3 cli_client.py
```

## Architecture

```
Server (port 5000)
├── ADB Controller
├── Playlist Manager
└── REST API
     │
     ├── Web UI (browser)
     └── CLI Client (terminal)
```

## Features

- Play/Pause, Next/Previous, Rewind/Forward
- Volume control (up/down/mute)
- Fullscreen toggle, quality settings, playback speed
- Playlist management for YouTube URLs
- Multiple clients share same state
- **Settings panel** - Configure device IP, port, and unlock PIN

## API Endpoints

- `GET /api/status` - Connection status
- `GET /api/playlist` - Get playlist
- `POST /api/play` - Play/pause
- `POST /api/playlist/next` - Next video
- `POST /api/playlist/previous` - Previous video
- `POST /api/volume/up` - Volume up
- `POST /api/volume/down` - Volume down
- `POST /api/playlist/add` - Add URL (JSON body)
- `POST /api/fullscreen` - Toggle fullscreen
- `POST /api/custom/listen` - Listen for tap and record coordinates
- `GET /api/custom/buttons` - Get all saved custom buttons
- `POST /api/custom/buttons` - Save new custom button (JSON: {name, x, y})
- `DELETE /api/custom/buttons/<name>` - Delete custom button
- `POST /api/custom/buttons/<name>/execute` - Execute saved custom button
- And more...

## CLI Commands

```bash
p         Play/Pause
n         Next video
b         Previous video
+         Volume up
-         Volume down
m         Mute
fs        Fullscreen
add       Add URL to playlist
list      Show playlist
status    Check connection
record    Record custom tap (listens for 10 seconds)
save      Save recorded tap with a name
buttons   List all saved custom buttons
exec      Execute a saved custom button
del       Delete a custom button
help      Show all commands
```

## Files

- `server.py` - API server (Flask)
- `cli_client.py` - CLI client
- `adb_controller.py` - ADB wrapper
- `playlist_manager.py` - Playlist logic
- `settings_manager.py` - Settings storage
- `index.html` - Web UI

## Requirements

- Python 3.7+
- Flask
- requests
- ADB (Android Debug Bridge)
- NewPipe app on tablet

## Tips

- Keep server running in one terminal
- Use as many CLI clients as you want
- Configure device IP and PIN in Settings panel (web UI)
- Playlist saved to `playlist.json`
- Settings saved to `settings.json`
- **Virtual environment:** If using venv, remember to activate it before running
- **With uv:** Use `uv run server.py` / `uv run cli_client.py` (no activation needed)
>>>>>>> 5f1a019 (starting off good.)
