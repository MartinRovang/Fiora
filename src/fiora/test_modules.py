import numpy as np
from skimage.transform import resize

# import typestting union
from typing import Union

import coloredlogs, logging
import glob

coloredlogs.install()


class MedianValues:
    """Tests or gathers the median values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        median_val = np.median(data)
        self.memory.append(median_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.median(data), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class MeanValues:
    """Tests or gathers the mean values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        mean_val = np.mean(data)
        self.memory.append(mean_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.mean(data), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class MaxValues:
    """Tests or gathers the max values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        max_val = np.max(data)
        self.memory.append(max_val)

    def make_test(self, **kwargs) -> dict:
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        self.test_val = float(round(np.max(data), 3))
        if self.__class__.__name__ in suite:
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class MinValues:
    """Tests or gathers the min values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        min_val = np.min(data)
        self.memory.append(min_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.min(data), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class Q05Values:
    """Tests or gathers the 5th percentile values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        q05_val = np.quantile(data, 0.05)
        self.memory.append(q05_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.quantile(data, 0.05), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class Q95Values:
    """Tests or gathers the 95th percentile values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        q95_val = np.quantile(data, 0.95)
        self.memory.append(q95_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": round(min(self.memory), 3),
                "max": round(max(self.memory), 3),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.quantile(data, 0.95), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class Q1Values:
    """Tests or gathers the 1st quartile values of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        q1_val = np.quantile(data, 0.25)
        self.memory.append(q1_val)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.quantile(data, 0.25), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class Q3Values:
    """Tests or gathers the 3rd quartile values of the data, for both the test and reference data"""

    def __init__(self):
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        q3_val = np.quantile(data, 0.75)
        self.memory.append(q3_val)

    def make_test(self, **kwargs) -> dict:
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = float(round(np.quantile(data, 0.75), 3))
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class PercentageForeground:
    """Tests or gathers the percentage of foreground pixels in the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        foreground_values = (data > 0).astype("int").sum()
        background_values = (data <= 0).astype("int").sum()
        percentage_foreground = foreground_values / (
            foreground_values + background_values
        )
        perc_fg = round(percentage_foreground, 3)
        self.memory.append(perc_fg)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            foreground_values = (data > 0).astype("int").sum()
            background_values = (data <= 0).astype("int").sum()
            percentage_foreground = foreground_values / (
                foreground_values + background_values
            )
            perc_fg = round(percentage_foreground, 3)
            self.test_val = float(perc_fg)
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class NumInfs:
    """Tests or gathers the number of inf values in the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        num_infs = np.isinf(data).sum()
        self.memory.append(num_infs)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {self.__class__.__name__: {"amount": float(np.sum(self.memory))}}

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            num_infs = np.isinf(data).sum()
            self.test_val = float(num_infs)
            if self.test_val == 0:
                return True
            else:
                return False
        else:
            return "N/A"


class NumNans:
    """Tests or gathers the number of nan values in the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        num_nans = np.isnan(data).sum()
        self.memory.append(num_nans)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {self.__class__.__name__: {"amount": float(np.sum(self.memory))}}

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            num_nans = np.isnan(data).sum()
            self.test_val = float(num_nans)
            if self.test_val == 0:
                return True
            else:
                return False
        else:
            return "N/A"


class GetNumNegatives:
    """Tests or gathers the number of negative values in the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        num_negatives = (data < 0).astype("int").sum()
        self.memory.append(num_negatives)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "min": float(round(min(self.memory), 3)),
                "max": float(round(max(self.memory), 3)),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            num_negatives = (data < 0).astype("int").sum()
            self.test_val = float(num_negatives)
            if (
                suite[self.__class__.__name__]["min"]
                <= self.test_val
                <= suite[self.__class__.__name__]["max"]
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class OrientiationCheck:
    """Tests or gathers the orientation of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results
        dps is the number of samples in the reference data"""
        self.memory = []
        self.dps = 0

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        downsampled_brain = np.array(
            resize(data, (124, 124, 124), mode="constant", order=3)
        )

        downsampled_brain = downsampled_brain - np.mean(downsampled_brain)
        downsampled_brain = downsampled_brain /(np.std(downsampled_brain)+ 1e-10)
        if len(self.memory) == 0:
            self.memory = downsampled_brain
        else:
            self.memory += downsampled_brain
        self.dps += 1

    def make_test(self, **kwargs) -> dict:
        """Consolidate the metrics for testing"""
        meanbrain = self.memory / self.dps
        meanbrain = meanbrain.tolist()
        return {self.__class__.__name__: {"meanbrain": meanbrain}}

    def tester(self, **kwargs) -> Union[bool, str]:
        """
        Test the orientation correlation of the test suite
        """
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            brain_mean_ref = np.array(suite[self.__class__.__name__]["meanbrain"])
            correlation_value = {"sagital": [], "coronal": [], "axial": []}
            data = np.array(resize(data, (124, 124, 124), mode="constant", order=3))
            slice_axis = brain_mean_ref.shape[0]
            data = data - np.mean(data)
            data = data / (np.std(data) + 1e-10)
            for i in range(slice_axis):
                targets = brain_mean_ref[i, :, :]
                targets = targets > 0

                target_test1 = data[i, :, :][targets]
                target_test2 = data[:, i, :][targets]
                target_test3 = data[:, :, i][targets]

                if len(target_test1) > 0:
                    corr1 = np.corrcoef(brain_mean_ref[i, :, :][targets], target_test1)
                else:
                    corr1 = np.array([0])
                if len(target_test2) > 0:
                    corr2 = np.corrcoef(brain_mean_ref[i, :, :][targets], target_test2)
                else:
                    corr2 = np.array([0])
                if len(target_test3) > 0:
                    corr3 = np.corrcoef(brain_mean_ref[i, :, :][targets], target_test3)
                else:
                    corr3 = np.array([0])
                # if the inverse of isnan is zero
                check_if_all_are_nan1 = np.isnan(corr1).flatten().sum() != len(
                    corr1.flatten()
                )
                check_if_all_are_nan2 = np.isnan(corr2).flatten().sum() != len(
                    corr2.flatten()
                )
                check_if_all_are_nan3 = np.isnan(corr3).flatten().sum() != len(
                    corr3.flatten()
                )
                if check_if_all_are_nan1:
                    correlation_value["sagital"].append(np.nanmean(corr1))
                else:
                    correlation_value["sagital"].append(0)
                if check_if_all_are_nan2:
                    correlation_value["coronal"].append(np.nanmean(corr2))
                else:
                    correlation_value["coronal"].append(0)
                if check_if_all_are_nan3:
                    correlation_value["axial"].append(np.nanmean(corr3))
                else:
                    correlation_value["axial"].append(0)

            correlation_axis_0 = np.nanmean(correlation_value["sagital"])
            correlation_axis_1 = np.nanmean(correlation_value["coronal"])
            correlation_axis_2 = np.nanmean(correlation_value["axial"])

            self.test_val = {
                "sagital_correlation": float(correlation_axis_0),
                "coronal_correlation": float(correlation_axis_1),
                "axial_correlation": float(correlation_axis_2),
            }
            if (correlation_axis_0 > correlation_axis_1) and (
                correlation_axis_0 > correlation_axis_2
            ):
                return True
            else:
                return False
        else:
            return "N/A"


class DuplicateCheck:
    """Tests or gathers the number of duplicate datapoints, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = {}

    def run(self, **kwargs) -> None:
        """Run through the data and gathers needed data"""
        data = kwargs["data"]
        pat_id = kwargs["pat_id"]

        # slice out center
        data = np.array(data)
        x, y, z = data.shape
        data = data[int(x // 2), :, :]
        data = resize(data, (124, 124), mode="constant", order=3)
        data = data.tolist()
        self.memory[pat_id] = data

    def make_test(self, **kwargs) -> dict:
        """Consolidate the metrics for testing"""

        # test on itself to see if there is any duplicates in the reference data
        self.self_tester()
        return {self.__class__.__name__: {"centre_slices_downsampled": self.memory}}

    def self_tester(self) -> None:
        """Test the reference data for duplicates"""
        self.temp_duplicate_name_list = []
        self.temp_duplicate_list = []
        for key, value in self.memory.items():
            for key2, value2 in self.memory.items():
                if (
                    key != key2
                    and key not in self.temp_duplicate_name_list
                    and key2 not in self.temp_duplicate_name_list
                ):
                    # check same array
                    self.temp_duplicate_name_list.append(key)
                    duplicate_test = np.array_equal(value, value2)
                    if duplicate_test:
                        # print
                        self.temp_duplicate_list.append([key, key2])

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the duplicate correlation of the test suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            data = np.array(data)
            x, y, z = data.shape
            data = data[int(x // 2), :, :]
            data = resize(data, (124, 124), mode="constant", order=3)
            reference_data = suite[self.__class__.__name__]["centre_slices_downsampled"]
            ids_checks = {}
            for key in reference_data.keys():
                # get test for each id
                ref_data = np.array(reference_data[key])
                ids_checks[key] = np.array_equal(data, ref_data)

            self.test_val = {
                key: False for key, value in ids_checks.items() if value == True
            }
            return {key: False for key, value in ids_checks.items() if value == True}
        else:
            return "N/A"


class DataType:
    """Tests or gathers the data type of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        file_type = str(data.dtype)
        self.memory.append(file_type)

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {
            self.__class__.__name__: {
                "data_types": np.unique(self.memory).tolist(),
            }
        }

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = str(data.dtype)
            if self.test_val in suite[self.__class__.__name__]["data_types"]:
                return True
            else:
                return False
        else:
            return "N/A"

class StdValues:
    """Tests or gathers the standard deviation of the data, for both the test and reference data"""

    def __init__(self):
        """Initialize the variables needed for the test, memory is the basic variable for storing the results"""
        self.memory = []

    def run(self, **kwargs) -> None:
        """Run the test and store the results in memory"""
        data = kwargs["data"]
        self.memory.append(np.std(data))

    def make_test(self, **kwargs) -> dict:
        """Make the test for the suite"""
        return {self.__class__.__name__: {"std_values": self.memory}}

    def tester(self, **kwargs) -> Union[bool, str]:
        """Test the data against the suite"""
        data = kwargs["data"]
        suite = kwargs["suite"]
        if self.__class__.__name__ in suite:
            self.test_val = np.std(data)
            if self.test_val in suite[self.__class__.__name__]["std_values"]:
                return True
            else:
                return False
        else:
            return "N/A"