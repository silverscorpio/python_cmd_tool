class Parser:
    def __init__(self, file_name: str):
        self.txt_filename = file_name + "txt"

    def read_txt(self):
        with open(self.txt_filename, "rb") as f:
            file_data = f.read()
        return file_data
