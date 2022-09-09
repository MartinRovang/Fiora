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

class FioraSuiteGenerator:
    """Suite generator for creating the test suite file"""
    def __init__(self, files, suitename, _logger):
        self.suitename = suitename
        self.files = files
        self.all_tests = []
        self._logger = _logger
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
        # log the amount of tests used
        _logger.info(f"Found {orginal_tests_len} test(s) and {custom_tests_len} custom test(s) to be used in suite")

        for test in class_tests:
            self.all_tests.append(test[1]())
    
    def catch_metrics(self) -> None:
        """Catch the metrics from the test modules"""
        for file in tqdm(self.files):
            id = file.split("/")[-1].split(".")[0]
            id = id.split("\\")[-1]
            img = nib.load(file)
            data = img.get_fdata()
            for class_test in self.all_tests:
                class_test.run(data = data, pat_id = id)
    
    def create_suite(self) -> None:
        """Create the suite file"""
        suite = {}
        for class_test in self.all_tests:
            suite.update(class_test.make_test())
            try:
                reference_data_duplicates = class_test.temp_duplicate_list
                # log warnings for duplicate names
                for duplicate in reference_data_duplicates:
                    self._logger.warning(f"Duplicate name found in reference data: {duplicate}")
            except:
                pass
        # write to file
        with open(f"{vp.module_folder_name}/test_suites/{self.suitename}.json", "w") as f:
            json.dump(suite, f, indent=4)
        

    



