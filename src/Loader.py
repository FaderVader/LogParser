from StructureBuilder import StructureBuilder 
from Types import LogLine
from os import listdir
from os import path as check_path


class Loader:
    """
    Assumed logfile name-format: {app_name}-{yyyy-mm-dd}{.ext}
    """
    def __init__(self, base_path=None, app_name='GalaxySiteSelector', file_ext='.log'): 
        self.base_path = self.get_base_path(base_path)  
        self.app_name = app_name
        self.file_ext = file_ext
        self.structure = None
        self.setup()

    def setup(self):
        files = self.getListOfFiles() 
        self.structure = StructureBuilder.CreateFileStructure(files)

    def get_base_path(self, base_path):
        """
        Verify that folder exists.
        """
        if base_path is not None:  # if base_path was supplied as arg, we check if its valid -
            found = check_path.isdir(base_path)
            if not found:
                raise FileNotFoundError(f"Path {base_path} is not valid")

        # - otherwise, we use one of the defaults
        paths = {'path_a': '../logs/', 'path_b': './logs/'}  # if debug: './logs/'   if run from shell: '../logs/'
        if check_path.isdir(paths['path_a']):
            return paths['path_a']
        else:
            return paths['path_b']

    def stripFileNames(self, file_list):
        """
        Strip extension from filename.
        """
        strip_length = -4  # '.log' is removed
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

    def GetStructure(self):
        """
        Get structure for holding logfiles
        """
        return self.structure

    def GetStructuredLogs(self): 
        """
        Using pre-build structure-scaffolding, we load all logs into structure [client][file]
        """
        file_structure = self.structure
        base_path = self.base_path
        app_name = self.app_name
        file_ext = self.file_ext

        for client in file_structure:
            for logfile in file_structure[client]:
                complete_filename = f'{app_name}-{client}-{logfile}{file_ext}'
                file_contents = self.loadOneLogfile(f'{base_path}{complete_filename}')
                file_structure[client][logfile] = file_contents 
        return file_structure
