import fiora.test_modules
import inspect
import nibabel as nib
import json
from tqdm import tqdm
import fiora.vars_and_path as vp


class FioraSuiteGenerator:
    """Suite generator for creating the test suite file"""
    def __init__(self, files, suitename):
        self.suitename = suitename
        self.files = files
        self.all_tests = []
        class_tests = inspect.getmembers(fiora.test_modules, inspect.isclass)
        for test in class_tests:
            self.all_tests.append(test[1]())
    
    def catch_metrics(self):
        """Catch the metrics from the test modules"""
        for file in tqdm(self.files):
            img = nib.load(file)
            data = img.get_fdata()
            for class_test in self.all_tests:
                class_test.run(data)
    
    def create_suite(self):
        """Create the suite file"""
        suite = {}
        for class_test in self.all_tests:
            suite.update(class_test.make_test())
        # write to file
        with open(f"{vp.module_folder_name}/test_suites/{self.suitename}.json", "w") as f:
            json.dump(suite, f, indent=4)
        

    



