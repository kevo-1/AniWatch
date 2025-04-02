import json
import os
import sys
from pathlib import Path

def resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent.parent
    
    return base_path / relative_path

def GetClientID():
    if "DISCORD_CLIENT_ID" in os.environ:
        return os.environ["DISCORD_CLIENT_ID"]
    
    config_locations = [
        resource_path("config.json"),          
        resource_path("Utilities/config.json"), 
        Path("config.json"),                    
        Path.home() / ".aniwatch_config.json"   
    ]
    
    for config_path in config_locations:
        try:
            with open(config_path, "r", encoding='utf-8') as f:
                config = json.load(f)
                if client_id := config.get("DISCORD_CLIENT_ID") or config.get("client_id"):
                    return client_id
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    
    return os.getenv("DISCORD_CLIENT_ID", "")