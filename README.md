# CoverSpot

A simple Raspberry Pi application that displays the album art of your currently playing Spotify track in fullscreen.

## Requirements

- Raspberry Pi with a display (or any Linux machine)
- Python 3
- A Spotify account
- A Spotify Developer App

## Installation

1. Install system dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-pygame
```

2. Install Python dependencies:
```bash
pip3 install spotipy requests pillow
```

3. Download the script:
```bash
wget https://raw.githubusercontent.com/yourusername/coverspot/main/coverspot.py
```

## Spotify Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. In your app settings, add this redirect URI:
```
   http://127.0.0.1:8888/callback
```
4. Note your Client ID and Client Secret

## Usage

Run the application:
```bash
python3 coverspot.py
```

On first run, you will be prompted to enter your Spotify Client ID and Client Secret. These are saved to `~/.config/CoverSpot/config.json`.

You will then be given a URL to open in any browser. After logging in to Spotify, you will be redirected to a page that fails to load. This is expected. Copy the entire URL from your browser address bar and paste it into the terminal.

Once authenticated, the application will display album art for whatever is playing on your Spotify account.

Press ESC to exit.

## Configuration

All configuration is stored in `~/.config/CoverSpot/`:

- `config.json` - Your Spotify API credentials
- `token_cache` - Your authentication token

To reset the application, remove the config directory:
```bash
rm -rf ~/.config/CoverSpot
```

## Autostart on Boot

To run CoverSpot automatically when your Raspberry Pi boots, add it to your autostart:
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/coverspot.desktop << EOF
[Desktop Entry]
Type=Application
Name=CoverSpot
Exec=python3 /path/to/coverspot.py
EOF
```

Replace `/path/to/coverspot.py` with the actual path to the script.

## License

MIT