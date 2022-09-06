"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = fiora.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""


import coloredlogs, logging
coloredlogs.install()
import os
import sys
import click
from fiora import __version__
from rich.console import Console
from rich.progress import track
import time
from rich.prompt import Prompt
import glob
import uuid
import yaml
import fiora.vars_and_path as vp
import fiora.suit_generator as sg
import fiora.suit_tester as st
import json

__author__ = "Martin RÃ¸vang"
__copyright__ = "Martin RÃ¸vang"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


@click.command()
@click.option("--init", help="Initialize the project", is_flag=True, default=False)
@click.option(
    "--datasource", help="Add reference data", type=click.STRING, default=None
)
@click.option(
    "--suite", help="Create a new test suite", type=click.STRING, default=None
)
@click.option(
    "--vv",
    default=logging.INFO,
    help="Enable debug logging",
    is_flag=True,
    flag_value=logging.DEBUG,
)
@click.option("--version", help="Version of the app", is_flag=True, default=False)
@click.argument("validate", nargs=3, default=None, required=False)
def main(**kwargs):
    """
    Console script for fiora.

    Argparse:
        --init: Initialize the project

        --datasource: Add reference data

        --suite: Create a new test suite

        --vv: Enable debug logging

        --version: Version of the app

        validate: Validate a test suite [NAME_OF_SUITE] [PATH_TO_DATA]
    """
    setup_logging(kwargs["vv"])
    console = Console()

    if kwargs["version"]:
        print("Fiora version: ", __version__)
        return

    if kwargs["init"]:
        console.print(
            """
 ______   __     ______     ______     ______    
/\  ___\ /\ \   /\  __ \   /\  == \   /\  __ \   
\ \  __\ \ \ \  \ \ \/\ \  \ \  __<   \ \  __ \  
 \ \_\    \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\ 
  \/_/     \/_/   \/_____/   \/_/ /_/   \/_/\/_/ 
                                                 
""",
            style="bold red",
        )
        time.sleep(0.5)
        # log
        _logger.info("Initializing the project")
        # Initialize the project
        # Make directory structure
        console.print("Building directory structure", style="bold cyan")
        # log
        _logger.info("Building directory structure")
        os.makedirs(f"{vp.module_folder_name}", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/test_suites", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/test_suites/reports", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/validations", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/validations/reports", exist_ok=True)
        # log
        _logger.info("Completed")

    if kwargs["suite"]:
        if kwargs["suite"] != "new":
            console.print("Invalid command for suite", style="bold red")
            _logger.error("Invalid command for suite")
        else:
            data_path = Prompt.ask("""Insert path the suite will be based on (Only works for nii.gz files)""")
            #check if exists
            if os.path.exists(data_path):
                all_files_nii_compressed = glob.glob(os.path.join(data_path, "*.nii.gz"))
                # feedback how many files
                # log
                _logger.info(f"Found {len(all_files_nii_compressed)} files")
                suitename = Prompt.ask("""Give a name of your test suite""")
                _logger.info("Creating test suite")

                # Create a new test suite

                if len(all_files_nii_compressed) == 0:
                    _logger.error("No files found in path")
                    return
                else:
                    _logger.info("Complete")
                    _logger.info("Starting data profiling")
                    suite = sg.FioraSuiteGenerator(all_files_nii_compressed, suitename)
                    suite.catch_metrics()
                    suite.create_suite()
                    _logger.info("Complete")
            else:
                console.print("Path does not exist", style="bold red")
                _logger.error("Path does not exist")
                return

    if kwargs["validate"]:
        path_to_data = kwargs["validate"][2]
        if os.path.exists(path_to_data):
            all_files_nii_compressed = glob.glob(os.path.join(path_to_data, "*.nii.gz"))
            if len(all_files_nii_compressed) == 0:
                _logger.error("No files found in path")
                return
            else:
                # log how many found
                _logger.info(f"Found {len(all_files_nii_compressed)} file(s) to be tested with suite {kwargs['validate'][1]}")
                name_of_suite = kwargs["validate"][1]
                if os.path.exists(f"{vp.module_folder_name}/test_suites/{name_of_suite}.json"):
                    _logger.info("Starting validation")
                    _logger.info(f"Id of validation test {id}")
                    
                    # Validate a test suite
                    suite = st.DataTester(name_of_suite, all_files_nii_compressed)
                    results = suite.validate()
                    _logger.info("Complete")
                    # log results
                    _logger.info(f"Results: {results}")
                else:
                    _logger.error("Suite does not exist")
                    return


                
                


if __name__ == "__main__":
    main()
