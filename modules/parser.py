"""Parser Class for Parsing through the Downloaded Data"""
import logging
import os
import sys
from collections import defaultdict


class Parser:
    def __init__(self, architecture: str, file_name: str):
        self.data_dir = os.path.join(os.getcwd(), "repo_data")
        self.architecture = architecture
        self.txt_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".txt")
        )
        self.file_data = None
        self.package_file_dict = None
        self.package_file_dict_sorted = None

    def read_txt(self) -> bytes:
        """
        Get data from text file
        Returns:
            bytes_object: downloaded data in bytes format
        """
        try:
            with open(self.txt_filename, "rb") as f:
                self.file_data = f.read()
        except FileNotFoundError as e:
            sys.exit(e)
        else:
            return self.file_data

    def parse_txt(self) -> dict:
        """
        Parse data (text) to get packages and corresponding files
        Returns:
            dict_object: dictionary of packages and their corresponding files
        """
        data_str = Parser._convert_to_str(self.read_txt())
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
        filename: str = "results",
    ) -> list:
        """
        Main task - Output the top-n packages and their files in descending order
        Args:
            top_n: no of top packages required (based on the number of files contained in them),
            default=10 and sorting in descending order
            output: prints the list of top_n to stdout/console
            write_to_file: to indicate if results are to be written to a txt file
            filename: if yes above, the filename otherwise default name of "results" is used
        Returns:
            list: the list of reverse sorted top-n packages
        """
        if self.package_file_dict is None:
            self.package_file_dict_sorted = Parser._sort_dict_len_value(
                self.parse_txt(), desc=True
            )
        self.package_file_dict_sorted = Parser._sort_dict_len_value(
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
                    header_string = "FOR ARCHITECTURE {}:\n{:^40} {:^30}".format(
                        self.architecture, "PACKAGE NAME", "NUMBER OF FILES"
                    )
                    # TODO logging
                    print(header_string)
                    logging.info(header_string)
                    f.write(header_string)
                    for ind, val in enumerate(self.package_file_dict_sorted[:top_n]):
                        package_files_row = "{}. {:-<50} {}".format(
                            (ind + 1), val[0], len(val[1])
                        )
                        # TODO logging
                        print(package_files_row)
                        if write_to_file:
                            f.write(package_files_row + "\n")
            except FileNotFoundError as e:
                sys.exit(e)
            else:
                return self.package_file_dict_sorted

    def __str__(self):
        """
        Give info about the Packages and Files in the data
        Returns:
            str: outputs information about the total packages and total files to stdout/console
        """
        return f"""Content Indices Info:
        Total Packages: {len(self.package_file_dict)}
        Total Files: {sum([len(i) for i in self.package_file_dict.values()])}
        """

    @staticmethod
    def _convert_to_str(text: bytes) -> str:
        """
        Helper function: Convert Bytes to String
        Args:
            text: byte-string to be converted to string
        Returns:
            str: the converted string
        """
        return text.decode("utf-8")

    @staticmethod
    def _sort_dict_len_value(dictionary: dict, desc: bool = False) -> list:
        """
        Sort the dictionary in descending order based on length of values
        Args:
            dictionary: dictionary with values as 'list' and sorted in ascending order (default) based on length
            desc: if sorting needs to be in descending order
        Returns:
            list: list containing the dictionary elements as tuples sorted as stated above
        """
        return sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=desc)


if __name__ == "__main__":
    logger = logging.getLogger()
    print(logger)
