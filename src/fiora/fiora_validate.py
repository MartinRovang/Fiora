from typing import Tuple
from unittest import result
import src.fiora.generate_report as gr
import src.fiora.fiora_profiler as fp
import json
import yaml
import uuid
import mypy


def validate(data_path, name_of_suite) -> Tuple[dict, str]:
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
    with open(f"Fiora_strc/validations/{name_of_suite}_{validation_id}.json", "w") as outfile:
        json.dump(json_target, outfile)

    reportmaker = gr.ReportMaker(name_of_suite, data_path, validation_id)
    results = reportmaker.generate_report_markdown_validation(validation_id, data_path)

    return results, validation_id
