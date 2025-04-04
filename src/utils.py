import json

def load_geojson(path):
    """Load a GeoJSON file from disk."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_geojson(data, path):
    """Save data to a GeoJSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)