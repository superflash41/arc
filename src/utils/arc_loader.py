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

    
    def build_dic_from_dir(self, base_dir):
        """
        build a dictionary mirroring the directory structure
        sample of an element: d["training"]["00576224"] = {json content}
        """
        d = {}

        subsets = ["training", "evaluation"]
        for s in subsets:
            subset_dir = os.path.join(base_dir, s)
            # check if the dir exists
            if not os.path.isdir(subset_dir):
                raise FileNotFoundError(f"there is no directory {subset_dir}!")
        
            d[s] = {} # each subset gets its own dictionary
            for fn in os.listdir(subset_dir): # sample: 00576224.json
                if not fn.endswith(".json"): # sanity check
                    continue
                task_id = fn[:-5] # remove the .json
                fpath = os.path.join(subset_dir, fn)
                with open(fpath, "r", encoding="utf-8") as f:
                    d[s][task_id] = json.load(f)

        self.d = d

    def show(self):
        """
        print the dictionary
        """
        if self.d is None:
            print("the dictionary is empty!")
            return
        print(json.dumps(self.d, indent=4))
