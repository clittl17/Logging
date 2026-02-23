# Logging

A simple Python logging helper built on top of the standard `logging` module.

## Files

| File | Purpose |
|------|---------|
| `logger.py` | `get_logger()` factory function |
| `tests/test_logger.py` | Unit tests (pytest) |

## Quick Start

```python
from logger import get_logger

log = get_logger(__name__)

log.debug("Debug message")
log.info("Application started")
log.warning("Low disk space")
log.error("Something went wrong")
log.critical("Fatal error")
```

### Log to a file as well

```python
log = get_logger(__name__, log_file="app.log")
log.info("This goes to stdout AND app.log")
```

### Change the minimum log level

```python
import logging
from logger import get_logger

log = get_logger(__name__, level=logging.WARNING)
log.debug("This is suppressed")
log.warning("This is shown")
```

## Running the Tests

```bash
pip install pytest
python -m pytest tests/ -v
```
