import cv2


class FrameManager:

    def __init__(
        self,
        target_width=1280,
        target_height=720
    ):

        self.target_width = target_width
        self.target_height = target_height

    def resize_frame(self, frame):

        resized_frame = cv2.resize(
            frame,
            (self.target_width, self.target_height)
        )

        return resized_frame

    def convert_to_rgb(self, frame):

        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

    def get_frame_shape(self, frame):

        return frame.shape