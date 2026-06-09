import logging

import supervision as sv
import numpy as np


logger = logging.getLogger(__name__)


class MultiObjectTracker:
    """
    Production-grade ByteTrack wrapper.
    """

    def __init__(self):

        logger.info(
            "Initializing ByteTrack tracker"
        )

        self.tracker = sv.ByteTrack()

    def update(self, detections):

        logger.debug(
            f"Updating tracker with "
            f"{len(detections)} detections"
        )

        if len(detections) == 0:

            logger.debug(
                "No detections received for tracking"
            )

            return []

        xyxy = np.array([
            det["bbox"]
            for det in detections
        ])

        confidence = np.array([
            det["confidence"]
            for det in detections
        ])

        class_id = np.array([
            det["class_id"]
            for det in detections
        ])

        logger.debug(
            "Converted detections into numpy arrays"
        )

        supervision_detections = sv.Detections(
            xyxy=xyxy,
            confidence=confidence,
            class_id=class_id
        )

        tracked_detections = (
            self.tracker.update_with_detections(
                supervision_detections
            )
        )

        logger.debug(
            f"Tracker returned "
            f"{len(tracked_detections)} tracked objects"
        )

        tracks = []

        for i in range(len(tracked_detections)):

            bbox = tracked_detections.xyxy[i]

            track_id = tracked_detections.tracker_id[i]

            conf = tracked_detections.confidence[i]

            x1, y1, x2, y2 = map(int, bbox)

            tracks.append({
                "track_id": int(track_id),
                "bbox": [x1, y1, x2, y2],
                "confidence": float(conf),
            })

        logger.debug(
            f"Generated {len(tracks)} final tracks"
        )

        return tracks
