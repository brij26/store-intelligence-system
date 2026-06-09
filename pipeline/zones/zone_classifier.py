import logging

import cv2
import numpy as np

from pipeline.zones.priority_resolver import resolve_zone_priority


logger = logging.getLogger(__name__)


class ZoneClassifier:
    """
    Production-grade semantic zone classifier.
    """

    def __init__(self, polygons: dict):

        logger.info(
            f"Initializing ZoneClassifier with "
            f"{len(polygons)} polygons"
        )

        self.polygons = polygons

    def classify_point(self, point):

        logger.debug(
            f"Classifying point: {point}"
        )

        candidate_zones = []

        for zone_name, polygon in self.polygons.items():

            polygon_np = np.array(
                polygon,
                dtype=np.int32
            )

            result = cv2.pointPolygonTest(
                polygon_np,
                point,
                False
            )

            if result >= 0:

                logger.debug(
                    f"Point {point} matched "
                    f"zone={zone_name}"
                )

                candidate_zones.append(zone_name)

        resolved_zone = resolve_zone_priority(
            candidate_zones
        )

        logger.info(
            f"Resolved point {point} "
            f"to zone={resolved_zone}"
        )

        return resolved_zone

    def get_all_matching_zones(self, point):

        logger.debug(
            f"Finding all matching zones for "
            f"point={point}"
        )

        matched_zones = []

        for zone_name, polygon in self.polygons.items():

            polygon_np = np.array(
                polygon,
                dtype=np.int32
            )

            result = cv2.pointPolygonTest(
                polygon_np,
                point,
                False
            )

            if result >= 0:

                logger.debug(
                    f"Point {point} inside "
                    f"zone={zone_name}"
                )

                matched_zones.append(zone_name)

        logger.info(
            f"Point {point} matched "
            f"{len(matched_zones)} zones"
        )

        return matched_zones
