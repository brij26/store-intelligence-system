import cv2
from pathlib import Path

from pipeline.ingestion.frame_manager import FrameManager
from pipeline.utils.logger import setup_logger


logger = setup_logger(__name__)


class VideoReader:

    def __init__(
        self,
        video_path,
        frame_skip=1,
        resize=True
    ):

        self.video_path = Path(video_path)

        logger.info(
            f"Initializing VideoReader for: {self.video_path}"
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

        self.fps = self.cap.get(
            cv2.CAP_PROP_FPS
        )

        self.frame_skip = frame_skip

        self.frame_manager = FrameManager()

        self.resize = resize

        logger.info(
            f"VideoReader initialized successfully | "
            f"FPS={self.fps} | "
            f"Frame Skip={self.frame_skip}"
        )

    def read_frames(self):

        logger.info("Starting frame iteration")

        frame_id = 0

        while True:

            ret, frame = self.cap.read()

            if not ret:

                logger.warning(
                    "End of video reached"
                )

                break

            if frame_id % self.frame_skip == 0:

                timestamp = frame_id / self.fps

                if self.resize:

                    frame = (
                        self.frame_manager
                        .resize_frame(frame)
                    )

                yield {
                    "frame": frame,
                    "frame_id": frame_id,
                    "timestamp": timestamp
                }

            frame_id += 1

    def release(self):

        if self.cap.isOpened():

            self.cap.release()

            logger.info("VideoCapture released")