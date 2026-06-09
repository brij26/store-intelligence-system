import logging

import cv2


logger = logging.getLogger(__name__)


def draw_bbox(
    frame,
    bbox,
    track_id=None,
    zone_name=None,
    color=(0, 255, 0)
):

    logger.debug(
        f"Drawing bbox={bbox}, "
        f"track_id={track_id}, "
        f"zone_name={zone_name}"
    )

    x1, y1, x2, y2 = bbox

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        2
    )

    label = ""

    if track_id is not None:
        label += f"ID:{track_id}"

    if zone_name is not None:
        label += f" | {zone_name}"

    cv2.putText(
        frame,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2
    )


def draw_foot_point(
    frame,
    foot_point,
    color=(0, 0, 255)
):

    logger.debug(
        f"Drawing foot point at {foot_point}"
    )

    cv2.circle(
        frame,
        foot_point,
        5,
        color,
        -1
    )


def draw_polygon(
    frame,
    polygon,
    zone_name,
    color=(255, 0, 0)
):

    logger.debug(
        f"Drawing polygon for zone={zone_name}"
    )

    cv2.polylines(
        frame,
        [polygon],
        isClosed=True,
        color=color,
        thickness=2
    )

    x, y = polygon[0]

    cv2.putText(
        frame,
        zone_name,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
    )
