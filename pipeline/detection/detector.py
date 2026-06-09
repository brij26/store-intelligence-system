import logging

from ultralytics import YOLO


logger = logging.getLogger(__name__)


class PersonDetector:
    """
    Production-grade YOLO person detector.
    """

    PERSON_CLASS_ID = 0

    def __init__(
        self,
        model_path: str,
        conf_threshold: float = 0.3
    ):

        logger.info(
            f"Initializing YOLO model from: {model_path}"
        )

        self.model = YOLO(model_path)

        self.conf_threshold = conf_threshold

        logger.info(
            f"PersonDetector initialized with "
            f"conf_threshold={conf_threshold}"
        )

    def detect(self, frame):

        logger.debug("Running person detection on frame")

        results = self.model(
            frame,
            verbose=False
        )

        detections = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls_id = int(box.cls[0])

                # Person class only
                if cls_id != self.PERSON_CLASS_ID:
                    continue

                confidence = float(box.conf[0])

                if confidence < self.conf_threshold:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class_id": cls_id,
                })

        logger.debug(
            f"Detected {len(detections)} valid person detections"
        )

        return detections
