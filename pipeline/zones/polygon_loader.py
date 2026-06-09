import json
import logging

import numpy as np


logger = logging.getLogger(__name__)


SOURCE_POLYGON_WIDTH = 1280
SOURCE_POLYGON_HEIGHT = 720


def rescale_polygon(
    polygon,
    scale_x,
    scale_y
):

    logger.debug(
        f"Rescaling polygon with "
        f"scale_x={scale_x:.4f}, "
        f"scale_y={scale_y:.4f}"
    )

    scaled_polygon = []

    for x, y in polygon:

        scaled_x = int(x * scale_x)
        scaled_y = int(y * scale_y)

        scaled_polygon.append(
            [scaled_x, scaled_y]
        )

    logger.debug(
        f"Rescaled polygon contains "
        f"{len(scaled_polygon)} points"
    )

    return scaled_polygon


def load_polygons(
    json_path,
    target_width,
    target_height
):
    """
    Load polygons and automatically rescale them
    from drawing resolution -> actual video resolution.
    """

    logger.info(
        f"Loading polygons from: {json_path}"
    )

    with open(json_path, "r") as f:

        polygon_data = json.load(f)

    logger.debug(
        f"Loaded {len(polygon_data)} zones "
        f"from polygon JSON"
    )

    scale_x = (
        target_width / SOURCE_POLYGON_WIDTH
    )

    scale_y = (
        target_height / SOURCE_POLYGON_HEIGHT
    )

    logger.info(
        f"Polygon scaling factors -> "
        f"scale_x={scale_x:.4f}, "
        f"scale_y={scale_y:.4f}"
    )

    polygons = {}

    for zone_name, polygon_points in polygon_data.items():

        logger.debug(
            f"Processing zone: {zone_name}"
        )

        scaled_polygon = rescale_polygon(
            polygon_points,
            scale_x,
            scale_y
        )

        polygons[zone_name] = np.array(
            scaled_polygon,
            dtype=np.int32
        )

    logger.info(
        f"Successfully loaded and rescaled "
        f"{len(polygons)} polygons"
    )

    return polygons
