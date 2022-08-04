import json 
import os
import numpy as np
import mypy


class ReportMaker:
    """Class to report the results of the test suite into markdown or other types"""
    def __init__(self, suitename) -> None:
        self.suitename = suitename
    
    def load_json(self):
        with open(f'Fiora_strc/test_suites/{self.suitename}.json', 'r') as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file
    
    def generate_report_markdown(self):
        json_file = self.load_json()
        markdown_document = """"""
        for key in json_file[self.suitename]:
            if key == "distribution":
                markdown_document += "|Quantile | Min value | Max value|\n"
                markdown_document += "|-|-|-\n"
                for metric_type in json_file[self.suitename][key]:
                    markdown_document += f"| {metric_type} | {json_file[self.suitename][key][metric_type]['max']} | {json_file[self.suitename][key][metric_type]['min']}\n"
                markdown_document += "\n---\n"

            if key == "mean":
                max_val = json_file[self.suitename][key]['max']
                min_val = json_file[self.suitename][key]['min']
                markdown_document += f"mean must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"
            
            if key == "max_values":
                max_val = json_file[self.suitename][key]['max']
                min_val = json_file[self.suitename][key]['min']

                markdown_document += f"maximum value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"

            if key == "min_values":
                max_val = json_file[self.suitename][key]['max']
                min_val = json_file[self.suitename][key]['min']

                markdown_document += f"minimum value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"
            
            if key == "percentage_foreground":
                max_val = json_file[self.suitename][key]['max']
                min_val = json_file[self.suitename][key]['min']

                markdown_document += f"percentage of foreground value must be greater than or equal to `{min_val}` and less than or equal to `{max_val}`\n"
                markdown_document += "\n---\n"
            
            if key == "num_nans":
                total = json_file[self.suitename][key]['total']

                markdown_document += f"Total number of nans `{total}`\n"
                markdown_document += "\n---\n"
            
            if key == "num_infs":
                total = json_file[self.suitename][key]['total']

                markdown_document += f"Total number of infs `{total}`\n"
                markdown_document += "\n---\n"
            
            if key == "types":
                all_types = json_file[self.suitename][key]['unique_types']
                markdown_document += "Types: "
                for typ_ in all_types:
                    markdown_document += f"""<span style="background-color: #0000FF">{typ_}</span>"""
                markdown_document += "\n---\n"

        # save as markdown file
        with open(f'Fiora_strc/reports/{self.suitename}.md', 'w') as outfile:
            outfile.write(markdown_document)
            