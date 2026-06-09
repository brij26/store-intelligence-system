import json
import logging
import os


logger = logging.getLogger(__name__)


class JsonEventLogger:

    def __init__(self, output_path):

        self.output_path = output_path

        logger.info(
            f"Initializing JsonEventLogger "
            f"with output path: {output_path}"
        )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        logger.debug(
            f"Ensured event log directory exists: "
            f"{os.path.dirname(output_path)}"
        )

    def log_event(self, event):

        logger.debug(
            f"Logging event: {event}"
        )

        with open(self.output_path, "a") as f:

            f.write(
                json.dumps(event) + "\n"
            )

        logger.debug(
            "Event successfully written to JSONL file"
        )
