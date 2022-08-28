"""Parser Class for Parsing through the Downloaded Data and Obtaining Package Statistics"""

import logging
import os
import sys
from collections import defaultdict

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, architecture: str, verbose: bool, file_name: str = "data"):
        self.data_dir = os.path.join(os.getcwd(), "files")
        self.architecture = architecture
        self.verbosity = verbose
        self.txt_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".txt")
        )
        self.file_data = None
        self.package_file_dict = None
        self.package_file_dict_sorted = None

    def read_txt(self) -> bytes:
        """
        Read data from already generated text file
        Returns:
            bytes_object: downloaded data in bytes
        """
        try:
            with open(self.txt_filename, "rb") as f:
                self.file_data = f.read()
        except FileNotFoundError as e:
            logger.error("txt file not found for reading")
            sys.exit(e)
        else:
            return self.file_data

    def parse_txt(self) -> dict:
        """
        Parse data (text) to get packages and corresponding files
        Returns:
            dict: dictionary of packages and their corresponding files
        """
        data_str = Parser.convert_to_str(self.read_txt())
        data_list = data_str.strip().split("\n")
        self.package_file_dict = defaultdict(list)
        for ind, val in enumerate(data_list):
            file, package = val.split()[0], val.split()[1]
            self.package_file_dict[package].append(file)
        return self.package_file_dict

    def package_stats(
        self,
        top_n: int = 10,
        output: bool = True,
        write_to_file: bool = False,
        filename: str = "package_stats",
    ) -> list:
        """
        Main Task - Output the top-n packages and their files in descending order (Package Stats)
        Args:
            top_n: no of top packages required (based on the number of files contained in them),
            default=10 and sort in descending order
            output: if the list of top_n is printed to stdout/console
            write_to_file: if results are to be written to a txt file
            filename: if yes above, the filename else default base name of "package_stats" is used
        Returns:
            list: reverse-sorted (desc) top-n packages and their files
        """
        if self.verbosity:
            logging.info("Getting Package Stats...")
        if self.package_file_dict is None:
            self.package_file_dict_sorted = Parser.sort_dict_len_value(
                self.parse_txt(), desc=True
            )
        self.package_file_dict_sorted = Parser.sort_dict_len_value(
            self.package_file_dict, desc=True
        )
        if output:
            file_path = os.path.join(
                self.data_dir, (filename + f"_{self.architecture}" + ".txt")
            )
            if os.path.exists(file_path):
                os.remove(file_path)
            try:
                with open(file_path, "a") as f:
                    header_string = "FOR ARCHITECTURE {}:\n{:^40} {:^40}".format(
                        self.architecture, "PACKAGE NAME", "NUMBER OF FILES"
                    )
                    print(header_string)
                    f.write(header_string + "\n")
                    for ind, val in enumerate(self.package_file_dict_sorted[:top_n]):
                        package_files_row = "{:>5}. {:-<50} {}".format(
                            (ind + 1), val[0], len(val[1])
                        )
                        print(package_files_row)
                        if write_to_file:
                            f.write(package_files_row + "\n")
            except FileNotFoundError as e:
                sys.exit(e)
            else:
                return self.package_file_dict_sorted

    def __str__(self):
        """
        Give info about the downloaded data based on Package Stats
        Returns:
            str: output information about the total packages and total files to stdout/console
        """
        return f"""Content Indices Info:
        Total Packages: {len(self.package_file_dict)}
        Total Files: {sum([len(i) for i in self.package_file_dict.values()])}
        """

    @staticmethod
    def convert_to_str(text: bytes) -> str:
        """
        Helper function: Convert Bytes to String
        Args:
            text: byte-string to be converted to string
        Returns:
            str: the converted string
        """
        return text.decode("utf-8")

    @staticmethod
    def sort_dict_len_value(dictionary: dict, desc: bool = False) -> list:
        """
        Sort the dictionary in descending order based on length of values (list)
        Args:
            dictionary: dictionary with values sorted in ascending order (default) based on length
            desc: if sorting needs to be done in descending order
        Returns:
            list: contains the sorted dictionary elements as tuples
        """
        return sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=desc)
