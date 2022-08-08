


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
