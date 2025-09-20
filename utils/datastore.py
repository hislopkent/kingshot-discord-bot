from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Iterable, Mapping

from rapidfuzz import fuzz, process

log = logging.getLogger(__name__)

DATA_FILE_NAMES = ("heroes", "buildings", "research", "events", "aliases")


def _default_files(data_dir: Path) -> dict[str, Path]:
    return {name: data_dir / f"{name}.json" for name in DATA_FILE_NAMES}


class DataStore:
    def __init__(self, data_dir: Path | None = None):
        data_dir = data_dir or Path(__file__).resolve().parents[1] / "data"
        self._files: dict[str, Path] = _default_files(data_dir)
        self.data: dict[str, dict[str, Any]] = {name: {} for name in self._files}

    async def load_all(self) -> None:
        for name, path in self._files.items():
            self.data[name] = self._load_json(path)

    def _load_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            log.warning("Data file missing: %s", path)
            return {}
        try:
            with path.open("r", encoding="utf-8") as fp:
                loaded = json.load(fp)
        except json.JSONDecodeError as exc:
            log.error("Failed to parse %s: %s", path, exc)
            return {}
        if isinstance(loaded, Mapping):
            return dict(loaded)
        log.error("Data file %s did not contain an object at the top level", path)
        return {}

    def _alias(self, name: str) -> str:
        return self.data.get("aliases", {}).get(name, name)

    def _fuzzy_best(self, name: str, bucket: str, cutoff: int = 70) -> str | None:
        bucket_dict = self.data.get(bucket, {})
        if not bucket_dict:
            return None
        alias = self._alias(name)
        if alias in bucket_dict:
            return alias
        choices: Iterable[str] = bucket_dict.keys()
        result = process.extractOne(alias, choices, scorer=fuzz.WRatio)
        if not result:
            return None
        match, score, _ = result
        return match if score >= cutoff else None

    def _lookup(self, bucket: str, name: str) -> tuple[str, Any] | None:
        key = self._fuzzy_best(name, bucket)
        if key is None:
            return None
        bucket_dict = self.data.get(bucket, {})
        if key not in bucket_dict:
            return None
        return key, bucket_dict[key]

    def lookup_hero(self, name: str) -> tuple[str, Any] | None:
        return self._lookup("heroes", name)

    def lookup_building(self, name: str) -> tuple[str, Any] | None:
        return self._lookup("buildings", name)

    def lookup_research(self, name: str) -> tuple[str, Any] | None:
        return self._lookup("research", name)

    def lookup_event(self, name: str) -> tuple[str, Any] | None:
        return self._lookup("events", name)

    def get_hero(self, name: str) -> Any | None:
        match = self.lookup_hero(name)
        return None if match is None else match[1]

    def get_building(self, name: str) -> Any | None:
        match = self.lookup_building(name)
        return None if match is None else match[1]

    def get_research(self, name: str) -> Any | None:
        match = self.lookup_research(name)
        return None if match is None else match[1]

    def get_event(self, name: str) -> Any | None:
        match = self.lookup_event(name)
        return None if match is None else match[1]

    def list_events(self) -> list[str]:
        return sorted(self.data.get("events", {}))
