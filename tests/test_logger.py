import os
import sys
import pytest
from kheramat.logger import (
    setup_logging, install_crash_handler, log_crash,
    read_app_log, read_crash_log, clear_all_logs, LOG_DIR, APP_LOG_PATH, CRASH_LOG_PATH
)

def test_logger_setup():
    setup_logging()
    assert os.path.exists(LOG_DIR)
    assert os.path.exists(APP_LOG_PATH)
    log_content = read_app_log()
    assert "Vectra logging subsystem initialized" in log_content

def test_crash_logging():
    clear_all_logs()
    try:
        raise ValueError("Simulated crash for logger test")
    except ValueError as e:
        exc_type, exc_val, exc_tb = sys.exc_info()
        log_crash(exc_type, exc_val, exc_tb)
        
    crash_content = read_crash_log()
    assert "VECTRA CRASH REPORT" in crash_content
    assert "ValueError" in crash_content
    assert "Simulated crash for logger test" in crash_content

def test_clear_logs():
    clear_all_logs()
    assert read_crash_log().strip() == ""
