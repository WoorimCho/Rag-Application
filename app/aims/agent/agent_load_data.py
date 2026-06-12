import os


class AgentLoadData:
    def __init__(self, file_or_directory=None):
        self.file_or_directory = file_or_directory

    def load(self):
        if not self.file_or_directory:
            raise ValueError("No file or directory specified for loading data.")
        # Implement the actual loading logic here
        print(f"Loading data from: {self.file_or_directory}")

    def __processFile(self, path):


    def __processFolder(self, path, subdir=False):
            if os.path.isfile(filepath):
                yield filepath
            elif os.path.isdir(filepath):
        for filename in os.listdir(path):
            #filepath = os.path.join(path, filename)
            filepath = path + '/' + filename
            if os.path.isfile(filepath):
                yield filepath
            elif os.path.isdir(filepath):
                
            else:



        if not self.file_or_directory:
            raise ValueError("No file or directory specified for getting file list.")
        # Implement logic to return a list of files in the directory
        print(f"Getting file list from: {self.file_or_directory}")
        return []