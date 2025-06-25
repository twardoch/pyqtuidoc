#!/usr/bin/env python
""" """

import logging
import os
import sys
from argparse import ArgumentParser
from collections import OrderedDict

from PyQt5 import QtWidgets, uic

import pyqtuidoc

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakemods"))

PROG = "qtuidocmake"


def cli():
    parser = ArgumentParser(prog="%s" % PROG)
    group = parser.add_argument_group("paths and folders")
    group.add_argument("path", metavar="path", help="path to video file")
    group.add_argument(
        "-p",
        "--preview",
        dest="preview",
        action="store_true",
        default=False,
        help="show a preview of the UI instead of generating code",
    )
    group.add_argument(
        "-o",
        "--output",
        dest="output",
        default="-",
        metavar="FILE",
        help="write generated code to FILE instead of stdout",
    )
    group.add_argument(
        "-x",
        "--execute",
        dest="execute",
        action="store_true",
        default=False,
        help="generate extra code to test and display the class",
    )
    group.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="show debug output",
    )
    group.add_argument(
        "-i",
        "--indent",
        dest="indent",
        action="store",
        type=int,
        default=4,
        metavar="N",
        help="set indent width to N spaces, tab if N is 0 [default: 4]",
    )

    group = parser.add_argument_group("other")
    group.add_argument(
        "--import-from",
        dest="import_from",
        metavar="PACKAGE",
        help="generate imports of pyrcc5 generated modules in the style 'from PACKAGE import ...'",
    )
    group.add_argument(
        "--from-imports",
        dest="from_imports",
        action="store_true",
        default=False,
        help="the equivalent of '--import-from=.'",
    )
    group.add_argument(
        "--resource-suffix",
        dest="resource_suffix",
        action="store",
        default="_rc",
        metavar="SUFFIX",
        help="append SUFFIX to the basename of resource files [default: _rc]",
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        help="-v show progress, -vv show debug",
    )
    group.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{PROG} {pyqtuidoc.__version__}",
        help="show version and exit",
    )

    return parser


def dumpQObject(qobject):
    OrderedDict()
    # if 'toolTip' in


def dumpQObjectTree(qobject, level=0):
    """
    A helper function for printing the tree view of QObjects. Qt offers a similar function, but
    it is only available if Qt was a debug build.
    Args:
        qobject[QObject]: The object to dump the tree.
        level[int]: The indent level.
    """

    if level == 0:
        print("+ " + qobject.objectName() + " (" + str(type(qobject)) + ")")

    children = qobject.children()
    n = len(children)
    for i in range(n):
        child = children[i]

        if i == 0:
            print("|  " * (level + 1))
            prefix = "|  " * (level) + "+--"
        else:
            print("|  " * (level + 2))
            prefix = "|  " * (level + 1)

        print(prefix + "+ " + child.objectName() + " (" + dumpQObject(qobject) + ")")
        dumpQObjectTree(child, level + 1)


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self, uipath):
        super().__init__()
        self.ui = uic.loadUi(uipath, self)
        # self.show()


def main(*args, **kwargs):
    parser = cli(*args, **kwargs)
    opts = parser.parse_args()
    opts.verbose = 40 - (10 * opts.verbose) if opts.verbose > 0 else 0
    logging.basicConfig(
        level=opts.verbose,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    opts = vars(opts)
    logging.debug("Running with options:\n%s" % repr(opts))
    del opts["verbose"]

    QtWidgets.QApplication(sys.argv)
    w = AppWindow(opts["path"])
    print(dir(w))
    help(w)
    # dumpQObjectTree(w)
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()
