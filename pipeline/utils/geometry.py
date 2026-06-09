import logging
import math


logger = logging.getLogger(__name__)


def get_bbox_center(bbox):

    logger.debug(
        f"Calculating bbox center for bbox={bbox}"
    )

    x1, y1, x2, y2 = bbox

    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)

    center_point = (center_x, center_y)

    logger.debug(
        f"Computed bbox center: {center_point}"
    )

    return center_point


def get_foot_point(bbox):

    logger.debug(
        f"Calculating foot point for bbox={bbox}"
    )

    x1, y1, x2, y2 = bbox

    foot_x = int((x1 + x2) / 2)
    foot_y = int(y2)

    foot_point = (foot_x, foot_y)

    logger.debug(
        f"Computed foot point: {foot_point}"
    )

    return foot_point


def euclidean_distance(point1, point2):

    logger.debug(
        f"Calculating euclidean distance between "
        f"{point1} and {point2}"
    )

    distance = math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )

    logger.debug(
        f"Computed euclidean distance: {distance}"
    )

    return distance
