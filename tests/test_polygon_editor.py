# tests/test_polygon_editor.py

"""
Unit tests for polygon editor utilities.
"""

import json
import tempfile
from pathlib import Path

from pipeline.zones.polygon_editor import (
    load_existing_zones,
    save_zones,
    zones
)


# ============================================================
# TEST SAVE ZONES
# ============================================================

def test_save_zones():

    # Create temporary file
    with tempfile.NamedTemporaryFile(
        suffix=".json",
        delete=False
    ) as temp_file:

        temp_path = temp_file.name

    # Dummy zones
    test_zones = {
        "entry_zone": [
            [100, 100],
            [200, 100],
            [200, 200]
        ]
    }

    # Inject zones
    zones.clear()
    zones.update(test_zones)

    # Save zones
    save_zones(temp_path)

    # Verify file exists
    assert Path(temp_path).exists()

    # Read JSON back
    with open(temp_path, "r") as f:

        loaded_data = json.load(f)

    # Verify content
    assert loaded_data == test_zones

    print("✅ test_save_zones passed")


# ============================================================
# TEST LOAD ZONES
# ============================================================

def test_load_existing_zones():

    # Create temp JSON file
    with tempfile.NamedTemporaryFile(
        suffix=".json",
        delete=False,
        mode="w"
    ) as temp_file:

        json.dump(
            {
                "promo_zone": [
                    [10, 10],
                    [50, 10],
                    [50, 50]
                ]
            },
            temp_file
        )

        temp_path = temp_file.name

    # Clear current zones
    zones.clear()

    # Load zones
    load_existing_zones(temp_path)

    # Verify zones loaded
    assert "promo_zone" in zones

    assert len(zones["promo_zone"]) == 3

    print("✅ test_load_existing_zones passed")


# ============================================================
# TEST POLYGON STRUCTURE
# ============================================================

def test_polygon_structure():

    polygon = [
        [0, 0],
        [100, 0],
        [100, 100]
    ]

    # Polygon should have at least 3 points
    assert len(polygon) >= 3

    # Every point should contain x,y
    for point in polygon:

        assert len(point) == 2

        assert isinstance(point[0], int)
        assert isinstance(point[1], int)

    print("✅ test_polygon_structure passed")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_save_zones()

    test_load_existing_zones()

    test_polygon_structure()

    print("\n🎉 All polygon editor tests passed")
