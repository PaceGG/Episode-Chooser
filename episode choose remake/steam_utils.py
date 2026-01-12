import requests
from show_images import select_image_from_urls


def get_appids_by_name(game_name):
    url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&l=en&cc=us"
    response = requests.get(url).json()
    items = [item for item in response.get("items", []) if item["type"] == "app"]
    if items:
        return [item["id"] for item in items]
    return None

def select_header_by_game_name(game_name):
    app_ids = get_appids_by_name(game_name)
    headers = [f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg" for app_id in app_ids]
    return select_image_from_urls(headers)