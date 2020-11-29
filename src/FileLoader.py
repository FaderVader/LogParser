"""
This module loads all log-files from designated folder
"""
from LogLine import LogLine


def loadOneLogfile(path):
    allLines = []
    with open(path) as file:
        for line in file:
            allLines.append(LogLine(line.replace('\n', '')))  # remove trailing newline
    return allLines


# arg fileStructure should be instance of output from StructureBuilder
def LoadLogsFromStructure(fileStructure, base_path): 
    app_name = 'GalaxySiteSelector'
    file_ext = '.log'

    for client in fileStructure:
        for logfile in fileStructure[client]:
            complete_filename = f'{app_name}-{client}-{logfile}{file_ext}'
            file_contents = loadOneLogfile(f'{base_path}{complete_filename}')
            fileStructure[client][logfile] = file_contents 
    return fileStructure
