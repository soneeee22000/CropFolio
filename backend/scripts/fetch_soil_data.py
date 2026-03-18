"""One-time script to fetch soil data from ISRIC SoilGrids for all townships.

Usage:
    python -m scripts.fetch_soil_data

This queries the SoilGrids v2.0 REST API for soil properties at each township's
coordinates and writes results to backend/data/soil_profiles.json.

Rate limit: SoilGrids allows ~5 requests/second for unauthenticated users.
We add a 0.5s delay between requests to be respectful.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import httpx

# Add parent to path so we can import app modules
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
PROPERTIES = ["phh2o", "nitrogen", "soc", "clay", "sand", "silt", "cec"]
DEPTH = "0-30cm"
VALUE = "Q0.5"
TIMEOUT = 30.0
DELAY_SECONDS = 0.5

DATA_DIR = ROOT / "data"
TOWNSHIPS_PATH = DATA_DIR / "townships.json"
OUTPUT_PATH = DATA_DIR / "soil_profiles.json"


def classify_texture(clay: int, sand: int, silt: int) -> str:
    """Classify soil texture using simplified USDA triangle."""
    if clay >= 40:
        return "clay"
    if clay >= 35 and sand < 45:
        return "silty_clay" if silt >= 40 else "clay"
    if clay >= 27:
        return "silty_clay_loam" if silt >= 40 else "clay_loam"
    if sand >= 70:
        return "sandy_loam" if clay >= 10 else "sand"
    if silt >= 50:
        return "silt_loam"
    return "loam"


def rate_fertility(nitrogen: float, soc: float, cec: float) -> str:
    """Rate overall soil fertility."""
    score = 0
    if nitrogen >= 1.5:
        score += 2
    elif nitrogen >= 1.0:
        score += 1
    if soc >= 15.0:
        score += 2
    elif soc >= 8.0:
        score += 1
    if cec >= 20.0:
        score += 2
    elif cec >= 12.0:
        score += 1
    if score >= 5:
        return "high"
    if score >= 4:
        return "moderate_high"
    if score >= 2:
        return "moderate"
    if score >= 1:
        return "low"
    return "very_low"


def fetch_soil(lat: float, lon: float) -> dict | None:
    """Fetch soil properties from SoilGrids API."""
    params = {
        "lon": lon,
        "lat": lat,
        "property": PROPERTIES,
        "depth": DEPTH,
        "value": VALUE,
    }
    try:
        resp = httpx.get(SOILGRIDS_URL, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return extract_properties(data)
    except (httpx.HTTPError, KeyError, ValueError) as e:
        print(f"  ERROR: {e}")
        return None


def extract_properties(data: dict) -> dict:
    """Extract and convert SoilGrids response to our format."""
    raw: dict[str, float] = {}
    for layer in data.get("properties", {}).get("layers", []):
        name = layer.get("name", "")
        for depth in layer.get("depths", []):
            if depth.get("label") == DEPTH:
                val = depth.get("values", {}).get(VALUE)
                if val is not None:
                    raw[name] = val

    result = {
        "ph_h2o": round(raw.get("phh2o", 65) / 10.0, 1),
        "nitrogen_g_per_kg": round(raw.get("nitrogen", 100) / 100.0, 1),
        "soc_g_per_kg": round(raw.get("soc", 100) / 10.0, 1),
        "clay_pct": int(raw.get("clay", 250) / 10),
        "sand_pct": int(raw.get("sand", 350) / 10),
        "silt_pct": int(raw.get("silt", 400) / 10),
        "cec_cmol_per_kg": round(raw.get("cec", 150) / 10.0, 1),
    }
    result["texture_class"] = classify_texture(
        result["clay_pct"], result["sand_pct"], result["silt_pct"]
    )
    result["fertility_rating"] = rate_fertility(
        result["nitrogen_g_per_kg"],
        result["soc_g_per_kg"],
        result["cec_cmol_per_kg"],
    )
    return result


def main() -> None:
    """Fetch soil data for all townships and save to JSON."""
    with open(TOWNSHIPS_PATH, encoding="utf-8") as f:
        townships = json.load(f)

    print(f"Fetching soil data for {len(townships)} townships...")

    results: dict = {
        "_metadata": {
            "description": "Soil properties for Myanmar townships at 0-30cm depth",
            "source": "ISRIC SoilGrids v2.0 (https://soilgrids.org)",
            "parameters": {
                "ph_h2o": "Soil pH in water (1:5 ratio), unitless",
                "nitrogen_g_per_kg": "Total nitrogen content, g/kg",
                "soc_g_per_kg": "Soil organic carbon, g/kg",
                "clay_pct": "Clay content (< 2 um), %",
                "sand_pct": "Sand content (50-2000 um), %",
                "silt_pct": "Silt content (2-50 um), %",
                "cec_cmol_per_kg": "Cation exchange capacity, cmol(+)/kg",
            },
            "depth": "0-30cm mean",
        }
    }

    success = 0
    for twp in townships:
        tid = twp["id"]
        lat = twp["latitude"]
        lon = twp["longitude"]
        print(f"  {twp['name']} ({tid}): {lat}, {lon} ... ", end="", flush=True)

        props = fetch_soil(lat, lon)
        if props:
            props["township_id"] = tid
            results[tid] = props
            success += 1
            print("OK")
        else:
            print("FAILED")

        time.sleep(DELAY_SECONDS)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone: {success}/{len(townships)} townships saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
