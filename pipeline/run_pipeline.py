import logging
from datetime import datetime

import cv2

from pipeline.detection.detector import PersonDetector
from pipeline.tracking.tracker import MultiObjectTracker

from pipeline.utils.geometry import get_foot_point

from pipeline.utils.video_utils import VideoReader

from pipeline.utils.visualization import (
    draw_bbox,
    draw_foot_point,
    draw_polygon
)

from pipeline.zones.polygon_loader import load_polygons

from pipeline.zones.semantic_mapper import SemanticMapper

from pipeline.events.zone_event_engine import (
    ZoneEventEngine
)

from pipeline.storage.json_event_logger import (
    JsonEventLogger
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    )
)

logger = logging.getLogger(__name__)


logger.info(
    "Starting Retail Spatial Intelligence Pipeline"
)


event_logger = JsonEventLogger(
    "outputs/events/store_1_events.jsonl"
)


VIDEO_PATH = (
    "D:/store-intelligence-system/data/raw/Store_2/zone.mp4"
)

MODEL_PATH = (
    "D:/store-intelligence-system/"
    "experiments/models/weights/yolov8n.pt"
)

ZONE_JSON_PATH = (
    "D:\store-intelligence-system\configs\store_2\zone_area.json"
)


# ---------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------

logger.info("Initializing video reader")

video_reader = VideoReader(VIDEO_PATH)

fps = video_reader.get_fps()

logger.info(f"Video FPS: {fps}")

logger.info("Initializing detector")

detector = PersonDetector(
    model_path=MODEL_PATH,
    conf_threshold=0.3
)

logger.info("Initializing tracker")

tracker = MultiObjectTracker()

frame_width, frame_height = (
    video_reader.get_frame_size()
)

logger.info(
    f"Video frame size: "
    f"{frame_width}x{frame_height}"
)

logger.info("Loading polygons")

polygons = load_polygons(
    json_path=ZONE_JSON_PATH,
    target_width=frame_width,
    target_height=frame_height
)

logger.info(
    f"Loaded {len(polygons)} polygons"
)

logger.info("Initializing semantic mapper")

semantic_mapper = SemanticMapper(
    polygons=polygons,
    min_stable_frames=10
)

logger.info("Initializing event engine")

event_engine = ZoneEventEngine()


# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------

logger.info("Entering main processing loop")

frame_count = 0

while True:

    success, frame = video_reader.read()

    if not success:

        logger.info(
            "Video stream ended or "
            "failed to read frame"
        )

        break

    frame_count += 1

    logger.debug(
        f"Processing frame {frame_count}"
    )

    detections = detector.detect(frame)

    logger.debug(
        f"Frame {frame_count}: "
        f"{len(detections)} detections"
    )

    tracks = tracker.update(detections)

    logger.debug(
        f"Frame {frame_count}: "
        f"{len(tracks)} tracks"
    )

    # Draw polygons
    for zone_name, polygon in polygons.items():

        draw_polygon(
            frame,
            polygon,
            zone_name
        )

    # Process tracks
    for track in tracks:

        track_id = track["track_id"]

        bbox = track["bbox"]

        logger.debug(
            f"Processing track_id={track_id}"
        )

        foot_point = get_foot_point(bbox)

        semantic_result = semantic_mapper.map_track_to_zone(
            track_id=track_id,
            foot_point=foot_point
        )

        stable_zone = semantic_result["stable_zone"]

        logger.debug(
            f"Track {track_id} mapped "
            f"to zone={stable_zone}"
        )

        events = event_engine.update(
            track_id=track_id,
            stable_zone=stable_zone,
            timestamp=datetime.utcnow()
        )

        # Draw visualization
        draw_bbox(
            frame,
            bbox,
            track_id=track_id,
            zone_name=stable_zone
        )

        draw_foot_point(
            frame,
            foot_point
        )

        # Event logging
        for event in events:

            logger.info(
                f"Generated event: {event}"
            )

            event_logger.log_event(event)

    # ---------------------------------------------------
    # DISPLAY RESIZE
    # ---------------------------------------------------

    display_width = 1400
    display_height = 800

    display_frame = cv2.resize(
        frame,
        (display_width, display_height)
    )

    cv2.imshow(
        "Retail Spatial Intelligence",
        display_frame
    )

    key = cv2.waitKey(1)

    if key == ord("q"):

        logger.info(
            "Exit requested by user"
        )

        break


logger.info(
    "Releasing video resources"
)

video_reader.release()

cv2.destroyAllWindows()

logger.info(
    "Retail Spatial Intelligence "
    "Pipeline stopped successfully"
)
