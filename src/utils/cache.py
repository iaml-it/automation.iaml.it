import glob
import json
import os


class Cache:
    def __init__(self):
        self.base_path = '../cache/'

    def clear_cache(self):
        files = glob.glob(self.base_path + '*.json')
        for file in files:
            os.remove(file)

    def exist_cache(self, name):
        if ".json" in name:
            filename = f'{self.base_path}{name}'
        else:
            filename = f'{self.base_path}{name}.json'
        filenames = glob.glob(filename)
        return len(filenames) > 0

    def read_cache(self, name):
        if ".json" in name:
            fname = f'{self.base_path}{name}'
        else:
            fname = f'{self.base_path}{name}.json'
        filenames = glob.glob(fname)
        data = []
        for filename in filenames:
            with open(filename, 'r') as file:
                data.extend(json.load(file))
        return data

    def write_cache(self, name, data):
        if ".json" in name:
            filename = f'{self.base_path}{name}'
        else:
            filename = f'{self.base_path}{name}.json'
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
