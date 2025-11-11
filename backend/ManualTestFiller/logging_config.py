import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """
        Configure the logging of the application, as this application
        is containerized, it should and must have a clean way to get the
        log easily !
    """
    # Make sure to logs directory exists
    os.makedirs(name='logs', exist_ok=True)

    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO

    # File-based logging
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask app starting up !')
