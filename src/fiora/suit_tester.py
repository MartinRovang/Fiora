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
            img = nib.load(file)
            data = img.get_fdata().flatten()
            for class_test in self.all_tests:
                result = class_test.tester(data, self.suite)
                if result != "N/A":
                    # acculumalte the results
                    results_tests.update({class_test.__class__.__name__: result})
                    
        return results_tests
    