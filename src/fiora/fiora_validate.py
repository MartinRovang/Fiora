from typing import Tuple
from unittest import result
import fiora.generate_report as gr
import fiora.fiora_profiler as fp
import json
import yaml
import uuid
import mypy
import rich
from rich.console import Console
import os

def validate(data_path, name_of_suite, output_report=True) -> Tuple[dict, str]:
    """
    Validate a test suite against a datafile.

    Parameters
    ----------
    data_path : str
        Path to the datafile.
    name_of_suite : str
        Name of the test suite.
    """
    with open(f"Fiora_strc/test_suites/{name_of_suite}.json", "r") as infile:
        reference_json = json.load(infile)
    data_id = reference_json["data_id"]
    yaml_file = yaml.safe_load(open(f"Fiora_strc/datafiles/{data_id}.yml", "r"))
    data_type = yaml_file["testing_pipeline"]["type"]
    json_target = fp.get_general_profile(data_path, name_of_suite, data_type)
    json_target["data_target"] = data_path
    validation_id = str(uuid.uuid4())

    if output_report:
        with open(f"Fiora_strc/validations/{name_of_suite}_{validation_id}.json", "w") as outfile:
            json.dump(json_target, outfile)
    reportmaker = gr.ReportMaker(name_of_suite)
    results = reportmaker.generate_report_markdown_validation(validation_id, data_path, output_report=output_report)

    return results, validation_id


def start_validation(path_to_data, name_of_suite, output_report=True) -> dict:
    """
    Start a validation test suite.
    """
    console = Console()
    if os.path.exists(path_to_data):
        if os.path.exists(f"Fiora_strc/test_suites/{name_of_suite}.json"):
            console.print(f"Starting validation", style="bold cyan")
            results, id = validate(path_to_data, name_of_suite, output_report=output_report)
            if output_report:
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
            # assert false_results == 0, "There are failed tests"
            if output_report:
                return results, id
            else:
                return results
        else:
            console.print("test suite does not exist", style="bold red")
            return
    else:
        console.print("data path does not exist", style="bold red")
        return