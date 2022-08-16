import numpy as np
from fiora.jsonify_metrics import Jsonify_Base
# resize from scikit image
from skimage.transform import resize


class MetricBase:
    def __init__(self, name):
        self.all_files_metrics = {
        "q_05": [],
        "q1": [],
        "median": [],
        "q3": [],
        "q_95": [],
        "mean": [],
        "max_value": [],
        "min_value": [],
        "percentage_foreground": [],
        "num_nans": [],
        "num_infs": [],
        "types": [],
        "shapes_ax1": [],
        "shapes_ax2": [],
        "shapes_ax3": [],
        "downsampled_brains": [],
    }
        self.jsonify_base = Jsonify_Base(name)


    def create_json(self):
        return self.jsonify_base.run_sequence(self.all_files_metrics)

    def get_types(self, data):
        self.all_files_metrics["types"].append(str(data.dtype))
        self.jsonify_base.create_types()
    
    def get_distribution(self, data):
        data = data[data != 0]
        q_05 = round(np.quantile(data, 0.05), 3)
        q1 = round(np.quantile(data, 0.25), 3)
        median = round(np.median(data), 3)
        q3 = round(np.quantile(data, 0.75), 3)
        q_95 = round(np.quantile(data, 0.95), 3)
        self.all_files_metrics["q_05"].append(q_05)
        self.all_files_metrics["q1"].append(q1)
        self.all_files_metrics["median"].append(median)
        self.all_files_metrics["q3"].append(q3)
        self.all_files_metrics["q_95"].append(q_95)
        self.jsonify_base.create_distribution()

    
    def get_mean(self, data):
        mean = round(np.mean(data), 3)
        self.all_files_metrics["mean"].append(mean)
        self.jsonify_base.create_mean()
    
    def get_max_value(self, data):
        max_value = round(np.max(data.copy()), 3)
        self.all_files_metrics["max_value"].append(max_value)
        self.jsonify_base.create_max_value()


    def get_min_value(self, data):
        min_value = round(np.min(data.copy()), 3)
        self.all_files_metrics["min_value"].append(min_value)
        self.jsonify_base.create_min_value()
    
    def get_percentage_foreground(self, data):
        foreground_values = (data > 0).astype("int").sum()
        background_values = (data <= 0).astype("int").sum()
        percentage_foreground = foreground_values / (
            foreground_values + background_values
        )
        percentage_foreground = round(percentage_foreground, 3)
        self.all_files_metrics["percentage_foreground"].append(percentage_foreground)
        self.jsonify_base.create_percentage_foreground()
    
    def get_num_nans(self, data):
        num_nans = np.isnan(data).sum()
        self.all_files_metrics["num_nans"].append(num_nans)
        self.jsonify_base.create_num_nans()
    
    def get_num_infs(self, data):
        num_infs = np.isinf(data).sum()
        self.all_files_metrics["num_infs"].append(num_infs)
        self.jsonify_base.create_num_infs()
    
    def get_shapes(self, data):
        shapes_ax1 = data.shape[0]
        shapes_ax2 = data.shape[1]
        shapes_ax3 = data.shape[2]
        self.all_files_metrics["shapes_ax1"].append(shapes_ax1)
        self.all_files_metrics["shapes_ax2"].append(shapes_ax2)
        self.all_files_metrics["shapes_ax3"].append(shapes_ax3)
        self.jsonify_base.create_shapes()
    

    def get_orientation_correlation(self, data):
        downsampled_brain = np.array(resize(data, (64, 64, 64), mode="constant"))
        if len(self.all_files_metrics["downsampled_brains"]) == 0:
            self.all_files_metrics["downsampled_brains"] = [downsampled_brain]
        else:
            self.all_files_metrics["downsampled_brains"].append(downsampled_brain)
        self.jsonify_base.create_orientation_correlation()


    
    
