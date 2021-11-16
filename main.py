# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import getopt
from parse import Parse as Psr
import transform as trm
import sys


def main(argv):
    # config filename
    configfile = None

    # if no params passed or more then needed then usage() message
    if not argv or len(argv) > 2:
        trm.usage(sys.argv[0])
        sys.exit(2)

    # validate options and arguments
    try:
        opts, args = getopt.getopt(argv, "c:h:")
    except getopt.GetoptError:
        trm.usage(sys.argv[0])
        sys.exit(2)

    # extract configfile from the argument
    for opt, arg in opts:
        if opt in ["-h"]:
            trm.usage(sys.argv[0])
            sys.exit(2)
        elif opt in ["-c"]:
            configfile = trm.unx2win(arg)

    # validate config
    try:
        # open JSON config file
        conf = open(configfile, mode="r")
        # init config dictionary with defaulted values as list type
        # conf_dict = dd(list)
        # load JSON config into dictionary
        conf_dict = json.load(conf)
        conf.close()
    except FileNotFoundError:
        print(f"Config file {configfile} was not found.")
        sys.exit(2)

    # created parsing instance
    parse = Psr(configfile, conf_dict)

    # JSON validation
    if not parse.validate_flat_config():
        print(parse.error_msg)
        sys.exit(2)

    # input file validation
    if not trm.validate_input_file(parse):
        print(parse.error_msg)
        sys.exit(2)

    # go through output key in config and loop through all defined types
    for out_key, out_val in parse.output.items():
        trm.export(parse, out_key, out_val)


if __name__ == '__main__':
    # call main with option arguments only, omit first argument which is name of executing program
    main(sys.argv[1:])
