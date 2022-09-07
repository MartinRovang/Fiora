import fiora.test_modules
import inspect
import nibabel as nib
import json
from tqdm import tqdm
import fiora.vars_and_path as vp


class DataTester:
    """Suite generator for creating the test suite file"""
    def __init__(self, suitename, files):
        self.suitename = suitename
        self.files = files
        self.testing_values = {}
        # load json
        with open(f"{vp.module_folder_name}/test_suites/{suitename}.json", "r") as f:
            self.suite = json.load(f)
        self.all_tests = []
        class_tests = inspect.getmembers(fiora.test_modules, inspect.isclass)
        for test in class_tests:
            self.all_tests.append(test[1]())
    
    def validate(self):
        """test the metrics from the test modules"""
        results_tests = {}
        for file in tqdm(self.files):
            pat_id = file.split("/")[-1].split(".")[0]
            pat_id = pat_id.split("\\")[-1]
            img = nib.load(file)
            data = img.get_fdata()
            for class_test in self.all_tests:
                result = class_test.tester(data = data, suite = self.suite)
                if pat_id not in self.testing_values:
                    self.testing_values[pat_id] = []
                self.testing_values[pat_id].append({class_test.__class__.__name__: class_test.test_val})
                if result != "N/A" and type(result) == bool:
                    results_tests.update({class_test.__class__.__name__: result})
                if type(result) == dict:
                    if len(result) > 0:
                        if class_test.__class__.__name__ in results_tests:
                            results_tests[class_test.__class__.__name__].append(result)
                        else:
                            results_tests.update({class_test.__class__.__name__: [result]})
                    else:
                        pass
        return results_tests
    