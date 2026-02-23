##API_KEY = "0bZ0W6cxl0unmT5XjUrxL7X50HprqK8U0es3AGJr"



from flask import Flask, jsonify, render_template, request
import requests
import json
import os


app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

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

FAVOURITES_FILE = "favourites.json"
CACHE_FILE = "animal_cache.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_favourites():
    if os.path.exists(FAVOURITES_FILE):
        with open(FAVOURITES_FILE, "r") as f:
            return json.load(f)
    return []

def save_favourites(favourites):
    with open(FAVOURITES_FILE, "w") as f:
        json.dump(favourites, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/animal/<name>")
def get_animal(name):
    # Check cache first
    cache = load_json(CACHE_FILE)
    if name in cache:
        print(f"Loaded {name} from cache")
        return jsonify(cache[name])

    # Not in cache, fetch from API
    print(f"Fetching {name} from API")
    response = requests.get(
        "https://api.api-ninjas.com/v1/animals",
        params={"name": name},
        headers={"X-Api-Key": API_KEY}
    )
    data = response.json()
    if data:
        animal = data[0]
        result = {
            "name": animal["name"],
            "location": animal.get("locations", ["Unknown"]),
            "habitat": animal["characteristics"].get("habitat", "Unknown"),
            "diet": animal["characteristics"].get("diet", "Unknown"),
            "slogan": animal["characteristics"].get("slogan", ""),
            "lifespan": animal["characteristics"].get("lifespan", "Unknown"),
            "name_of_young": animal("characteristics").get("name_of_young","Unknown"),
        }
        # Save to cache
        cache[name] = result
        save_json(CACHE_FILE, cache)
        return jsonify(result)

    return jsonify({"error": "Animal not found"})

@app.route("/animals")
def animal_list():
    return jsonify(ANIMALS)

@app.route("/favourites", methods=["GET"])
def get_favourites():
    return jsonify(load_favourites())

@app.route("/favourites", methods=["POST"])
def add_favourite():
    animal = request.json
    favourites = load_favourites()
    if not any(f["name"] == animal["name"] for f in favourites):
        favourites.append(animal)
        save_favourites(favourites)
        return jsonify({"message": "Saved!"})
    return jsonify({"message": "Already saved!"})

@app.route("/favourites/<name>", methods=["DELETE"])
def remove_favourite(name):
    favourites = load_favourites()
    favourites = [f for f in favourites if f["name"] != name]
    save_favourites(favourites)
    return jsonify({"message": "Removed!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)