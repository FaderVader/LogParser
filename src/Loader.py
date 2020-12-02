from StructureBuilder import StructureBuilder 
from LogLine import LogLine
from os import listdir
from os import path as check_path


class Loader:
    def __init__(self, base_path='../testSources/', app_name='GalaxySiteSelector', file_ext='.log'): 
        self.base_path = self.get_base_path()  # config - if debug: './testSources/'   if run from shell: '../testSources/'
        self.app_name = app_name
        self.file_ext = file_ext

    def get_base_path(self):
        path = '../testSources/'
        if check_path.isdir(path):
            return path
        else:
            return './testSources/'
        # try:
        #     with open(path) as f:
        #         return path
        # except:
        #     path = './testSources/'
        #     return path

    def stripFileNames(self, file_list):
        """
        Strip extension from filename.
        """
        strip_length = -4
        stripped_file_names = []
        for file in file_list:
            stripped_file_names.append(file[:strip_length])
        return stripped_file_names

    def getListOfFiles(self):
        """
        Get all files in search-folder, without extension.
        """
        files = listdir(self.base_path)
        stripped = self.stripFileNames(files)
        return stripped

    def loadOneLogfile(self, path):
        """
        Parse every text-line from one file into an instance of LogLine.
        """
        allLines = []
        with open(path) as file:
            for line in file:
                allLines.append(LogLine(line.replace('\n', '')))  # remove trailing newline
        return allLines

    # wrap StructureBuilder in method, Loader should be sole direct dependancy in Query
    def GetStructure(self):
        """
        Get structure for holding logfiles
        """
        structureBuilder = StructureBuilder()
        files = self.getListOfFiles()
        structure = structureBuilder.CreateFileStructure(files)
        return structure

    def GetStructuredLogs(self): 
        """
        Using pre-build structure-scaffold, load all logs into structure [client][file][linenumber]
        """
        fileStructure = self.GetStructure()
        app_name = self.app_name
        file_ext = self.file_ext

        for client in fileStructure:
            for logfile in fileStructure[client]:
                complete_filename = f'{app_name}-{client}-{logfile}{file_ext}'
                file_contents = self.loadOneLogfile(f'{self.base_path}{complete_filename}')
                fileStructure[client][logfile] = file_contents 
        return fileStructure
