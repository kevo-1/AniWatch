import json

def GetClientID():
    with open("D:/Projects/AniWatch/Utilities/config.json", "r") as f:
        config = json.load(f)
    return config.get("client_id", "")