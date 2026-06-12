class FolderLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, 'r') as file:
            content = file.read()
        return content

    def get_metadata(self):
        return {
            'file_path': self.path,
            'file_size': len(self.load())
        }
    def split_content(self, chunk_size=1000):
        content = self.load()
        return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]