"""Parser for Parsing & Processing the Downloaded Data & Obtaining Package Stats"""

import logging
import os
import sys
from collections import defaultdict
from typing import Union

logger = logging.getLogger(__name__)


class Parser:
    def __init__(
        self,
        architecture: str,
        verbose: bool,
        file_name: str = "data",
        get_contents: bool = False,
    ):
        self.data_dir = os.path.join(os.getcwd(), "files")
        self.architecture = architecture
        self.verbosity = verbose
        self.txt_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".txt")
        )
        self.file_data = None
        self.package_file_dict_len = defaultdict(int)
        self.package_file_dict = defaultdict(list)
        self.package_file_dict_sorted = None
        self.package_file_dict_len_sorted = None
        self.get_contents = get_contents

    def read_txt(self) -> bytes:
        """
        Read data from saved text file
        Returns:
            bytes_object: downloaded data in bytes
        """
        try:
            with open(self.txt_filename, "rb") as f:
                self.file_data = f.read()
        except FileNotFoundError:
            logger.error("No txt file found to read from")
            sys.exit()
        else:
            return self.file_data

    def parse_txt(self) -> None:
        """
        Parse raw data to get packages & corresponding files in list form
        Returns:
            dict: dictionary of packages & their corresponding files using helper function
        """
        data_str = Parser.convert_to_str(self.read_txt())
        data_list = data_str.strip().split("\n")
        self._process_contents(data=data_list)

    def package_stats(
        self,
        top_n: int = 10,
        output: bool = True,
        write_to_file: bool = False,
        filename: str = "package_stats",
    ) -> list:
        """
        Main Task - Output the top-n packages & their files in descending order (Package Stats)
        Args:
            top_n: no of top packages required (based on the number of files contained in them),
            default=10 & sort in descending order
            output: if the list of top_n is printed to stdout/console
            write_to_file: if results are to be written to a txt file
            filename: if yes above, the filename else default base name of "package_stats" is used
        Returns:
            list: reverse-sorted (desc) top-n packages & their files
        """
        if not self.package_file_dict_len:
            self.parse_txt()
            self.package_file_dict_len_sorted = Parser.sort_dict_len(
                self.package_file_dict_len, desc=True
            )
        self.package_file_dict_len_sorted = Parser.sort_dict_len(
            self.package_file_dict_len, desc=True
        )
        if self.verbosity:
            logging.info(f"Getting Stats for top-{top_n} Packages...")
        if output:
            file_path = os.path.join(
                self.data_dir, (filename + f"_{self.architecture}" + ".txt")
            )
            try:
                with open(file_path, "w") as f:
                    header_string = "FOR ARCHITECTURE '{}':\n{:^40} {:^40}".format(
                        self.architecture, "PACKAGE NAME", "NUMBER OF FILES"
                    )
                    print(header_string)
                    f.write(header_string + "\n")
                    for ind, val in enumerate(
                        self.package_file_dict_len_sorted[:top_n]
                    ):
                        package_files_row = "{:>5}. {:-<50} {}".format(
                            (ind + 1), val[0], val[1]
                        )
                        print(package_files_row)
                        if write_to_file:
                            f.write(package_files_row + "\n")
            except IOError as e:
                logger.error(f"Error while writing results txt file: {e}")
                sys.exit()
            else:
                return self.package_file_dict_len_sorted

    def __str__(self):
        """
        Give info about the downloaded data based on Package Stats
        Returns:
            str: output information about the total packages & total files to stdout/console
        """
        if self.package_file_dict is None:
            self.parse_txt()
        return f"""Content Indices Info:
        Total Packages: {len(self.package_file_dict_len)}
        Total Files: {sum([i for i in self.package_file_dict_len.values()])}
        Empty Packages: {sum([i for i in self.package_file_dict_len.values() if i == 0])}
        Ungrouped Data: {self.package_file_dict_len["ungrouped_data"]}
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
    def sort_dict_len(dictionary: dict, desc: bool = False) -> list:
        """
        Sort dictionary in descending order based on length of values (list)
        Args:
            dictionary: dictionary with values sorted in ascending order (default) based on length
            desc: if sorting needs to be done in descending order
        Returns:
            list: contains the sorted dictionary elements as tuples
        """
        return sorted(dictionary.items(), key=lambda x: x[1], reverse=desc)

    def _process_contents(self, data: list) -> None:
        """
        Helper function: Process raw text content for the given architecture
        Args:
            data: packages & files data in list form, read from saved txt file
        Returns:
            dict: dictionary containing packages as keys & their files as values (list)
        """
        if self.verbosity:
            logging.info("Processing raw data...")
        for ind, val in enumerate(data):
            file_and_package = val.split()
            if len(file_and_package) == 2:
                file_s, package = Parser._split_by_comma(
                    val.split()[0]
                ), Parser._split_by_comma(val.split()[1])
                if file_s[0] == "EMPTY_PACKAGE":
                    logger.warning(f"No file for '{package[0]}' package")
                    self.package_file_dict_len[package[0]] = 0
                    if self.get_contents:
                        self.package_file_dict[package[0]] = []
                else:
                    for pack in package:
                        self.package_file_dict_len[pack] += len(file_s)
                        if self.get_contents:
                            self.package_file_dict[pack].extend(file_s)

            elif len(file_and_package) == 1:
                logging.warning(
                    f"File or Package missing in file @ {ind + 1} line, skipped"
                )
                self.package_file_dict_len["ungrouped_data"] += 1
                if self.get_contents:
                    self.package_file_dict["ungrouped_data"].extend(file_and_package[0])

            elif not file_and_package:
                continue

    @staticmethod
    def _split_by_comma(element: str) -> Union[list, str]:
        if element:
            return element.split(",")
        return ""
