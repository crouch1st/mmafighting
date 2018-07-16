
import logging
import sys

import structlog


def configure_structlog(level='INFO', development_mode=False):
    """Configures structlog loggers. If development_mode set to True, will pretty print exception traces.
    :param level: defaults to 'info'
    :param development_mode: defaults to False.
    :return:
    """
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info
    ]

    if sys.version_info < (3,0):
        processors.append(structlog.processors.UnicodeEncoder(encoding='utf-8'))

    if development_mode:
        processors.append(structlog.processors.ExceptionPrettyPrinter())

    # append the renderer last
    # processors.append(structlog.processors.JSONRenderer())
    processors.append(structlog.processors.KeyValueRenderer())  # if we want to use 'kv' tag in filebeats, lets use this renderer

    structlog.configure_once(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(stream=sys.stdout, format='%(message)s', level=log_levels[level.upper()])

    # quiet chatty libs
    logging.getLogger("requests").setLevel(logging.WARNING)
