import json
from pathlib import Path
from rapidfuzz import process, fuzz

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FILES = {
    "heroes": DATA_DIR / "heroes.json",
    "buildings": DATA_DIR / "buildings.json",
    "research": DATA_DIR / "research.json",
    "events": DATA_DIR / "events.json",
    "aliases": DATA_DIR / "aliases.json",
}

class DataStore:
    def __init__(self):
        self.data = {k: {} for k in FILES}

    async def load_all(self):
        for name, path in FILES.items():
            self.data[name] = self._load_json(path)

    def _load_json(self, path: Path):
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _alias(self, name: str) -> str:
        return self.data.get("aliases", {}).get(name, name)

    def _fuzzy_best(self, name: str, bucket: str, cutoff: int = 70):
        bucket_dict = self.data.get(bucket, {})
        if not bucket_dict:
            return None
        choices = list(bucket_dict.keys())
        alias = self._alias(name)
        if alias in bucket_dict:
            return alias
        res = process.extractOne(alias, choices, scorer=fuzz.WRatio)
        if not res:
            return None
        match, score, _ = res
        return match if score >= cutoff else None

    def get_hero(self, name): key = self._fuzzy_best(name, "heroes"); return None if key is None else self.data["heroes"][key]
    def get_building(self, name): key = self._fuzzy_best(name, "buildings"); return None if key is None else self.data["buildings"][key]
    def get_research(self, name): key = self._fuzzy_best(name, "research"); return None if key is None else self.data["research"][key]
    def get_event(self, name): key = self._fuzzy_best(name, "events"); return None if key is None else self.data["events"][key]
    def list_events(self): return self.data.get("events", {}).keys()
