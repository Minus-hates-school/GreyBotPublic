from __future__ import annotations
import logging

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

class ColorFormatter(logging.Formatter):
    Colors = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET = '\033[0m'

    # Ignore that target thinggy, We Overideing the default format command.
    def format(self, record):
        log_color = self.Colors.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

def setup_logger(
        level: int = logging.INFO,
        stream_logs: bool = False,
        logger_format: str = LOGGER_FORMAT,
) -> None:
    """Sets up the service logger
        Parameters
        ----------
        level : int, optional
            Level to log in the main logger, by default logging.INFO
        stream_logs : bool, optional
            Flag to stream the logs to the console, by default False
        logger_format : str, optional
            Format the logger will log in, by default LOGGER_FORMAT
        """
    log_formatter = ColorFormatter(logger_format)

    handlers: list[logging.Handler] = []
    if stream_logs:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(level)
        handlers.append(stream_handler)
    logging.basicConfig(level=level, handlers=handlers)
