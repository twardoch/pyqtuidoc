#!/usr/bin/env python
"""
Command-line interface for pyqtuidoc.
"""

import argparse
import importlib.metadata
import logging
import sys

from PyQt5 import QtWidgets, uic

# The fakemods import was handled by sys.path manipulation.
# This should be resolved with proper packaging if fakemods are necessary.
# For now, assuming they might be part of a test setup or older structure.
# The original `sys.path.append` is removed.

PROG = "qtuidocmake"


def cli() -> argparse.ArgumentParser:
    """
    Configures and returns the argument parser for the CLI.
    """
    parser = argparse.ArgumentParser(prog=f"{PROG}")
    group = parser.add_argument_group("paths and folders")
    group.add_argument("path", metavar="path", help="path to .ui file")
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
        help=(
            "generate imports of pyrcc5 generated modules in the style "
            "'from PACKAGE import ...'"
        ),
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
        version=f"{PROG} {importlib.metadata.version('pyqtuidoc')}",
        help="show version and exit",
    )

    return parser


# def dump_q_object(qobject: Any) -> Optional[OrderedDict[Any, Any]]:
# Renamed and type hinted
#     """Dumps QObject properties. Currently unused."""
#     # rep = OrderedDict() # Unused variable
#     # if 'toolTip' in ...: # Original code was incomplete
#     return None # Placeholder, as original was incomplete and unused


# def dump_q_object_tree( # Renamed and type hinted
#     qobject: Any, level: int = 0
# ) -> None:
#     """
#     A helper function for printing the tree view of QObjects.
#     Qt offers a similar function, but it is only available if Qt was a debug build.
#     Args:
#         qobject: The object to dump the tree.
#         level: The indent level.
#     """
#     # This function seems to be for debugging and uses print extensively.
#     # It's not directly used by the core logic. Commenting out for now.
#     # We can re-introduce it with proper logging if needed.
#
#     # if level == 0:
#     #     logging.debug(
#     #         f"+ {qobject.objectName()} ({type(qobject)})"  # type: ignore
#     #      )
#
#     # children = qobject.children() # type: ignore
#     # for i, child in enumerate(children):
#     #     if i == 0:
#     #         logging.debug(f"{'|  ' * (level + 1)}")
#     #         prefix = f"{'|  ' * level}+--"
#     #     else:
#     #         logging.debug(f"{'|  ' * (level + 2)}")
#     #         prefix = f"{'|  ' * (level + 1)}"
#
#     #     # Assuming dump_q_object would return a string representation
#     #     obj_details = dump_q_object(qobject)
#     #     logging.debug(
#     #         f"{prefix}+ {child.objectName()} ({obj_details})"  # type: ignore
#     #     )
#     #     dump_q_object_tree(child, level + 1)


# class AppWindow(QtWidgets.QMainWindow):
#     def __init__(self, uipath: str) -> None:
#         super().__init__()
#         self.ui = uic.loadUi(uipath, self)  # type: ignore[attr-defined]
#         # self.show()


def setup_logging(verbosity: int, debug_mode: bool) -> None:
    """Configures logging based on verbosity and debug mode."""
    log_level = logging.WARNING  # Default
    if debug_mode:  # Explicit debug flag takes precedence
        log_level = logging.DEBUG
    elif verbosity == 0:  # No -v flags
        log_level = logging.ERROR
    elif verbosity == 1:  # -v
        log_level = logging.WARNING
    elif verbosity == 2:  # -vv
        log_level = logging.INFO
    elif verbosity >= 3:  # -vvv or more
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """
    Main entry point for the qtuidocmake CLI.
    """
    parser = cli()
    parsed_args = parser.parse_args()  # type: argparse.Namespace

    setup_logging(parsed_args.verbose, parsed_args.debug)

    logging.debug(f"Running with options: {parsed_args!r}")

    if parsed_args.preview:
        if hasattr(parsed_args, "path") and parsed_args.path:
            _app = QtWidgets.QApplication(sys.argv)

            class PreviewAppWindow(QtWidgets.QMainWindow):
                def __init__(self, uipath_str: str) -> None:
                    super().__init__()
                    uic.loadUi(uipath_str, self)
                    self.show()

            _window = PreviewAppWindow(parsed_args.path)  # noqa: F841 (unused variable)
            sys.exit(_app.exec_())
        else:
            logging.error("No UI file path provided for preview.")
            parser.print_help()
            sys.exit(1)
    elif hasattr(parsed_args, "path") and parsed_args.path:
        logging.info(f"Processing UI file: {parsed_args.path}")
        try:
            # Placeholder for actual uic.compileUi or other processing logic
            # from PyQt5.uic import compileUi
            # Example:
            # with open(
            #    parsed_args.output if parsed_args.output != "-" else sys.stdout, "w"
            # ) as f:
            #     compileUi(
            #         parsed_args.path,
            #         f,
            #         execute=parsed_args.execute,
            #         indent=parsed_args.indent,
            #         import_from=parsed_args.import_from,
            #         from_imports=parsed_args.from_imports,
            #         resource_suffix=parsed_args.resource_suffix
            #     )

            output_content = (
                f"# TODO: Implement .ui processing for {parsed_args.path}\n"
                f"# Options: {parsed_args!r}\n"
            )
            if parsed_args.output == "-":
                sys.stdout.write(output_content)
            else:
                with open(
                    parsed_args.output, "w", encoding="utf-8"
                ) as output_file:
                    output_file.write(output_content)
                logging.info(
                    f"Placeholder output written to {parsed_args.output}"
                )
            logging.info("UI processing logic needs to be implemented.")

        except FileNotFoundError:
            logging.error(f"UI file not found: {parsed_args.path}")
            sys.exit(1)
        except (OSError, RuntimeError) as e:  # Catch more specific exceptions
            logging.error(f"An error occurred during UI processing: {e!s}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
