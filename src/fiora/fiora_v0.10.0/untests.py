


import numpy as np
class MetricTester:
    def __init__(self):
        self.test_result_json = {}
    
    def test_mean(self, json_ref, json_test):
        """
        Test the mean of the test suite
        """
        mean_ref = json_ref["mean"]
        mean_test = json_test["mean"]
        test_check = mean_ref["max"] >= mean_test["max"] and mean_ref["min"] <= mean_test["min"]
        self.test_result_json["mean"] = test_check
        return test_check
    
    def test_max_values(self, json_ref, json_test):
        """
        Test the max values of the test suite
        """
        max_values_ref = json_ref["max_value"]
        max_values_test = json_test["max_value"]
        test_check = (
            max_values_ref["max"] >= max_values_test["max"]
            and max_values_ref["min"] <= max_values_test["min"]
        )
        self.test_result_json["max_value"] = test_check
        return test_check
    
    def test_min_values(self, json_ref, json_test):
        """
        Test the min values of the test suite
        """
        min_values_ref = json_ref["min_value"]
        min_values_test = json_test["min_value"]
        test_check = (
            min_values_ref["max"] >= min_values_test["max"]
            and min_values_ref["min"] <= min_values_test["min"]
        )
        self.test_result_json["min_value"] = test_check
        return test_check
    
    def test_percentage_foreground(self, json_ref, json_test):
        """
        Test the percentage foreground of the test suite
        """
        percentage_foreground_ref = json_ref["percentage_foreground"]
        percentage_foreground_test = json_test["percentage_foreground"]
        test_check = (
            percentage_foreground_ref["max"] >= percentage_foreground_test["max"]
            and percentage_foreground_ref["min"] <= percentage_foreground_test["min"]
        )
        self.test_result_json["percentage_foreground"] = test_check
        return test_check

    def test_num_nans(self, json_ref, json_test):
        """
        Test the number of nans of the test suite
        """
        num_nans_ref = json_ref["num_nans"]
        num_nans_test = json_test["num_nans"]
        test_check = (
            num_nans_ref["total"] == num_nans_test["total"]
        )
        self.test_result_json["num_nans"] = test_check
        return test_check

    
    def test_num_infs(self, json_ref, json_test):
        """
        Test the number of infs of the test suite
        """
        num_infs_ref = json_ref["num_infs"]
        num_infs_test = json_test["num_infs"]
        test_check = (
            num_infs_ref["total"] == num_infs_test["total"]
        )
        self.test_result_json["num_infs"] = test_check
        return test_check
    
    def test_types(self, json_ref, json_test):
        """
        Test the types of the test suite
        """
        types_ref = json_ref["types"]
        types_test = json_test["types"]
        test_check = set(types_test["unique_types"]).issubset(set(types_ref["unique_types"]))
        self.test_result_json["types"] = test_check
        return test_check
    
    def test_distribution(self, dist_metric_ref, dist_metric_test, quantile_test):
        """
        Test the distribution of the test suite
        """
        test_check = dist_metric_ref["max"] >= dist_metric_test["max"] and dist_metric_ref["min"] <= dist_metric_test["min"]
        if "distribution" not in self.test_result_json:
            self.test_result_json["distribution"] = {}
        self.test_result_json["distribution"][quantile_test] = test_check
        return test_check

    
    def test_shape_ax1(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax1"]
        unique_shape_test = json_test["shapes_ax1"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        test_check = set(B).issubset(set(A))
        self.test_result_json["shapes_ax1"] = test_check
        return test_check
    
    def test_shape_ax2(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax2"]
        unique_shape_test = json_test["shapes_ax2"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        test_check = set(B).issubset(set(A))
        self.test_result_json["shapes_ax2"] = test_check
        return test_check
    
    def test_shape_ax3(self, json_ref, json_test):
        """
        Test the unique shape of the test suite
        """
        unique_shape_ref = json_ref["shapes_ax3"]
        unique_shape_test = json_test["shapes_ax3"]
        # check if values in test exists in reference
        A = list(unique_shape_ref.values())[0]
        B = list(unique_shape_test.values())[0]
        test_check = set(B).issubset(set(A))
        self.test_result_json["shapes_ax3"] = test_check
        return test_check


    def test_orientation_correlation(self, json_ref, json_test):
        """
        Test the orientation correlation of the test suite
        """
        brain_mean_val_ref = np.array(json_ref["orientation_correlation"])
        brain_mean_val_test = np.array(json_test["orientation_correlation"])

        # Get correlation value
        slice_axis = brain_mean_val_ref.shape[0]
        correlation_value = {"sagital": [], "coronal": [], "axial": []}

        for i in range(slice_axis):
            targets = brain_mean_val_ref[i, :, :]
            targets = targets > 0

            target_test1 = brain_mean_val_test[i,:,:][targets]
            target_test2 = brain_mean_val_test[:,i,:][targets]
            target_test3 = brain_mean_val_test[:,:,i][targets]

            if len(target_test1) > 0:
                corr1 = np.corrcoef(brain_mean_val_ref[i,:,:][targets], target_test1)
            else:
                corr1 = np.array([0])
            if len(target_test2) > 0:
                corr2 = np.corrcoef(brain_mean_val_ref[i,:,:][targets], target_test2)
            else:
                corr2 = np.array([0])
            if len(target_test3) > 0:
                corr3 = np.corrcoef(brain_mean_val_ref[i,:,:][targets], target_test3)
            else:
                corr3 = np.array([0])
            # if the inverse of isnan is zero
            check_if_all_are_nan1 = np.isnan(corr1).flatten().sum() != len(corr1.flatten())
            check_if_all_are_nan2 = np.isnan(corr2).flatten().sum() != len(corr2.flatten())
            check_if_all_are_nan3 = np.isnan(corr3).flatten().sum() != len(corr3.flatten())
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

        #test if correlation is higher for the two other axes than axis 0
        test_check = (correlation_axis_0 > correlation_axis_1) and (correlation_axis_0 > correlation_axis_2)

        self.test_result_json["orientation_correlation"] = test_check
        return [correlation_axis_0, correlation_axis_1, correlation_axis_2], test_check