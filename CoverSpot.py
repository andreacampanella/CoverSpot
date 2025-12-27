import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import requests
from io import BytesIO
import time

APP_NAME = "CoverSpot"
CONFIG_DIR = os.path.expanduser(f"~/.config/{APP_NAME}")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CACHE_FILE = os.path.join(CONFIG_DIR, "token_cache")

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_config(client_id, client_secret):
    ensure_config_dir()
    config = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # Secure the file
    print(f"Config saved to {CONFIG_FILE}")

def setup_credentials():
    print(f"\n{'='*50}")
    print(f"  {APP_NAME} - First Time Setup")
    print(f"{'='*50}\n")
    print("You'll need to create a Spotify Developer App:")
    print("1. Go to https://developer.spotify.com/dashboard")
    print("2. Create a new app")
    print("3. Add this redirect URI: http://127.0.0.1:8888/callback")
    print()
    
    client_id = input("Enter your Client ID: ").strip()
    client_secret = input("Enter your Client Secret: ").strip()
    
    save_config(client_id, client_secret)
    return client_id, client_secret

def authenticate(client_id, client_secret):
    ensure_config_dir()
    
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-currently-playing user-read-playback-state",
        cache_path=CACHE_FILE,
        open_browser=False
    )
    
    # Check if we have a valid cached token
    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        print(f"\n{'='*50}")
        print(f"  {APP_NAME} - Spotify Authorization")
        print(f"{'='*50}\n")
        
        auth_url = sp_oauth.get_authorize_url()
        print("Open this URL in a browser:\n")
        print(auth_url)
        print("\nAfter logging in, you'll get an error page - that's OK!")
        print("Copy the ENTIRE URL from the address bar.\n")
        
        response_url = input("Paste URL here: ").strip()
        code = sp_oauth.parse_response_code(response_url)
        sp_oauth.get_access_token(code)
        print("\n✓ Authorization successful!\n")
    
    return spotipy.Spotify(auth_manager=sp_oauth)

def get_album_art(sp):
    try:
        current = sp.current_playback()
        if current and current.get('item'):
            images = current['item']['album']['images']
            if images:
                return images[0]['url']
    except Exception as e:
        print(f"Error fetching playback: {e}")
    return None

def display_image(screen, url):
    try:
        response = requests.get(url)
        image = pygame.image.load(BytesIO(response.content))
        
        screen_w, screen_h = screen.get_size()
        img_w, img_h = image.get_size()
        scale = min(screen_w / img_w, screen_h / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        image = pygame.transform.smoothscale(image, new_size)
        
        x = (screen_w - new_size[0]) // 2
        y = (screen_h - new_size[1]) // 2
        
        screen.fill((0, 0, 0))
        screen.blit(image, (x, y))
        pygame.display.flip()
    except Exception as e:
        print(f"Error displaying image: {e}")

def main():
    # Load or create config
    config = load_config()
    if config:
        client_id = config['client_id']
        client_secret = config['client_secret']
    else:
        client_id, client_secret = setup_credentials()
    
    # Authenticate with Spotify
    sp = authenticate(client_id, client_secret)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(APP_NAME)
    pygame.mouse.set_visible(False)
    
    print(f"{APP_NAME} is running. Press ESC to quit.")
    
    current_image_url = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        image_url = get_album_art(sp)
        
        if image_url and image_url != current_image_url:
            current_image_url = image_url
            display_image(screen, image_url)
        elif not image_url and current_image_url is not None:
            screen.fill((0, 0, 0))
            pygame.display.flip()
            current_image_url = None
        
        time.sleep(2)
    
    pygame.quit()
    print("Goodbye!")

if __name__ == "__main__":
    main()