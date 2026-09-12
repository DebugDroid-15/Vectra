import os
import sys
import logging
import traceback
import platform
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = os.path.join(os.path.expanduser("~"), ".vectra", "logs")
APP_LOG_PATH = os.path.join(LOG_DIR, "vectra_app.log")
CRASH_LOG_PATH = os.path.join(LOG_DIR, "vectra_crash.log")

_initialized = False

def get_log_dir() -> str:
    os.makedirs(LOG_DIR, exist_ok=True)
    return LOG_DIR

def setup_logging():
    global _initialized
    if _initialized:
        return
    
    log_dir = get_log_dir()
    
    # Configure root logger
    logger = logging.getLogger("vectra")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # Remove any existing handlers
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # Format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s.%(module)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotating File Handler (5 MB per file, max 5 backups)
    file_handler = RotatingFileHandler(
        APP_LOG_PATH, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    _initialized = True
    logger.info("Vectra logging subsystem initialized.")

def get_logger(name: str = "vectra") -> logging.Logger:
    if not _initialized:
        setup_logging()
    if name == "vectra" or name.startswith("vectra."):
        return logging.getLogger(name)
    return logging.getLogger(f"vectra.{name}")

def log_crash(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions to dedicated crash log file and app log."""
    log_dir = get_log_dir()
    logger = get_logger("crash")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    sys_info = (
        f"--- VECTRA CRASH REPORT [{timestamp}] ---\n"
        f"OS: {platform.system()} {platform.release()} ({platform.version()})\n"
        f"Python Version: {platform.python_version()} ({sys.executable})\n"
        f"Exception Type: {exc_type.__name__}\n"
        f"Exception Details: {exc_value}\n"
        f"Traceback:\n{tb_str}\n"
        f"{'='*60}\n"
    )
    
    logger.critical(f"UNCAUGHT CRASH DETECTED:\n{sys_info}")
    
    # Append directly to crash log file
    try:
        with open(CRASH_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(sys_info)
    except Exception as e:
        logger.error(f"Failed to write to crash log file: {e}")

def _excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    log_crash(exc_type, exc_value, exc_traceback)

def install_crash_handler():
    setup_logging()
    sys.excepthook = _excepthook
    
    # Also hook threading exception handler if Python 3.8+
    if hasattr(sys, "unraisablehook"):
        def _unraisablehook(unraisable):
            logger = get_logger("unraisable")
            logger.error(f"Unraisable exception: {unraisable.err_msg}", exc_info=unraisable.exc_value)
        sys.unraisablehook = _unraisablehook

def read_app_log(max_lines: int = 500) -> str:
    if not os.path.exists(APP_LOG_PATH):
        return "No application log records found."
    try:
        with open(APP_LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            return "".join(lines[-max_lines:])
    except Exception as e:
        return f"Error reading log file: {e}"

def read_crash_log(max_lines: int = 500) -> str:
    if not os.path.exists(CRASH_LOG_PATH):
        return "No crash reports recorded."
    try:
        with open(CRASH_LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            return "".join(lines[-max_lines:])
    except Exception as e:
        return f"Error reading crash file: {e}"

def clear_all_logs():
    for path in [APP_LOG_PATH, CRASH_LOG_PATH]:
        if os.path.exists(path):
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.truncate(0)
            except Exception:
                pass

