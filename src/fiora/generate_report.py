import json
import os
import numpy as np
import mypy
import glob
from fiora.report_handler import ReportHandler


class ReportMaker:
    """Class to report the results of the test suite into markdown or other types"""

    def __init__(self, suitename) -> None:
        self.suitename = suitename
        self.json_ref = self.load_json(f"Fiora_strc/test_suites/{self.suitename}.json")

    def load_json(self, json_path):
        """
        Load the json file
        """
        with open(json_path, "r") as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file

    def test_mean(self, json_ref, json_test):
        """
        Test the mean of the test suite
        """
        mean_ref = json_ref["mean"]
        mean_test = json_test["mean"]
        return (
            mean_ref["max"] >= mean_test["max"] and mean_ref["min"] <= mean_test["min"]
        )

    def test_max_values(self, json_ref, json_test):
        """
        Test the max values of the test suite
        """
        max_values_ref = json_ref["max_values"]
        max_values_test = json_test["max_values"]
        return (
            max_values_ref["max"] >= max_values_test["max"]
            and max_values_ref["min"] <= max_values_test["min"]
        )

    def test_min_values(self, json_ref, json_test):
        """
        Test the min values of the test suite
        """
        min_values_ref = json_ref["min_values"]
        min_values_test = json_test["min_values"]
        return (
            min_values_ref["max"] >= min_values_test["max"]
            and min_values_ref["min"] <= min_values_test["min"]
        )

    def test_percentage_foreground(self, json_ref, json_test):
        """
        Test the percentage of foreground value of the test suite
        """
        percentage_foreground_ref = json_ref["percentage_foreground"]
        percentage_foreground_test = json_test["percentage_foreground"]
        return (
            percentage_foreground_ref["max"] >= percentage_foreground_test["max"]
            and percentage_foreground_ref["min"] <= percentage_foreground_test["min"]
        )

    def test_num_nans(self, json_ref, json_test):
        """
        Test the number of nans of the test suite
        """
        num_nans_ref = json_ref["num_nans"]
        num_nans_test = json_test["num_nans"]
        return num_nans_ref["total"] == num_nans_test["total"]

    def test_num_infs(self, json_ref, json_test):
        """
        Test the number of infs of the test suite
        """
        num_infs_ref = json_ref["num_infs"]
        num_infs_test = json_test["num_infs"]
        return num_infs_ref["total"] == num_infs_test["total"]

    def test_types(self, json_ref, json_test):
        """
        Test the types of the test suite
        """
        types_ref = json_ref["types"]
        types_test = json_test["types"]
        # if type value in test exist in reference value
        return set(types_ref.keys()).issubset(set(types_test.keys()))

    def test_distribution(self, dist_metric_ref, dist_metric_test):
        """
        Test the distribution of the test suite
        """
        return (
            dist_metric_ref["max"] >= dist_metric_test["max"]
            and dist_metric_ref["min"] <= dist_metric_test["min"]
        )

    def test_shape_ax1(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax1"]
        unique_shape_test = json_test["shapes_ax1"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        return set(B).issubset(set(A))

    def test_shape_ax2(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax2"]
        unique_shape_test = json_test["shapes_ax2"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        return set(B).issubset(set(A))

    def test_shape_ax3(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax3"]
        unique_shape_test = json_test["shapes_ax3"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        return set(B).issubset(set(A))

    def generate_report_markdown_validation(
        self, validation_id, data_path, output_report=True
    ):
        """Generate the report markdown for the validation"""
        self.json_test = self.load_json(
            f"Fiora_strc/validations/{self.suitename}_{validation_id}.json"
        )
        self.reporthandler = ReportHandler(
            data_path, self.json_ref, self.json_test, validation_id
        )

        self.reporthandler.generate_distribution()
        self.reporthandler.begin_table()
        self.reporthandler.generate_mean()
        self.reporthandler.generate_max_values()
        self.reporthandler.generate_min_values()
        self.reporthandler.generate_percentage_foreground()
        self.reporthandler.generate_num_nans()
        self.reporthandler.generate_num_infs()
        self.reporthandler.generate_types()
        self.reporthandler.generate_shape_ax1()
        self.reporthandler.generate_shape_ax2()
        self.reporthandler.generate_shape_ax3()
        self.reporthandler.end_table()

        if output_report:
            test_results_json = self.reporthandler.generate_report()
        else:
            test_results_json = self.reporthandler.generate_report_json()

        return test_results_json

    def generate_report_markdown(self):
        """Generate the report in markdown format"""
        json_path = f"Fiora_strc/test_suites/{self.suitename}.json"
        json_file = self.load_json(json_path)
        markdown_document = """<center><img src="https://github.com/MartinRovang/Fiora/blob/master/flc_design2022080460426.jpg?raw=true" width="100"> <br><br>"""
        for key in json_file[self.suitename]:
            markdown_document += "<hr><br>"

            if key == "distribution":
                markdown_document += """ 
                <table>
                <thead>
                    <tr class="header">
                        <th>Quantile</th>
                        <th>Min value</th>
                        <th>Max value</th>
                    </tr>
                </thead>
                <tbody>
                """
                i = 0
                for quantile_ref in json_file[self.suitename][key]:
                    i += 1
                    # if even
                    if i % 2 == 0:
                        markdown_document += f"""
                        <tr class="even">
                            <td>{quantile_ref}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["min"]}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["max"]}</td>
                        </tr>
                        """
                    # if odd
                    else:
                        markdown_document += f"""
                        <tr class="odd">
                            <td>{quantile_ref}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["min"]}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["max"]}</td>
                        </tr>
                        """

                markdown_document += """
                                </tbody>
                                </table>"""
                markdown_document += "</center><br>"

            if key == "mean":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]
                markdown_document += f'mean must be greater than or equal to <span style="background-color: #0000FF; color:white">{min_val}</span> and less than or equal to <span style="background-color: #0000FF; color:white">{max_val}</span>'

            if key == "max_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f'maximum value must be greater than or equal to <span style="background-color: #0000FF; color:white">{min_val}</span> and less than or equal to <span style="background-color: #0000FF; color:white">{max_val}</span>'

            if key == "min_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f'minimum value must be greater than or equal to <span style="background-color: #0000FF; color:white">{min_val}</span> and less than or equal to <span style="background-color: #0000FF; color:white">{max_val}</span>'

            if key == "percentage_foreground":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f'percentage of foreground value must be greater than or equal to <span style="background-color: #0000FF; color:white">{min_val}</span> and less than or equal to <span style="background-color: #0000FF; color:white">{max_val}</span>'

            if key == "num_nans":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f'Total number of nans <span style="background-color: #0000FF; color:white">{total}</span>'

            if key == "num_infs":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f'Total number of infs <span style="background-color: #0000FF; color:white">{total}</span>'

            if key == "types":
                all_types = json_file[self.suitename][key]["unique_types"]
                markdown_document += "Types: "
                for typ_ in all_types:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{typ_}</span> """

            if key == "shapes_ax1":
                unique_shapes = json_file[self.suitename][key]["unique_shapes"]
                markdown_document += "Shapes ax 1: "
                for shape_ in unique_shapes:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """

            if key == "shapes_ax2":
                unique_shapes = json_file[self.suitename][key]["unique_shapes"]
                markdown_document += "Shapes ax 2: "
                for shape_ in unique_shapes:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """

            if key == "shapes_ax3":
                unique_shapes = json_file[self.suitename][key]["unique_shapes"]
                markdown_document += "Shapes ax 3: "
                for shape_ in unique_shapes:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """

            # at the end
            markdown_document += "</hr><br>"

        # save as markdown file
        with open(
            f"Fiora_strc/test_suites/reports/{self.suitename}.html", "w"
        ) as outfile:
            outfile.write(markdown_document)
