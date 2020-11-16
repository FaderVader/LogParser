"""
This module finds all files in specified folder
Extension is stripped from File-name
"""

from os import listdir
from os.path import join, isfile, isdir

def _stripFileNames(file_list):
    stripped_file_names =[]
    for file in file_list:
        stripped_file_names.append(file[:-4])
    return stripped_file_names


def GetListOfFiles(base_path):
    files = listdir(base_path)
    stripped = _stripFileNames(files)
    return stripped