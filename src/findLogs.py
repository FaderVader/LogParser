from os import listdir
from os.path import join, isfile, isdir

def _stripFileNames(file_list):
    stripped_file_names =[]
    for file in file_list:
        stripped_file_names.append(file[:-4])
    return stripped_file_names


def getListOfFiles():
    base_path = './testSources/'
    files = listdir(base_path)

    stripped = _stripFileNames(files)
    return stripped