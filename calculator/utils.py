from flask import jsonify
import logging, os , sys
from datetime import datetime

# --- Standardized JSON response utility ---
def response(result=None, error_message=None, status=200):
    """
    Standardized JSON response for success or error.

    - Only field is either 'result' or 'errorMessage', not both.
    - Status defaults to 200 for success, override with 409 for errors.
    """
    if error_message is not None:
        return jsonify({'errorMessage': error_message}), status
    else:
        return jsonify({'result': result}), status


# --- Custom formatter to show milliseconds ---
class TimeFormat(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        # Format with microseconds then trim to milliseconds
        return dt.strftime('%d-%m-%Y %H:%M:%S.%f')[:-3] 


# --- Helper to configure a logger ---
def setup_logger(name, dir, level, logfile, to_stdout=False):
    """
    Creates and returns a logger configured to write to a file (and optionally stdout).

    Args:
        name (str): Identifier for the logger.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        logfile (str): Filename under LOG_DIR where logs will be written.
        to_stdout (bool): If True, also output logs to the console.
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Retrieve or create a logger with the specified name
    logger = logging.getLogger(name)
    # Set the logger's threshold level
    logger.setLevel(level)

    # File handler writes log records to a file
    file_path = os.path.join(dir, logfile)
    handler = logging.FileHandler(file_path)
    handler.setFormatter(
        TimeFormat("%(asctime)s %(levelname)s: %(message)s")
    )
    logger.addHandler(handler)

    if to_stdout:
        # Optional stream handler that writes to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            TimeFormat("%(asctime)s %(levelname)s: %(message)s")
        )
        logger.addHandler(console_handler)

    # Return the configured logger
    return logger
