"""Service for loading and querying Myanmar township data."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class TownshipService:
    """Loads township data from JSON and provides lookup methods."""

    def __init__(self, data_dir: str = "data") -> None:
        """Initialize with path to data directory."""
        data_path = Path(data_dir) / "townships.json"
        with open(data_path, encoding="utf-8") as f:
            self._townships: list[dict[str, Any]] = json.load(f)
        self._index = {t["id"]: t for t in self._townships}

    def get_all(self) -> list[dict[str, Any]]:
        """Return all townships."""
        return self._townships

    def get_by_id(self, township_id: str) -> dict[str, Any] | None:
        """Return a single township by ID, or None if not found."""
        return self._index.get(township_id)

    def get_count(self) -> int:
        """Return total number of townships."""
        return len(self._townships)


@lru_cache(maxsize=1)
def get_township_service() -> TownshipService:
    """Return the singleton TownshipService instance."""
    return TownshipService()
