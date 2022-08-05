import nibabel as nib
import os
import numpy as np
import json
from rich.progress import track
import src.fiora.generate_report as gr


class FioraProfiler:
    """The profiler used to analyze the data and generate the tests metrics."""

    def __init__(self, data_path, filetype, suitename, data_id):
        self.data_path = data_path
        self.filetype = filetype
        self.suitename = suitename
        self.data_id = data_id
        self.report_gen = gr.ReportMaker(suitename)

    @staticmethod
    def get_files_nifty(path_to_file):
        """Get the files in the path_to_file."""
        nibfile = nib.load(path_to_file)
        data = nibfile.get_fdata()
        affine = nibfile.affine
        return data, affine

    def get_files_dcm(self, path_to_file):
        """Get the files in the path_to_file."""
        pass

    def save_json(self, json_file, json_path):
        """Save the json file."""
        with open(json_path, "w") as outfile:
            json.dump(json_file, outfile)

    def load_json(self, json_path):
        """Load the json file."""
        with open(json_path, "r") as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file

    def create_general_profile(self):
        """Create the general profile of the data."""
        # save json file
        json_path = f"Fiora_strc/test_suites/{self.suitename}.json"
        json_profile_results = get_general_profile(
            self.data_path, self.suitename, self.filetype
        )
        json_profile_results["data_id"] = str(self.data_id)

        self.save_json(json_profile_results, json_path)

    def make_report(self):
        """Make the report of the data."""
        self.report_gen.generate_report_markdown()


def get_general_profile(data_path, name, filetype):
    """Get the general profile of the data."""
    json_suite_test_file = {name: {}}
    files = [x for x in os.listdir(data_path) if x.endswith(filetype)]
    all_files_metrics = {
        "q_05": [],
        "q1": [],
        "median": [],
        "q3": [],
        "q_95": [],
        "mean": [],
        "max_value": [],
        "min_value": [],
        "percentage_foreground": [],
        "num_nans": [],
        "num_infs": [],
        "types": [],
    }

    for file in track(files, description="Profiling files", total=len(files)):
        data, affine = FioraProfiler.get_files_nifty(os.path.join(data_path, file))
        all_files_metrics["types"].append(str(data.dtype))

        all_files_metrics["max_value"].append(round(np.max(data.copy()), 3))
        all_files_metrics["min_value"].append(round(np.min(data.copy()), 3))

        foreground_values = (data.copy() > 0).astype("int").sum()
        background_values = (data.copy() <= 0).astype("int").sum()
        percentage_foreground = foreground_values / (
            foreground_values + background_values
        )
        nan_values = np.isnan(data.copy()).sum()
        inf_values = (data.copy() == np.inf).astype("int").sum()

        data = data.copy()[data.copy() != 0]
        q_05 = round(np.quantile(data.copy(), 0.05), 3)
        q1 = round(np.quantile(data.copy(), 0.25), 3)
        median = round(np.median(data.copy()), 3)
        q3 = round(np.quantile(data.copy(), 0.75), 3)
        q_95 = round(np.quantile(data.copy(), 0.95), 3)
        mean = round(np.mean(data.copy()), 3)
        # append to list
        all_files_metrics["q_05"].append(q_05)
        all_files_metrics["q1"].append(q1)
        all_files_metrics["median"].append(median)
        all_files_metrics["q3"].append(q3)
        all_files_metrics["q_95"].append(q_95)
        all_files_metrics["mean"].append(mean)
        all_files_metrics["percentage_foreground"].append(
            round(percentage_foreground, 3)
        )
        all_files_metrics["num_nans"].append(nan_values)
        all_files_metrics["num_infs"].append(inf_values)

    # add min and max for each category
    json_suite_test_file[name]["distribution"] = {
        "q_05": {
            "min": min(all_files_metrics["q_05"]),
            "max": max(all_files_metrics["q_05"]),
        },
        "q1": {
            "min": min(all_files_metrics["q1"]),
            "max": max(all_files_metrics["q1"]),
        },
        "median": {
            "min": min(all_files_metrics["median"]),
            "max": max(all_files_metrics["median"]),
        },
        "q3": {
            "min": min(all_files_metrics["q3"]),
            "max": max(all_files_metrics["q3"]),
        },
        "q_95": {
            "min": min(all_files_metrics["q_95"]),
            "max": max(all_files_metrics["q_95"]),
        },
    }
    json_suite_test_file[name]["mean"] = {
        "min": min(all_files_metrics["mean"]),
        "max": max(all_files_metrics["mean"]),
    }
    json_suite_test_file[name]["max_values"] = {
        "min": min(all_files_metrics["max_value"]),
        "max": max(all_files_metrics["max_value"]),
    }
    json_suite_test_file[name]["min_values"] = {
        "min": min(all_files_metrics["min_value"]),
        "max": max(all_files_metrics["min_value"]),
    }
    json_suite_test_file[name]["percentage_foreground"] = {
        "min": min(all_files_metrics["percentage_foreground"]),
        "max": max(all_files_metrics["percentage_foreground"]),
    }
    json_suite_test_file[name]["num_nans"] = {
        "total": int(sum(all_files_metrics["num_nans"]))
    }
    json_suite_test_file[name]["num_infs"] = {
        "total": int(sum(all_files_metrics["num_infs"]))
    }
    json_suite_test_file[name]["types"] = {
        "unique_types": list(np.unique(all_files_metrics["types"]))
    }

    return json_suite_test_file
