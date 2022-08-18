import nibabel as nib
import os
import json
from rich.progress import track
import fiora.generate_report as gr
from fiora.metrics import MetricBase


class FioraProfiler:
    """The profiler used to analyze the data and generate the tests metrics."""

    def __init__(self, data_path, filetype, suitename, data_id):
        self.data_path = data_path
        self.filetype = filetype
        self.suitename = suitename
        self.data_id = data_id
        self.report_gen = gr.ReportMaker(self.suitename)

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


def get_general_profile(data_path, name):
    """Get the general profile of the data."""
    files = [x for x in os.listdir(data_path)]
    metric_base = MetricBase(name)

    for file in track(files, description="Profiling files", total=len(files)):
        data, affine = FioraProfiler.get_files_nifty(os.path.join(data_path, file))

        metric_base.get_types(data)
        metric_base.get_max_value(data)
        metric_base.get_min_value(data)
        metric_base.get_shapes(data)
        metric_base.get_mean(data)
        metric_base.get_distribution(data)
        metric_base.get_percentage_foreground(data)
        metric_base.get_num_nans(data)
        metric_base.get_num_infs(data)
        metric_base.get_orientation_correlation(data)


    json_suite_test_file = metric_base.create_json()

    return json_suite_test_file
