import numpy as np

class MedianValues:
    def __init__(self):
        self.memory = []
    def run(self, data):
        median_val = np.median(data)
        self.memory.append(median_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.median(data),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"


class MeanValues:
    def __init__(self):
        self.memory = []
    def run(self, data):
        mean_val = np.mean(data)
        self.memory.append(mean_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.mean(data),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"


class MaxValues:
    def __init__(self):
        self.memory = []
    def run(self, data):
        max_val = np.max(data)
        self.memory.append(max_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.max(data),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"


class MinValues:
    def __init__(self):
        self.memory = []
    def run(self, data):
        min_val = np.min(data)
        self.memory.append(min_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.min(data),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class Q05Values:
    def __init__(self):
        self.memory = []
    def run(self, data):
        q05_val = np.quantile(data, 0.05)
        self.memory.append(q05_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.quantile(data, 0.05),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class Q95Values:
    def __init__(self):
        self.memory = []
    def run(self, data):
        q95_val = np.quantile(data, 0.95)
        self.memory.append(q95_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": round(min(self.memory),3), "max": round(max(self.memory),3)}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.quantile(data, 0.95),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class Q1Values:
    def __init__(self):
        self.memory = []
    def run(self, data):
        q1_val = np.quantile(data, 0.25)
        self.memory.append(q1_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.quantile(data, 0.25),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class Q3Values:
    def __init__(self):
        self.memory = []
    def run(self, data):
        q3_val = np.quantile(data, 0.75)
        self.memory.append(q3_val)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.quantile(data, 0.75),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class PercentageForeground:
    def __init__(self):
        self.memory = []
    def run(self, data):
        foreground_values = (data > 0).astype("int").sum()
        background_values = (data <= 0).astype("int").sum()
        percentage_foreground = foreground_values / (
            foreground_values + background_values
        )
        perc_fg = round(percentage_foreground, 3)
        self.memory.append(perc_fg)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round((data > 0).astype("int").sum() / ((data > 0).astype("int").sum() + (data <= 0).astype("int").sum()), 3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class GetNumInfs:
    def __init__(self):
        self.memory = []
    def run(self, data):
        num_infs = np.isinf(data).sum()
        self.memory.append(num_infs)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= np.isinf(data).sum() <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class GetNumNans:
    def __init__(self):
        self.memory = []
    def run(self, data):
        num_nans = np.isnan(data).sum()
        self.memory.append(num_nans)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= float(round(np.isnan(data).sum(),3)) <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

class GetNumNegatives:
    def __init__(self):
        self.memory = []
    def run(self, data):
        num_negatives = (data < 0).astype("int").sum()
        self.memory.append(num_negatives)
    def make_test(self):
        return {self.__class__.__name__: {"min": float(round(min(self.memory),3)), "max": float(round(max(self.memory),3))}}
    def tester(self, data, suite):
        if self.__class__.__name__ in suite:
            if suite[self.__class__.__name__]["min"] <= (data < 0).astype("int").sum() <= suite[self.__class__.__name__]["max"]:
                return True
            else:
                return False
        else:
            return "N/A"

