import logging

from typing import List


logger = logging.getLogger(__name__)


ZONE_PRIORITY = {
    "billing": 100,
    "staff": 95,
    "queue": 90,
    "demo_counter": 85,
    "shelf": 80,
    "entry": 70,
    "transition": 50,
    "walkway": 10,
    "outside": 0,
}


def get_zone_priority(zone_name: str) -> int:
    """
    Get semantic priority of a zone.

    Example:
        left_shelf_zone -> 80
        billing_zone -> 100
    """

    logger.debug(
        f"Resolving priority for zone: {zone_name}"
    )

    zone_name = zone_name.lower()

    for semantic_name, priority in ZONE_PRIORITY.items():

        if semantic_name in zone_name:

            logger.debug(
                f"Matched semantic zone "
                f"'{semantic_name}' with "
                f"priority={priority}"
            )

            return priority

    logger.warning(
        f"No semantic priority match found "
        f"for zone: {zone_name}"
    )

    return 0


def resolve_zone_priority(candidate_zones: List[str]) -> str:
    """
    Resolve overlapping polygons using semantic priority.
    """

    logger.debug(
        f"Resolving priority among candidate zones: "
        f"{candidate_zones}"
    )

    if not candidate_zones:

        logger.debug(
            "No candidate zones found, "
            "returning 'unknown'"
        )

        return "unknown"

    resolved_zone = max(
        candidate_zones,
        key=get_zone_priority
    )

    logger.info(
        f"Resolved final zone: {resolved_zone}"
    )

    return resolved_zone
