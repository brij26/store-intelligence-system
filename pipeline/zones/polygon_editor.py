# pipeline/zones/polygon_editor.py

"""
Polygon Zone Editor for Retail Analytics System
------------------------------------------------

Features:
- Draw polygon zones using mouse clicks
- Save zones into JSON
- Load existing zones
- Reset current polygon
- Multiple named zones
- Visual debugging
- Logging support

Controls:
---------
Left Mouse Click  -> Add polygon point
C                 -> Close current polygon
S                 -> Save current polygon
R                 -> Reset current polygon
N                 -> Enter new zone name
Q                 -> Quit editor
"""

import cv2
import json
import logging
import numpy as np
from pathlib import Path

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

current_polygon = []
zones = {}

drawing_closed = False

window_name = "Polygon Editor"

# These will be initialized later
original_frame = None
display_frame = None

# Current active zone name
current_zone_name = None

# JSON save path
json_output_path = None


# ============================================================
# LOAD EXISTING ZONES
# ============================================================

def load_existing_zones(json_path):
    """
    Load existing zones from JSON file if available.
    """

    global zones

    if Path(json_path).exists():

        logger.info(f"Loading existing zones from: {json_path}")

        with open(json_path, "r") as f:

            loaded_zones = json.load(f)

        # IMPORTANT:
        # Modify existing dict instead of replacing it
        zones.clear()

        zones.update(loaded_zones)

        logger.info(f"Loaded {len(zones)} zones successfully")

    else:

        logger.info("No existing zone file found. Starting fresh.")

        zones.clear()


# ============================================================
# SAVE ZONES TO JSON
# ============================================================

def save_zones(json_path):
    """
    Save all zones into JSON file.
    """

    with open(json_path, "w") as f:
        json.dump(zones, f, indent=4)

    logger.info(f"Zones saved successfully -> {json_path}")


# ============================================================
# DRAW EXISTING ZONES
# ============================================================

def draw_existing_zones(frame):
    """
    Draw all previously saved zones on frame.
    """

    for zone_name, polygon in zones.items():

        pts = np.array(polygon, np.int32)

        cv2.polylines(
            frame,
            [pts],
            isClosed=True,
            color=(255, 0, 0),
            thickness=2
        )

        # Draw zone label
        x, y = polygon[0]

        cv2.putText(
            frame,
            zone_name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


# ============================================================
# REFRESH DISPLAY
# ============================================================

def refresh_display():
    """
    Refresh display frame with all drawings.
    """

    global display_frame

    # Reset frame
    display_frame = original_frame.copy()

    # Draw already saved zones
    draw_existing_zones(display_frame)

    # Draw current polygon
    if len(current_polygon) > 0:

        pts = np.array(current_polygon, np.int32)

        cv2.polylines(
            display_frame,
            [pts],
            isClosed=drawing_closed,
            color=(0, 255, 0),
            thickness=2
        )

        # Draw points
        for point in current_polygon:

            cv2.circle(
                display_frame,
                point,
                radius=5,
                color=(0, 255, 0),
                thickness=-1
            )

        # Draw current zone label
        if current_zone_name is not None:

            x, y = current_polygon[0]

            cv2.putText(
                display_frame,
                current_zone_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

    cv2.imshow(window_name, display_frame)


# ============================================================
# MOUSE CALLBACK
# ============================================================

def mouse_callback(event, x, y, flags, param):
    """
    Handle mouse click events.
    """

    global current_polygon

    if event == cv2.EVENT_LBUTTONDOWN:

        current_polygon.append((x, y))

        logger.info(f"Point added -> ({x}, {y})")

        refresh_display()


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_polygon_editor(video_path, json_path):
    """
    Main polygon editor runner.
    """

    global original_frame
    global current_polygon
    global current_zone_name
    global drawing_closed
    global json_output_path

    json_output_path = json_path

    logger.info("Starting Polygon Editor")

    # --------------------------------------------------------
    # Load Existing Zones
    # --------------------------------------------------------

    load_existing_zones(json_path)

    # --------------------------------------------------------
    # Load Video
    # --------------------------------------------------------

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        logger.error("Failed to open video")

        return

    # Read first frame
    success, frame = cap.read()

    if not success:

        logger.error("Failed to read frame")

        return

    original_frame = frame.copy()

    logger.info("First frame loaded successfully")

    # --------------------------------------------------------
    # Setup Window
    # --------------------------------------------------------

    cv2.namedWindow(window_name)

    cv2.setMouseCallback(window_name, mouse_callback)

    refresh_display()

    # --------------------------------------------------------
    # Main Loop
    # --------------------------------------------------------

    while True:

        key = cv2.waitKey(1) & 0xFF

        # ----------------------------------------------------
        # CLOSE POLYGON
        # ----------------------------------------------------

        if key == ord('c'):

            if len(current_polygon) >= 3:

                drawing_closed = True

                logger.info("Polygon closed")

                refresh_display()

            else:

                logger.warning("Need at least 3 points to close polygon")

        # ----------------------------------------------------
        # SAVE POLYGON
        # ----------------------------------------------------

        elif key == ord('s'):

            if current_zone_name is None:

                logger.warning("No zone name provided")

                continue

            if len(current_polygon) < 3:

                logger.warning("Polygon needs at least 3 points")

                continue

            # Save polygon
            zones[current_zone_name] = current_polygon.copy()

            # Save JSON
            save_zones(json_output_path)

            logger.info(f"Zone saved -> {current_zone_name}")

            # Reset current polygon
            current_polygon = []

            drawing_closed = False

            current_zone_name = None

            refresh_display()

        # ----------------------------------------------------
        # RESET CURRENT POLYGON
        # ----------------------------------------------------

        elif key == ord('r'):

            logger.info("Resetting current polygon")

            current_polygon = []

            drawing_closed = False

            refresh_display()

        # ----------------------------------------------------
        # NEW ZONE NAME
        # ----------------------------------------------------

        elif key == ord('n'):

            zone_name = input("\nEnter Zone Name: ")

            current_zone_name = zone_name.strip()

            logger.info(f"Current zone -> {current_zone_name}")

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        elif key == ord('q'):

            logger.info("Exiting Polygon Editor")

            break

    cap.release()

    cv2.destroyAllWindows()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    video_path = "data/raw/store_1/cam_1.mp4"

    json_path = "configs/zones/store_1_cam_1_zones.json"

    run_polygon_editor(video_path, json_path)
