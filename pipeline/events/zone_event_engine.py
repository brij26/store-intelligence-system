import logging

from collections import defaultdict
from datetime import datetime


logger = logging.getLogger(__name__)


class ZoneEventEngine:

    def __init__(self):

        logger.info(
            "Initializing ZoneEventEngine"
        )

        self.track_state = defaultdict(
            lambda: {
                "previous_zone": None,
                "current_zone": None,
                "zone_enter_time": None,
            }
        )

    def update(
        self,
        track_id,
        stable_zone,
        timestamp=None
    ):

        if timestamp is None:
            timestamp = datetime.utcnow()

        logger.debug(
            f"Updating zone state for "
            f"track_id={track_id}, "
            f"stable_zone={stable_zone}"
        )

        state = self.track_state[track_id]

        events = []

        # First observation
        if state["current_zone"] is None:

            logger.info(
                f"Track {track_id} entered "
                f"initial zone: {stable_zone}"
            )

            state["current_zone"] = stable_zone
            state["zone_enter_time"] = timestamp

            events.append({
                "event_type": "ZONE_ENTER",
                "track_id": track_id,
                "zone": stable_zone,
                "timestamp": str(timestamp),
            })

            return events

        # Zone transition
        if stable_zone != state["current_zone"]:

            previous_zone = state["current_zone"]

            logger.info(
                f"Track {track_id} transitioned "
                f"from {previous_zone} "
                f"to {stable_zone}"
            )

            dwell_seconds = (
                timestamp - state["zone_enter_time"]
            ).total_seconds()

            logger.debug(
                f"Track {track_id} dwell time "
                f"in {previous_zone}: "
                f"{dwell_seconds:.2f}s"
            )

            # EXIT EVENT
            events.append({
                "event_type": "ZONE_EXIT",
                "track_id": track_id,
                "zone": previous_zone,
                "dwell_time_seconds": dwell_seconds,
                "timestamp": str(timestamp),
            })

            # ENTER EVENT
            events.append({
                "event_type": "ZONE_ENTER",
                "track_id": track_id,
                "zone": stable_zone,
                "timestamp": str(timestamp),
            })

            state["previous_zone"] = previous_zone
            state["current_zone"] = stable_zone
            state["zone_enter_time"] = timestamp

        return events

    def remove_track(
        self,
        track_id,
        timestamp=None
    ):

        if timestamp is None:
            timestamp = datetime.utcnow()

        logger.debug(
            f"Removing track_id={track_id}"
        )

        if track_id not in self.track_state:

            logger.warning(
                f"Track {track_id} not found "
                f"in track_state"
            )

            return []

        state = self.track_state[track_id]

        dwell_seconds = (
            timestamp - state["zone_enter_time"]
        ).total_seconds()

        logger.info(
            f"Track {track_id} ended in "
            f"zone={state['current_zone']} "
            f"after {dwell_seconds:.2f}s"
        )

        events = [{
            "event_type": "TRACK_END",
            "track_id": track_id,
            "zone": state["current_zone"],
            "dwell_time_seconds": dwell_seconds,
            "timestamp": str(timestamp),
        }]

        del self.track_state[track_id]

        return events
