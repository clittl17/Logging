"""
logger.py – A simple, reusable logging helper built on Python's built-in
``logging`` module.

Usage
-----
    from logger import get_logger

    log = get_logger(__name__)
    log.info("Application started")
    log.warning("Low disk space")
    log.error("Something went wrong")

You can also log to a file:

    log = get_logger(__name__, log_file="app.log")
"""

import logging
import sys


def get_logger(
    name: str,
    level: int = logging.DEBUG,
    log_file: str | None = None,
    fmt: str = "%(asctime)s  %(name)s  %(levelname)-8s  %(message)s",
    date_fmt: str = "%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    """Return a configured :class:`logging.Logger`.

    Parameters
    ----------
    name:
        Logger name (typically ``__name__``).
    level:
        Minimum severity level to capture (default: ``logging.DEBUG``).
    log_file:
        Optional path to a log file.  When provided, messages are written
        to both the console *and* the file.
    fmt:
        Log-record format string.
    date_fmt:
        Date/time format used inside the log record.

    Returns
    -------
    logging.Logger
        A logger that is ready to use.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers when the logger is retrieved multiple times.
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    # Console handler – always present.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler – optional.
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
