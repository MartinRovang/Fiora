"""
This is the main entry point of the application.
"""

import coloredlogs, logging, verboselogs
coloredlogs.install()
verboselogs.install()
import os
import sys
import click
from fiora import __version__
from rich.console import Console
from rich.progress import track
import time
from rich.prompt import Prompt
import glob
import fiora.vars_and_path as vp
import fiora.suit_generator as sg
import fiora.suit_tester as st
import json

__author__ = "Martin Soria Røvang"
__copyright__ = "Martin Soria Røvang"
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
# validate option takes two string arguments name of suite and path to target data
@click.option(
    "--validate",
    help="Use a test suite to validate on a target data example: validate suite_name path_to_target_data",
    nargs=2,
    type=click.STRING,
    default=None,
)
# custom_test option takes one string arguments name of test
@click.option(
    "--custom_test",
    help="Create a custom test: custom_test test_name",
    nargs=1,
    type=click.STRING,
    default=None,
)
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
        # log
        _logger.info("Building directory structure")
        os.makedirs(f"{vp.module_folder_name}", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/test_suites", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/test_suites/reports", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/validations", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/validations/reports", exist_ok=True)
        os.makedirs(f"{vp.module_folder_name}/custom_tests", exist_ok=True)
        # log
        _logger.info("Completed")

    if kwargs["suite"]:
        if kwargs["suite"] != "new":
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
                    suite = sg.FioraSuiteGenerator(all_files_nii_compressed, suitename, _logger)
                    suite.catch_metrics()
                    suite.create_suite()
                    _logger.info("Complete")
            else:
                _logger.error("Path does not exist")
                return
    
    if kwargs["custom_test"]:
        output = '''
from typing import Union

class MeanValues: #<--- Change the name of your test
    """Tests or gathers the mean values of the data, for both the test and reference data"""
    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = [] #<--- This is where the individual values from the data are stored
    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"] #<--- This is the data that is passed to the metrics
        mean_val = np.mean(data) # <--- Change this line to your test metric
        self.memory.append(mean_val) #<--- This is where the individual metrics are stored
    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}} #<--- This is where the test critera is defined
    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"] #<--- This is the data that is passed to the metrics
        suite = kwargs["suite"] #<--- This is the suite that defines the test criteria
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.mean(data),3)) #<--- This is where the test metric for the target data is defined
            if suite[self.__class__.__name__]["min"] <= self.test_val <= suite[self.__class__.__name__]["max"]: #<--- This is where the test criteria is made
                return True
            else:
                return False
        else:
            return "N/A"'''
        with open(f"{vp.module_folder_name}/custom_tests/{kwargs['custom_test']}_fioraT.py", "w") as f:
            f.write(output)
        _logger.success(f"Custom test added {vp.module_folder_name}/{kwargs['custom_test']}_fioraT.py, please edit the file to your needs. File must end with _fioraT.py")

    if kwargs["validate"]:
        path_to_data = kwargs["validate"][1]
        if os.path.exists(path_to_data):
            all_files_nii_compressed = glob.glob(os.path.join(path_to_data, "*.nii.gz"))
            if len(all_files_nii_compressed) == 0:
                _logger.error("No files found in path")
                return
            else:
                # log how many found
                _logger.info(f"Found {len(all_files_nii_compressed)} file(s) to be tested with suite {kwargs['validate'][0]}")
                name_of_suite = kwargs["validate"][0]
                if os.path.exists(f"{vp.module_folder_name}/test_suites/{name_of_suite}.json"):
                    _logger.info(f"Starting validation using suite: {name_of_suite}")
                    
                    # Validate a test suite
                    suite = st.DataTester(name_of_suite, all_files_nii_compressed, _logger)
                    results = suite.validate()

                    with open(f"{vp.module_folder_name}/validations/reports/{name_of_suite}_targetreport.json", "w") as f:
                        json.dump(suite.testing_values, f, indent=4)
                    with open(f"{vp.module_folder_name}/validations/reports/{name_of_suite}_suitereport.json", "w") as f:
                        json.dump(results, f, indent=4)
                    # count number of failed tests
                    num_failed = 0
                    num_of_tests = 0
                    for key, value in results.items():
                        num_of_tests += 1
                        # if a dict
                        if isinstance(value, list):
                            for d in value:
                                for key2, value2 in d.items():
                                    if value2 == False:
                                        _logger.error(f"Test {key} failed for {key2}")
                                        num_failed += 1
                                    else:
                                        _logger.success(f"Test {key} passed for {key2}")
                        else:
                            if value == False:
                                num_failed += 1
                                _logger.error(f"Test {key} failed")
                            else:
                                _logger.success(f"Test {key} passed")
                    # logg the ones passed
                    _logger.info(f"Number of tests passed: {num_of_tests - num_failed}/{num_of_tests}")
                else:
                    _logger.error("Suite does not exist")
                    return

if __name__ == "__main__":
    main()
