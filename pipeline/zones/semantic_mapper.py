import logging

from pipeline.zones.zone_classifier import ZoneClassifier
from pipeline.zones.temporal_smoother import TemporalZoneSmoother


logger = logging.getLogger(__name__)


class SemanticMapper:

    def __init__(
        self,
        polygons,
        min_stable_frames=10
    ):

        logger.info(
            f"Initializing SemanticMapper with "
            f"min_stable_frames={min_stable_frames}"
        )

        self.classifier = ZoneClassifier(polygons)

        self.smoother = TemporalZoneSmoother(
            min_stable_frames=min_stable_frames
        )

    def map_track_to_zone(
        self,
        track_id,
        foot_point
    ):

        logger.debug(
            f"Mapping track_id={track_id} "
            f"with foot_point={foot_point}"
        )

        raw_zone = self.classifier.classify_point(
            foot_point
        )

        logger.debug(
            f"Raw zone detected for "
            f"track_id={track_id}: {raw_zone}"
        )

        stable_zone = self.smoother.update(
            track_id=track_id,
            detected_zone=raw_zone
        )

        logger.debug(
            f"Stable zone resolved for "
            f"track_id={track_id}: {stable_zone}"
        )

        result = {
            "track_id": track_id,
            "foot_point": foot_point,
            "raw_zone": raw_zone,
            "stable_zone": stable_zone,
        }

        logger.debug(
            f"Semantic mapping result: {result}"
        )

        return result
