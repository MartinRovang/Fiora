import json
import os
import numpy as np
import mypy
import glob
from src.fiora.ascii_design import DESIGN


class ReportMaker:
    """Class to report the results of the test suite into markdown or other types"""

    def __init__(self, suitename) -> None:
        self.suitename = suitename

    def load_json(self, json_path):
        """
        Load the json file
        """
        with open(json_path, "r") as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file

    def generate_report_markdown(self):
        """Generate the report in markdown format"""
        json_path = f"Fiora_strc/test_suites/{self.suitename}.json"
        json_file = self.load_json(json_path)
        markdown_document = """<center>\n\n"""
        for key in json_file[self.suitename]:
            if key == "distribution":
                markdown_document += "|Quantile | Min value | Max value|\n"
                markdown_document += "|-|-|-\n"
                for metric_type in json_file[self.suitename][key]:
                    markdown_document += f"| {metric_type} | {json_file[self.suitename][key][metric_type]['min']} | {json_file[self.suitename][key][metric_type]['max']}\n"
                markdown_document += "\n---\n"

            if key == "mean":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]
                markdown_document += f"mean must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"

            if key == "max_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"maximum value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"

            if key == "min_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"minimum value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"

            if key == "percentage_foreground":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"percentage of foreground value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"

            if key == "num_nans":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f"Total number of nans `{total}`\n"
                markdown_document += "\n---\n"

            if key == "num_infs":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f"Total number of infs `{total}`\n"
                markdown_document += "\n---\n"

            if key == "types":
                all_types = json_file[self.suitename][key]["unique_types"]
                markdown_document += "Types: "
                for typ_ in all_types:
                    markdown_document += (
                        f"""<span style="background-color: #0000FF">{typ_}</span>"""
                    )
                markdown_document += "\n---\n"

        # save as markdown file
        with open(
            f"Fiora_strc/test_suites/reports/{self.suitename}.md", "w"
        ) as outfile:
            outfile.write(markdown_document)

    def test_mean(self, json_ref, json_test):
        """
        Test the mean of the test suite
        """
        mean_ref = json_ref["mean"]
        mean_test = json_test["mean"]
        if mean_ref["max"] >= mean_test["max"] and mean_ref["min"] <= mean_test["min"]:
            return True
        else:
            return False

    def test_max_values(self, json_ref, json_test):
        """
        Test the max values of the test suite
        """
        max_values_ref = json_ref["max_values"]
        max_values_test = json_test["max_values"]
        if (
            max_values_ref["max"] >= max_values_test["max"]
            and max_values_ref["min"] <= max_values_test["min"]
        ):
            return True
        else:
            return False

    def test_min_values(self, json_ref, json_test):
        """
        Test the min values of the test suite
        """
        min_values_ref = json_ref["min_values"]
        min_values_test = json_test["min_values"]
        if (
            min_values_ref["max"] >= min_values_test["max"]
            and min_values_ref["min"] <= min_values_test["min"]
        ):
            return True
        else:
            return False

    def test_percentage_foreground(self, json_ref, json_test):
        """
        Test the percentage of foreground value of the test suite
        """
        percentage_foreground_ref = json_ref["percentage_foreground"]
        percentage_foreground_test = json_test["percentage_foreground"]
        if (
            percentage_foreground_ref["max"] >= percentage_foreground_test["max"]
            and percentage_foreground_ref["min"] <= percentage_foreground_test["min"]
        ):
            return True
        else:
            return False

    def test_num_nans(self, json_ref, json_test):
        """
        Test the number of nans of the test suite
        """
        num_nans_ref = json_ref["num_nans"]
        num_nans_test = json_test["num_nans"]
        if num_nans_ref["total"] == num_nans_test["total"]:
            return True
        else:
            return False

    def test_num_infs(self, json_ref, json_test):
        """
        Test the number of infs of the test suite
        """
        num_infs_ref = json_ref["num_infs"]
        num_infs_test = json_test["num_infs"]
        if num_infs_ref["total"] == num_infs_test["total"]:
            return True
        else:
            return False

    def test_types(self, json_ref, json_test):
        """
        Test the types of the test suite
        """
        types_ref = json_ref["types"]
        types_test = json_test["types"]
        if types_ref["unique_types"] == types_test["unique_types"]:
            return True
        else:
            return False

    def test_distribution(self, dist_metric_ref, dist_metric_test):
        """
        Test the distribution of the test suite
        """
        if (
            dist_metric_ref["max"] >= dist_metric_test["max"]
            and dist_metric_ref["min"] <= dist_metric_test["min"]
        ):
            return True
        else:
            return False

    def generate_report_markdown_validation(self, validation_id):
        """Generate the report markdown for the validation"""
        json_test = self.load_json(
            f"Fiora_strc/validations/{self.suitename}_{validation_id}.json"
        )
        json_ref = self.load_json(f"Fiora_strc/test_suites/{self.suitename}.json")
        markdown_document = f"""<center>
        {DESIGN}
        \n"""
        test_results_json = {}
        for key in json_ref[self.suitename]:
            if key == "distribution":
                test_results_json[key] = {}
                markdown_document += "|Test|Quantile | Min value | Max value|\n"
                markdown_document += "|-|-|-|-\n"
                for quantile_ref, quantile_test in zip(
                    json_ref[self.suitename][key], json_test[self.suitename][key]
                ):
                    test_result = self.test_distribution(
                        json_ref[self.suitename][key][quantile_ref],
                        json_test[self.suitename][key][quantile_test],
                    )
                    if test_result:
                        markdown_document += f"✅|{quantile_ref}|{json_ref[self.suitename][key][quantile_ref]['min']}|{json_ref[self.suitename][key][quantile_ref]['max']}|\n"
                    else:
                        markdown_document += f"❌|{quantile_ref}|{json_ref[self.suitename][key][quantile_ref]['min']}|{json_ref[self.suitename][key][quantile_ref]['max']}|\n"
                    test_results_json[key][quantile_ref] = test_result

                markdown_document += "\n---\n"

            if key == "mean":
                test_result = self.test_mean(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                if test_result:
                    markdown_document += f"✅ mean must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                else:
                    markdown_document += f"❌ mean must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "max_values":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_max_values(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ maximum values must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                else:
                    markdown_document += f"❌ maximum values must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "min_values":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_min_values(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ minimum values must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                else:
                    markdown_document += f"❌ minimum values must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"

                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "percentage_foreground":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_percentage_foreground(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ percentage of foreground must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                else:
                    markdown_document += f"❌ percentage of foreground must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "num_nans":
                total = json_ref[self.suitename][key]["total"]
                test_result = self.test_num_nans(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ number of nans must be `{total}`\n"
                else:
                    markdown_document += f"❌ number of nans must be `{total}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "num_infs":
                total = json_ref[self.suitename][key]["total"]
                test_result = self.test_num_infs(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ number of infs must be `{total}`\n"
                else:
                    markdown_document += f"❌ number of infs must be `{total}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"

            if key == "types":
                unique_types = json_ref[self.suitename][key]["unique_types"]
                test_result = self.test_types(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                markdown_document += "Types: "
                for typ_ in unique_types:
                    markdown_document += (
                        f"""<span style="background-color: #0000FF">{typ_}</span>"""
                    )
                if test_result:
                    markdown_document += f"✅ unique types must be `{unique_types}`\n"
                else:
                    markdown_document += f"❌ unique types must be `{unique_types}`\n"
                test_results_json[key] = test_result
                markdown_document += "\n---\n"
        markdown_document += "</center>"
        # save as markdown file
        with open(
            f"Fiora_strc/validations/reports/{self.suitename}_{validation_id}.md",
            "w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(markdown_document)

        return test_results_json
