import logging

import cv2


logger = logging.getLogger(__name__)


class VideoReader:

    def __init__(self, video_path):

        logger.info(
            f"Initializing VideoReader with "
            f"video: {video_path}"
        )

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():

            logger.error(
                f"Unable to open video: {video_path}"
            )

            raise ValueError(
                f"Unable to open video: {video_path}"
            )

        logger.info(
            "VideoCapture initialized successfully"
        )

    def read(self):

        success, frame = self.cap.read()

        if not success:

            logger.debug(
                "No more frames available or "
                "failed to read frame"
            )

        return success, frame

    def release(self):

        logger.info(
            "Releasing VideoCapture resource"
        )

        self.cap.release()

    def get_fps(self):

        fps = int(
            self.cap.get(cv2.CAP_PROP_FPS)
        )

        logger.debug(
            f"Retrieved video FPS: {fps}"
        )

        return fps

    def get_frame_size(self):

        width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        logger.debug(
            f"Retrieved frame size: "
            f"{width}x{height}"
        )

        return width, height
