#!/usr/bin/env python

import os, sys, logging
from optparse import OptionParser

try:
    import tftpy
except:
    # Get tftpy package directory
    PACKAGE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    # Append tftpy package directory to the python path
    sys.path.append(os.path.realpath(PACKAGE_PATH))
    import tftpy


def main():
    usage=""
    parser = OptionParser(usage=usage)
    parser.add_option('-i',
                      '--ip',
                      type='string',
                      help='ip address to bind to (default: INADDR_ANY)',
                      default="")
    parser.add_option('-p',
                      '--port',
                      type='int',
                      help='local port to use (default: 69)',
                      default=69)
    parser.add_option('-r',
                      '--root',
                      type='string',
                      help='path to serve from',
                      default=None)
    parser.add_option('-q',
                      '--quiet',
                      action='store_true',
                      default=False,
                      help="Do not log unless it is critical")
    parser.add_option('-d',
                      '--debug',
                      action='store_true',
                      default=False,
                      help='upgrade logging from info to debug')
    options, args = parser.parse_args()

    if options.debug:
        tftpy.setLogLevel(logging.DEBUG)
    elif options.quiet:
        tftpy.setLogLevel(logging.WARN)
    else:
        tftpy.setLogLevel(logging.INFO)

    if not options.root:
        parser.print_help()
        sys.exit(1)

    server = tftpy.TftpServer(options.root)
    try:
        server.listen(options.ip, options.port)
    except tftpy.TftpException as err:
        sys.stderr.write("%s\n" % str(err))
        sys.exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
