#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import sys
import pyqtuidoc
from argparse import ArgumentParser
import logging
from . import compileUi, loadUi

PROG = 'qtuidocmake'

class Driver(object):
    """ This encapsulates access to the pyuic functionality so that it can be
    called by code that is Python v2/v3 specific.
    """

    LOGGER_NAME = 'PyQt5.uic'

    def __init__(self, opts, ui_file):
        """ Initialise the object.  opts is the parsed options.  ui_file is the
        name of the .ui file.
        """

        if opts.debug:
            logger = logging.getLogger(self.LOGGER_NAME)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        self._opts = opts
        self._ui_file = ui_file

    def invoke(self):
        """ Generate the Python code. """

        needs_close = False

        if sys.hexversion >= 0x03000000:
            if self._opts.output == '-':
                from io import TextIOWrapper

                pyfile = TextIOWrapper(sys.stdout.buffer, encoding='utf8')
            else:
                pyfile = open(self._opts.output, 'wt', encoding='utf8')
                needs_close = True
        else:
            if self._opts.output == '-':
                pyfile = sys.stdout
            else:
                pyfile = open(self._opts.output, 'wt')
                needs_close = True

        import_from = self._opts.import_from

        if import_from:
            from_imports = True
        elif self._opts.from_imports:
            from_imports = True
            import_from = '.'
        else:
            from_imports = False

        compileUi(self._ui_file, pyfile, self._opts.execute, self._opts.indent,
                  from_imports, self._opts.resource_suffix, import_from)

        if needs_close:
            pyfile.close()
        return 0

    def on_IOError(self, e):
        """ Handle an IOError exception. """

        sys.stderr.write("Error: %s: \"%s\"\n" % (e.strerror, e.filename))

    def on_SyntaxError(self, e):
        """ Handle a SyntaxError exception. """

        sys.stderr.write("Error in input file: %s\n" % e)

    def on_NoSuchClassError(self, e):
        """ Handle a NoSuchClassError exception. """

        sys.stderr.write(str(e) + "\n")

    def on_NoSuchWidgetError(self, e):
        """ Handle a NoSuchWidgetError exception. """

        sys.stderr.write(str(e) + "\n")

    def on_Exception(self, e):
        """ Handle a generic exception. """

        if logging.getLogger(self.LOGGER_NAME).level == logging.DEBUG:
            import traceback

            traceback.print_exception(*sys.exc_info())
        else:
            from PyQt5 import QtCore

            sys.stderr.write("An unexpected error occurred. PyQt (%s)" % QtCore.PYQT_VERSION_STR)


def cli():
    parser = ArgumentParser(
        prog="%s" % PROG
    )
    group = parser.add_argument_group('paths and folders')
    group.add_argument(
        'path',
        metavar='path',
        help='path to video file'
    )
    group.add_argument(
        "-p", "--preview",
        dest="preview",
        action="store_true",
        default=False,
        help="show a preview of the UI instead of generating code"
    )
    group.add_argument(
        "-o", "--output",
        dest="output",
        default="-",
        metavar="FILE",
        help="write generated code to FILE instead of stdout"
    )
    group.add_argument(
        "-x", "--execute",
        dest="execute",
        action="store_true",
        default=False,
        help="generate extra code to test and display the class"
    )
    group.add_argument(
        "-d", "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="show debug output"
    )
    group.add_argument(
        "-i", "--indent",
        dest="indent",
        action="store",
        type=int,
        default=4,
        metavar="N",
        help="set indent width to N spaces, tab if N is 0 [default: 4]"
    )

    group = parser.add_argument_group('other')
    group.add_argument(
        "--import-from",
        dest="import_from",
        metavar="PACKAGE",
        help="generate imports of pyrcc5 generated modules in the style 'from PACKAGE import ...'"
    )
    group.add_argument(
        "--from-imports",
        dest="from_imports",
        action="store_true",
        default=False, help="the equivalent of '--import-from=.'"
    )
    group.add_argument(
        "--resource-suffix",
        dest="resource_suffix",
        action="store",
        default="_rc",
        metavar="SUFFIX",
        help="append SUFFIX to the basename of resource files [default: _rc]"
    )
    group.add_argument(
        '-v', '--verbose',
        action='count',
        default=1,
        help='-v show progress, -vv show debug'
    )
    group.add_argument(
        '-V', '--version',
        action='version',
        version='%s %s' % (PROG, pyqtuidoc.__version__),
        help='show version and exit'
    )

    return parser


def main(*args, **kwargs):
    parser = cli(*args, **kwargs)
    opts = parser.parse_args()
    opts.verbose = 40 - (10 * opts.verbose) if opts.verbose > 0 else 0
    logging.basicConfig(level=opts.verbose, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    #opts = vars(opts)
    logging.debug('Running with options:\n%s' % repr(opts))
    #del opts['verbose']
    driver = Driver(opts, opts.path)

    exit_status = 1

    try:
        exit_status = driver.invoke()

    except IOError as e:
        driver.on_IOError(e)

    except SyntaxError as e:
        driver.on_SyntaxError(e)

    except NoSuchClassError as e:
        driver.on_NoSuchClassError(e)

    except NoSuchWidgetError as e:
        driver.on_NoSuchWidgetError(e)

    except Exception as e:
        driver.on_Exception(e)

    sys.exit(exit_status)

if __name__ == '__main__':
    main()
