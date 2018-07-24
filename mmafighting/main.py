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

    image = os.path.join(os.getcwd(), "pngs", "small_logo.png")

    content = Scraper(config=parameters, image=image)
    content.send_desirable_content()

if __name__ == '__main__':
    logging_config.configure_structlog(level='info')

    logger = structlog.get_logger(__name__)

    main()