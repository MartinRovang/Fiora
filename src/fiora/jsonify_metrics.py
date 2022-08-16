import numpy as np

class Jsonify_Base:
    """ Class for creating json file for each test """
    def __init__(self, name):
        self.json_suite_test_file = {name: {}}
        self.sequence = []
        self.name = name
    
    def get_distribution(self, data):
        """ Get distribution of data """
        self.json_suite_test_file[self.name]["distribution"] = {
        "0.05": {
            "min": min(data["q_05"]),
            "max": max(data["q_05"]),
        },
        "Q1": {
            "min": min(data["q1"]),
            "max": max(data["q1"]),
        },
        "Median": {
            "min": min(data["median"]),
            "max": max(data["median"]),
        },
        "Q3": {
            "min": min(data["q3"]),
            "max": max(data["q3"]),
        },
        "0.95": {
            "min": min(data["q_95"]),
            "max": max(data["q_95"]),
        },
        }
        return self.json_suite_test_file
    
    def get_mean(self, data):
        """ Get mean of data """
        self.json_suite_test_file[self.name]["mean"] = {
        "min": min(data["mean"]),
        "max": max(data["mean"]),
        }
        return self.json_suite_test_file
    
    def get_max_value(self, data):
        """ Get max value of data """
        self.json_suite_test_file[self.name]["max_value"] = {
        "min": min(data["max_value"]),
        "max": max(data["max_value"]),
        }
        return self.json_suite_test_file
    
    def get_min_value(self, data):
        """ Get min value of data """
        self.json_suite_test_file[self.name]["min_value"] = {
        "min": min(data["min_value"]),
        "max": max(data["min_value"]),
        }
        return self.json_suite_test_file
    
    def get_percentage_foreground(self, data):
        """ Get percentage of foreground pixels """
        self.json_suite_test_file[self.name]["percentage_foreground"] = {
        "min": min(data["percentage_foreground"]),
        "max": max(data["percentage_foreground"]),
        }
        return self.json_suite_test_file
    
    def get_types(self, data):
        """ Get types of data """
        self.json_suite_test_file[self.name]["types"] = {
        "unique_types": [str(x) for x in np.unique(data["types"])]
        }
    
    def get_num_nans(self, data):
        """ Get number of nans """
        self.json_suite_test_file[self.name]["num_nans"] = {
        "total": int(sum(data["num_nans"]))
        }
        return self.json_suite_test_file
    
    def get_num_infs(self, data):
        """ Get number of infs """
        self.json_suite_test_file[self.name]["num_infs"] = {
        "total": int(sum(data["num_infs"]))
        }
        return self.json_suite_test_file
    
    def get_shapes(self, data):
        """ Get shapes of data """
        self.json_suite_test_file[self.name]["shapes_ax1"] = {
        "unique_shapes": [int(x) for x in np.unique(data["shapes_ax1"])]
        }
        self.json_suite_test_file[self.name]["shapes_ax2"] = {
        "unique_shapes": [int(x) for x in np.unique(data["shapes_ax2"])]
        }
        self.json_suite_test_file[self.name]["shapes_ax3"] = {
        "unique_shapes": [int(x) for x in np.unique(data["shapes_ax3"])]
        }
        return self.json_suite_test_file
    
    def get_orientation_correlation(self, data):
        for i , brain in enumerate(data["downsampled_brains"]):
            if i == 0:
                total_brain = brain
            else:
                total_brain += brain
        total_brain /= len(data["downsampled_brains"])
        self.json_suite_test_file[self.name]["orientation_correlation"] = total_brain.astype(int).tolist()

        return self.json_suite_test_file
    
    def create_orientation_correlation(self):
        """ Add the json creation of creat_distribution to the sequence """
        if self.get_orientation_correlation not in self.sequence:
            self.sequence.append(self.get_orientation_correlation)

    def create_distribution(self):
        """ Add the json creation of creat_distribution to the sequence """
        if self.get_distribution not in self.sequence:
            self.sequence.append(self.get_distribution)
    
    def create_mean(self):
        """ Add the json creation of creat_mean to the sequence """
        if self.get_mean not in self.sequence:
            self.sequence.append(self.get_mean)
    
    def create_max_value(self):
        """ Add the json creation of creat_max_value to the sequence """
        if self.get_max_value not in self.sequence:
            self.sequence.append(self.get_max_value)
    
    def create_min_value(self):
        """ Add the json creation of creat_min_value to the sequence """
        if self.get_min_value not in self.sequence:
            self.sequence.append(self.get_min_value)
    
    def create_percentage_foreground(self):
        """ Add the json creation of creat_percentage_foreground to the sequence """
        if self.get_percentage_foreground not in self.sequence:
            self.sequence.append(self.get_percentage_foreground)
    
    def create_types(self):
        """ Add the json creation of creat_types to the sequence """
        if self.get_types not in self.sequence:
            self.sequence.append(self.get_types)
    
    def create_num_nans(self):
        """ Add the json creation of creat_num_nans to the sequence """
        if self.get_num_nans not in self.sequence:
            self.sequence.append(self.get_num_nans)
    
    def create_num_infs(self):
        """ Add the json creation of creat_num_infs to the sequence """
        if self.get_num_infs not in self.sequence:
            self.sequence.append(self.get_num_infs)

    def create_shapes(self):
        """ Add the json creation of creat_shapes to the sequence """
        if self.get_shapes not in self.sequence:
            self.sequence.append(self.get_shapes)


    def run_sequence(self, data):
        """ Run the sequence of functions """
        for func in self.sequence:
            func(data)
        return self.json_suite_test_file