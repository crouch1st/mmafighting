import os
# import getopt
import sys
import json
import logging.config
print(os.getcwd)
from mmafighting import mmafighting as mma


logger = logging.getLogger(__name__)



def main(argv):
    json_data = os.path.join(os.getcwd(), "config", "mmafighting.conf")
    with open(json_data) as json_file:
        parameters = json.load(json_file)
        print(parameters)

        mma.get_desirable_urls(parameters['website'])


# def usage():
#     print("""
#     Usage: python ingest_sources.py [options]
#
#     Options:
#     -h, --help    Show this help message and exit
#     -c CONF, --config CONF   Get input from and write output to database with parameters specified in CONF file
#
#     Examples:
#     python ingest_sources.py --config config/ingest_sources.conf
#
#     Tips:
#     To prevent excessive writes to stdout when working on large datasets, set LEVEL=INFO in the [handler_consoleHandler]
#     section in "logging.conf"
#     """)


# def main(argv):
#     try:
#         opts, args = getopt.getopt(argv, "hc:", ["help", "config="])
#     except getopt.GetoptError:
#         usage()
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt in ("-h", "--help"):
#             usage()
#             sys.exit()
#         elif opt in ("-c", "--config"):
#             utility.send_email_on_completion_for_function_with_json_input(arg, ingest_sources)



if __name__ == '__main__':
    try:
        this_file_directory = os.path.dirname(os.path.realpath(__file__))
        logging.config.fileConfig(os.sep.join([os.getcwd(), 'config', 'mmafighting.conf']),
                                  disable_existing_loggers=False)
        main(sys.argv[1:])
    except Exception as e:
        raise
