#!/usr/bin/python

# Programmer Shelby G

import hashlib, argparse


class InputFile:
    def __init__(self, in_fileName, in_hashType, in_hashSum):
        """
        :type in_fileName: str
        :type in_hashType: str
        :type in_hashSum: str

        """
        self.in_fileName = in_fileName
        self.in_hashType = in_hashType
        self.in_hashSum = in_hashSum

        self.my_hashSum = None


def process_args():

    parser_ob = argparse.ArgumentParser(description="Check integrity of files listed by input file.")

    parser_ob.add_argument("input", help="Path to input file containing files to check")
    parser_ob.add_argument("directory", help="Path to files in designated directory")

    file_contrast = parser_ob.parse_args()
    return file_contrast


def get_prog_file_info(file):
    f_open = open(file)
    f_listed = []
    for line in f_open:
        stripped_line = line.strip()
        list_lines = stripped_line.split()
        f_listed.append(list_lines)

    f_open.close()

    return f_listed


def sort_prog_file_info(input_file):

    file_list = get_prog_file_info(input_file)      # returning a list of tuples w/filename, hash type, sum

    file_objects = []

    for file in file_list:

        file_objects.append(InputFile(file[0], file[1], file[2]))

    return file_objects


def sha1_hashsum(string):
    # generate hash sum for sha1 hash-ed string

    return hashlib.sha1(string).hexdigest()


def md5_hashsum(string):
    # generate hash sum for md5 hash-ed string

    return hashlib.md5(string).hexdigest()


def sha256_hashsum(string):
    # generate hash sum for sha256 hash-ed string

    return hashlib.sha256(string).hexdigest()


def complete_file_data(input_file, directory):
    # open and read file
    # try to find existing file

    option_files = sort_prog_file_info(input_file)

    for option in option_files:
        try:

            fi_open = open(directory + option.in_fileName, "rb")
            fi_data = fi_open.read()
            if option.in_hashType == "sha1":

                option.my_hashSum = sha1_hashsum(fi_data)

            elif option.in_hashType == "md5":

                option.my_hashSum = md5_hashsum(fi_data)

            elif option.in_hashType == "sha256":

                option.my_hashSum = sha256_hashsum(fi_data)

            fi_open.close()

        except FileNotFoundError:

            continue                            # we assume InputFile.my_hashsum stays "none"

    return option_files


def file_integrity_checker(input_file, directory):
    # inputs a file with filenames, hash algorithms sha1/sha256/md5, and hash sums
    # checks for existence of named files on given directory
    # exception case for FILE NOT FOUND
    # generates hash sums of found files
    # compares given hash sums of input data and true files
    # confirms or denies the integrity of files listed
    # outputs filename from input doc and its status: PASS, FAIL, or NOT FOUND

    file_info = complete_file_data(input_file, directory)
    file_status = None

    for file in file_info:
        if file.my_hashSum is None:
            file_status = "NOT FOUND"

        elif file.my_hashSum == file.in_hashSum:
            file_status = "OK"

        else:
            file_status = "FAIL"

        temp = file.in_fileName + " " + file_status

        print(temp)


def main():

    check_files = process_args()
    file_integrity_checker(check_files.input, check_files.directory)

if __name__== "__main__":
    main()

