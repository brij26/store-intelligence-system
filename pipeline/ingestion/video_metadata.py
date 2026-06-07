import cv2
from pathlib import Path

from pipeline.utils.logger import setup_logger


logger = setup_logger(__name__)


class VideoMetadata:

    def __init__(self, video_path: str):

        self.video_path = Path(video_path)

        logger.info(
            f"Initializing VideoMetadata for: {self.video_path}"
        )

        if not self.video_path.exists():

            logger.error(
                f"Video file not found: {self.video_path}"
            )

            raise FileNotFoundError(
                f"Video not found: {self.video_path}"
            )

        self.cap = cv2.VideoCapture(
            str(self.video_path)
        )

        if not self.cap.isOpened():

            logger.error(
                f"Unable to open video: {self.video_path}"
            )

            raise ValueError(
                f"Unable to open video: {self.video_path}"
            )

        logger.info("Video opened successfully")

    def get_metadata(self):

        logger.info("Extracting video metadata")

        fps = self.cap.get(cv2.CAP_PROP_FPS)

        frame_count = int(
            self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        duration = frame_count / fps

        metadata = {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration": duration
        }

        logger.info(
            f"Metadata extracted successfully: {metadata}"
        )

        return metadata

    def release(self):

        if self.cap.isOpened():

            self.cap.release()

            logger.info("VideoCapture released")