import requests
import json
import os

API_KEY = "0bZ0W6cxl0unmT5XjUrxL7X50HprqK8U0es3AGJr"


ANIMALS = [
    "elephant", "lion", "giraffe", "penguin", "dolphin",
    "tiger", "koala", "panda", "cheetah", "gorilla",
    "zebra", "hippo", "crocodile", "kangaroo", "flamingo",
    "wolf", "bear", "fox", "owl", "eagle",
    "shark", "whale", "octopus", "jellyfish", "seahorse",
    "parrot", "toucan", "peacock", "hedgehog", "otter",
    "chimpanzee", "orangutan", "lemur", "meerkat", "wombat",
    "jaguar", "leopard", "lynx", "hyena", "rhinoceros",
    "camel", "llama", "bison", "moose", "reindeer"
]

CACHE_FILE = "animal_cache.json"

def fetch_animal(name):
    response = requests.get(
        "https://api.api-ninjas.com/v1/animals",
        params={"name": name},
        headers={"X-Api-Key": API_KEY}
    )
    data = response.json()
    if data:
        animal = data[0]
        return {
            "name": animal["name"],
            "location": animal.get("locations", ["Unknown"]),
            "habitat": animal["characteristics"].get("habitat", "Unknown"),
            "diet": animal["characteristics"].get("diet", "Unknown"),
            "slogan": animal["characteristics"].get("slogan", ""),
            "lifespan": animal["characteristics"].get("lifespan", "Unknown"),
            "name_of_young": animal["characteristics"].get("name_of_young", "Unknown"),
        }
    return None

# Load existing cache so we don't re-fetch things we already have
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

print(f"Starting preload - {len(ANIMALS)} animals to check...\n")

for name in ANIMALS:
    if name in cache:
        print(f"✓ {name} already cached, skipping")
    else:
        print(f"Fetching {name}...")
        result = fetch_animal(name)
        if result:
            cache[name] = result
            print(f"✓ {name} saved")
        else:
            print(f"✗ {name} not found")

with open(CACHE_FILE, "w") as f:
    json.dump(cache, f)

print(f"\nDone! {len(cache)} animals in cache.")