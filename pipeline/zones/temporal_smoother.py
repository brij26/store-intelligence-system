import logging

from collections import defaultdict


logger = logging.getLogger(__name__)


class TemporalZoneSmoother:
    """
    Smooth noisy zone transitions across frames.

    Example:
        walkway -> shelf -> walkway flickering
        becomes stable semantic classification.
    """

    def __init__(self, min_stable_frames: int = 10):

        logger.info(
            f"Initializing TemporalZoneSmoother "
            f"with min_stable_frames="
            f"{min_stable_frames}"
        )

        self.min_stable_frames = min_stable_frames

        self.track_state = defaultdict(
            lambda: {
                "current_zone": None,
                "candidate_zone": None,
                "candidate_count": 0,
            }
        )

    def update(self, track_id: int, detected_zone: str) -> str:

        logger.debug(
            f"Updating temporal smoother for "
            f"track_id={track_id}, "
            f"detected_zone={detected_zone}"
        )

        state = self.track_state[track_id]

        # First observation
        if state["current_zone"] is None:

            logger.info(
                f"Track {track_id} initialized "
                f"in zone={detected_zone}"
            )

            state["current_zone"] = detected_zone

            return detected_zone

        # Same zone
        if detected_zone == state["current_zone"]:

            logger.debug(
                f"Track {track_id} remains stable "
                f"in zone={detected_zone}"
            )

            state["candidate_zone"] = None
            state["candidate_count"] = 0

            return state["current_zone"]

        # New candidate transition
        if detected_zone == state["candidate_zone"]:

            state["candidate_count"] += 1

            logger.debug(
                f"Track {track_id} candidate "
                f"zone={detected_zone}, "
                f"candidate_count="
                f"{state['candidate_count']}"
            )

        else:

            logger.info(
                f"Track {track_id} detected new "
                f"candidate zone={detected_zone}"
            )

            state["candidate_zone"] = detected_zone
            state["candidate_count"] = 1

        # Stable transition achieved
        if state["candidate_count"] >= self.min_stable_frames:

            logger.info(
                f"Track {track_id} stabilized "
                f"into new zone={detected_zone}"
            )

            state["current_zone"] = detected_zone

            state["candidate_zone"] = None
            state["candidate_count"] = 0

        return state["current_zone"]

    def reset_track(self, track_id: int):

        logger.debug(
            f"Resetting temporal state for "
            f"track_id={track_id}"
        )

        if track_id in self.track_state:

            del self.track_state[track_id]

            logger.info(
                f"Removed temporal state for "
                f"track_id={track_id}"
            )
