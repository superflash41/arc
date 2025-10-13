import os
import json
# import glob
# import numpy as np
# import tqdm as tqdm

class Dataset(object):
    """
    base class for the arc dataset
    """
    def __init__(self):
        self.d = None # the dictionary mirroring the directory structure
        self.tasks = None # list of tasks (excluding the test output)
        self.outputs = None # list of test outputs
    
    def build_dict_from_dir(self, base_dir):
        """
        build a dictionary mirroring the directory structure
        sample element: d["training"]["00576224"] = {json content}
        """
        d = {}

        subsets = ["training", "evaluation"]
        for s in subsets:
            subset_dir = os.path.join(base_dir, s)
            if not os.path.isdir(subset_dir):
                raise FileNotFoundError(f"there is no directory {subset_dir}!")
        
            d[s] = {} # each subset gets its own dictionary
            for fn in sorted(os.listdir(subset_dir)): # sample: 00576224.json
                if not fn.endswith(".json"): # sanity check
                    continue
                task_id = fn[:-5] # remove the .json
                fpath = os.path.join(subset_dir, fn)
                with open(fpath, "r", encoding="utf-8") as f:
                    d[s][task_id] = json.load(f)

        self.d = d

    def show_dict(self):
        """
        print the dictionary
        """
        if self.d is None:
            print("the dictionary is empty!")
            return
        print(json.dumps(self.d, indent=2, sort_keys=True))

    def split_outputs(self, path):
        """
        extract the test output from all tasks
        """
        self.tasks = {}
        self.outputs = {}
        
        os.makedirs(path, exist_ok=True)
        for subset, tasks in self.d.items():
            outputs = {}
            # get all outputs from v["test"]
            for k, v in tasks.items():
                assert v.pop("name", k) == k # sanity check
                outputs[k] = [t.pop("output") for t in v["test"]]
            with open(os.path.join(path, f"{subset}_tasks.json"), "w", encoding="utf-8") as f:
                json.dump(tasks, f)
            with open(os.path.join(path, f"{subset}_outputs.json"), "w", encoding="utf-8") as f:
                json.dump(outputs, f)
            
            self.tasks[subset] = tasks
            self.outputs[subset] = outputs