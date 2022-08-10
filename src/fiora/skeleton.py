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


import logging
import os
import sys
import click
from fiora import __version__
from rich.console import Console
from rich.progress import track
import fiora.fiora_profiler as fp
import fiora.fiora_validate as fv
import time
import mypy
from rich.prompt import Prompt
import glob
import uuid
import yaml

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
        console.print("Initializing the project", style="bold cyan")
        # Initialize the project
        # Make directory structure
        console.print("Building directory structure", style="bold cyan")
        os.makedirs("Fiora_strc", exist_ok=True)
        os.makedirs("Fiora_strc/test_suites", exist_ok=True)
        os.makedirs("Fiora_strc/datafiles", exist_ok=True)
        os.makedirs("Fiora_strc/test_suites/reports", exist_ok=True)
        os.makedirs("Fiora_strc/validations", exist_ok=True)
        os.makedirs("Fiora_strc/validations/reports", exist_ok=True)
        console.print("Completed \U0001F970 \U0001F60D", style="bold cyan")

    if kwargs["datasource"]:
        if kwargs["datasource"] != "new":
            console.print("Invalid command for datasource", style="bold red")
        else:
            datapath = Prompt.ask("""Insert path to data folder (abspath)""")
            if os.path.isdir(datapath):
                console.print(
                    f"Connecting to data folder: {datapath}", style="bold cyan"
                )
                all_files_nii_compressed = glob.glob(os.path.join(datapath, "*.nii.gz"))
                all_files_nii = glob.glob(os.path.join(datapath, "*.nii"))
                all_files_dcm = glob.glob(os.path.join(datapath, "*.dcm"))
                N_nifty_compressed = len(all_files_nii_compressed)
                N_nifty = len(all_files_nii)
                N_dcm = len(all_files_dcm)
                total = N_nifty_compressed + N_nifty + N_dcm
                if total == 0:
                    console.print("No files found", style="bold red")
                    return
                if N_nifty_compressed > 0:
                    data_type = "nii.gz"
                    console.print(
                        f"Found {N_nifty_compressed} compressed nifty files",
                        style="bold cyan",
                    )

                if N_nifty > 0:
                    data_type = "nii"
                    console.print(f"Found {N_nifty} nifty file(s)", style="bold cyan")

                if N_dcm > 0:
                    data_type = "dcm"
                    console.print(f"Found {N_dcm} dcm files", style="bold cyan")

                if N_nifty_compressed > 0 and N_nifty > 0 and N_dcm > 0:
                    console.print(
                        f"Datafolder contains different data types, please ensure it only contains one type.",
                        style="bold cyan",
                    )
                    return
                else:
                    data_id = str(uuid.uuid4())
                    with open(f"Fiora_strc/datafiles/{data_id}.yml", "w") as f:
                        f.write(
                            f"""
testing_pipeline:
    path: {datapath}
    type: {data_type}
                        """
                        )
                console.print(
                    f"ID: {data_id}, Insert this id in the test suite setup.",
                    style="bold cyan",
                )
                console.print(f"Complete \U0001F970 \U0001F60D", style="bold cyan")
            else:
                console.print("Invalid path", style="bold red")

    if kwargs["suite"]:
        if kwargs["suite"] != "new":
            console.print("Invalid command for suite", style="bold red")
        else:
            data_id = Prompt.ask("""Insert id from the datasource setup""")
            suitename = Prompt.ask("""Give a name of your test suite""")
            if os.path.isfile(f"Fiora_strc/datafiles/{data_id}.yml"):
                console.print(f"Connecting datafile: {data_id}", style="bold cyan")
                yaml_file = yaml.safe_load(
                    open(f"Fiora_strc/datafiles/{data_id}.yml", "r")
                )
                console.print(f"Complete \U0001F970 \U0001F60D", style="bold cyan")
                console.print(f"Starting data profiling", style="bold cyan")
                data_path = yaml_file["testing_pipeline"]["path"]
                test_suite = fp.FioraProfiler(
                    data_path=data_path,
                    filetype=yaml_file["testing_pipeline"]["type"],
                    suitename=suitename,
                    data_id=data_id,
                )
                test_suite.create_general_profile()
                console.print(f"Complete \U0001F970 \U0001F60D", style="bold cyan")
                console.print(f"Making test suite report", style="bold cyan")
                test_suite.make_report()
                console.print(f"Complete \U0001F970 \U0001F60D", style="bold cyan")
            else:
                console.print("Invalid id", style="bold red")

    if kwargs["validate"]:
        path_to_data = kwargs["validate"][2]
        if os.path.exists(path_to_data):
            name_of_suite = kwargs["validate"][1]
            if os.path.exists(f"Fiora_strc/test_suites/{name_of_suite}.json"):
                console.print(f"Starting validation", style="bold cyan")
                results, id = fv.validate(path_to_data, name_of_suite)
                console.print(f"Id of validation test {id}", style="bold cyan")
                console.print(results, style="bold cyan")
                # count the number of false results and true results
                false_results = 0
                true_results = 0
                for cat in results:
                    # if is dict
                    if isinstance(results[cat], dict):
                        for key in results[cat]:
                            if results[cat][key] == False:
                                false_results += 1
                            else:
                                true_results += 1
                    else:
                        if results[cat] == False:
                            false_results += 1
                        else:
                            true_results += 1
                console.print(f"{false_results} Tests failed.", style="bold cyan")
                console.print(f"{true_results} Tests passed.", style="bold cyan")
                return results, id
            else:
                console.print("test suite does not exist", style="bold red")
                return
        else:
            console.print("data path does not exist", style="bold red")
            return
    #     print(kwargs["validate"])
    # _logger.debug("Starting crazy calculations...")

    # _logger.info("Script ends here")


if __name__ == "__main__":
    main()
