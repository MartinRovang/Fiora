import fiora.test_modules
import inspect
import nibabel as nib
import json
from tqdm import tqdm
import fiora.vars_and_path as vp
import coloredlogs, logging
import glob
coloredlogs.install()
import importlib

class DataTester:
    """Suite generator for creating the test suite file"""
    def __init__(self, suitename, files, _logger):
        self.suitename = suitename
        self.files = files
        self.testing_values = {}
        # load json
        with open(f"{vp.module_folder_name}/test_suites/{suitename}.json", "r") as f:
            self.suite = json.load(f)
        self.all_tests = []
        class_tests = inspect.getmembers(fiora.test_modules, inspect.isclass)
        custom_tests = glob.glob(f"{vp.module_folder_name}/custom_tests/*_fioraT.py")
        orginal_tests_len = len(class_tests)
        custom_tests_len = 0
        if len(custom_tests) > 0:
            # import files
            for file in custom_tests:
                module_name = file.split("/")
                module_name = module_name[-1].split(".")[0]
                module_name = module_name.split("\\")[-1]
                file = f"{vp.module_folder_name}.custom_tests.{module_name}"
                module = importlib.import_module(file)
                custom_tests = inspect.getmembers(module, inspect.isclass)
                custom_tests_len += len(custom_tests)
                class_tests.extend(custom_tests)
        for test in class_tests:
            self.all_tests.append(test[1]())
        _logger.info(f"Loaded {orginal_tests_len} tests from Fiora and {custom_tests_len} custom tests")
    
    def validate(self) -> dict:
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
    