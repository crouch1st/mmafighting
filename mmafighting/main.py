import json
import os

import structlog
from scraper import Scraper

import logging_config


def main():
    json_data = os.path.join(os.getcwd(), "config", "mmafighting.conf")
    with open(json_data) as json_file:
        parameters = json.load(json_file)
        logger.info(parameters)

        content = Scraper(config=parameters)
        content.send_desirable_content()

if __name__ == '__main__':
    logging_config.configure_structlog(level='info')

    logger = structlog.get_logger(__name__)

    main()