from unittest import suite
import nibabel as nib
import os
import numpy as np
import json
from rich.progress import track
import src.fiora.generate_report as gr

from sqlalchemy import all_
class FioraProfiler:
    def __init__(self, fiora_path, filetype, suitename):
        self.fiora_path = fiora_path
        self.filetype = filetype
        self.files = [x for x in os.listdir(self.fiora_path) if x.endswith(filetype)]
        self.suitename = suitename
        self.json_suite_test_file = {suitename: {}}
        self.report_gen = gr.ReportMaker(suitename)
        # save json file
        with open(f'Fiora_strc/test_suites/{suitename}.json', 'w') as outfile:
            json.dump(self.json_suite_test_file, outfile)
    
    def get_files_nifty(self, path_to_file):
        nibfile = nib.load(path_to_file)
        data = nibfile.get_fdata()
        affine = nibfile.affine
        return data, affine
    
    def get_files_dcm(self, path_to_file):
        pass

    def save_json(self, json_file):
        with open(f'Fiora_strc/test_suites/{self.suitename}.json', 'w') as outfile:
            json.dump(json_file, outfile)
    
    def load_json(self):
        with open(f'Fiora_strc/test_suites/{self.suitename}.json', 'r') as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file

    def get_general_profile(self):
        all_files_metrics = {'q_05': [], 'q1': [], 'median': [], 'q3': [], 'q_95': [], 'mean': [], 'max_value': [], 'min_value': [], 'percentage_foreground':[], 'num_nans': [], 'num_infs': [], 'types':[]}
        json_suite_test_file = self.load_json()
        
        for file in track(self.files, description='Profiling files', total=len(self.files)):
            data, affine = self.get_files_nifty(os.path.join(self.fiora_path, file))
            all_files_metrics['types'].append(str(data.dtype))
            foreground_values = (data > 0).astype('int').sum()
            background_values = (data <= 0).astype('int').sum()
            percentage_foreground = foreground_values / (foreground_values + background_values)
            nan_values = np.isnan(data).sum()
            inf_values = (data == np.inf).astype('int').sum()

            data = data[data != 0]
            q_05 = round(np.quantile(data, 0.05),3)
            q1 = round(np.quantile(data, 0.25),3)
            median = round(np.median(data),3)
            q3 = round(np.quantile(data, 0.75),3)
            q_95 = round(np.quantile(data, 0.95),3)
            mean = round(np.mean(data),3)
            # append to list
            all_files_metrics['q_05'].append(q_05)
            all_files_metrics['q1'].append(q1)
            all_files_metrics['median'].append(median)
            all_files_metrics['q3'].append(q3)
            all_files_metrics['q_95'].append(q_95)
            all_files_metrics['mean'].append(mean)
            all_files_metrics['max_value'].append(round(np.max(data),3))
            all_files_metrics['min_value'].append(round(np.min(data),3))
            all_files_metrics['percentage_foreground'].append(round(percentage_foreground,3))
            all_files_metrics['num_nans'].append(nan_values)
            all_files_metrics['num_infs'].append(inf_values)

        # add min and max for each category
        json_suite_test_file[self.suitename]["distribution"] = {"q_05": {'min': min(all_files_metrics["q_05"]), 'max': max(all_files_metrics["q_05"])}, "q1": {'min': min(all_files_metrics["q1"]), 'max': max(all_files_metrics["q1"])}, "median": {'min': min(all_files_metrics["median"]), 'max': max(all_files_metrics["median"])}, "q3": {'min': min(all_files_metrics["q3"]), 'max': max(all_files_metrics["q3"])}, "q_95": {'min': min(all_files_metrics["q_95"]), 'max': max(all_files_metrics["q_95"])}}
        json_suite_test_file[self.suitename]["mean"] = {'min': min(all_files_metrics["mean"]), 'max': max(all_files_metrics["mean"])}
        json_suite_test_file[self.suitename]["max_values"] = {'min': min(all_files_metrics["max_value"]), 'max': max(all_files_metrics["max_value"])}
        json_suite_test_file[self.suitename]["min_values"] = {'min': min(all_files_metrics["min_value"]), 'max': max(all_files_metrics["min_value"])}
        json_suite_test_file[self.suitename]["percentage_foreground"] = {'min': min(all_files_metrics["percentage_foreground"]), 'max': max(all_files_metrics["percentage_foreground"])}
        json_suite_test_file[self.suitename]["num_nans"] = {'total': int(sum(all_files_metrics["num_nans"]))}
        json_suite_test_file[self.suitename]["num_infs"] = {'total': int(sum(all_files_metrics["num_infs"]))}
        json_suite_test_file[self.suitename]["types"] = {'unique_types': list(np.unique(all_files_metrics['types']))}

        self.save_json(json_suite_test_file)
    
    def make_report(self):
        self.report_gen.generate_report_markdown()

    

    
    


    









        

    
    


