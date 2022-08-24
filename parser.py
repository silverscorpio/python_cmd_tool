"""Parser Class for Parsing the Downloaded Data"""

from collections import defaultdict


class Parser:
    def __init__(self, file_name: str):
        self.txt_filename = file_name + ".txt"
        self.file_data = None
        self.package_file_dict = None
        self.package_file_dict_sorted = None

    def read_txt(self) -> bytes:
        """Gets the data from text file"""
        with open(self.txt_filename, "rb") as f:
            self.file_data = f.read()
        return self.file_data

    def parse_txt(self) -> dict:
        """Parses the Text to get packages and corresponding files"""
        data_str = Parser.convert_to_str(self.read_txt())
        data_list = data_str.strip().split("\n")
        self.package_file_dict = defaultdict(list)
        for ind, val in enumerate(data_list):
            file, package = val.split()[0], val.split()[1]
            self.package_file_dict[package].append(file)
        return self.package_file_dict

    def package_stats(self, top_n: int = 10, output: bool = True) -> list:
        """Main task - Outputs the top-n (def 10) packages and their files in descending order (def)"""
        if self.package_file_dict is None:
            self.package_file_dict_sorted = Parser.sort_dict_len_value(
                self.parse_txt(), desc=True
            )
        self.package_file_dict_sorted = Parser.sort_dict_len_value(
            self.package_file_dict, desc=True
        )
        if output:
            print("{:^40} {:^30}".format("PACKAGE NAME", "NUMBER OF FILES"))
            for ind, val in enumerate(self.package_file_dict_sorted[:top_n]):
                print("{}. {:-<50} {}".format((ind + 1), val[0], len(val[1])))
        return self.package_file_dict_sorted

    def __str__(self):
        """Gives info about the Packages and Files in the data"""
        return f"""Content Indices Info:
        Total Packages: {len(self.package_file_dict)}
        Total Files: {sum([len(i) for i in self.package_file_dict.values()])}
        """

    @staticmethod
    def convert_to_str(text: bytes) -> str:
        """Converts Bytes to String"""
        return text.decode("utf-8")

    @staticmethod
    def sort_dict_len_value(dictionary: dict, desc: bool = False) -> list:
        """Sorts the dictionary in descending order (def) based on length of values (list)"""
        return sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=desc)
