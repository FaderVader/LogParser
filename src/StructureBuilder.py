""" 
    - build list of unique client-names -> create dict, key: clientname
    - build list of unique log-files pr client -> create dict, key: filename
    - for every log-file, build list of lines, then set 2. dict value to list
"""

class StructureBuilder:

    client_name_stripper = lambda name: (name[19:])[:-9]
    file_name_stripper = lambda filename: (filename[-8:])

    @staticmethod
    def _buildClientDict(fileList):
        # iterate over list of file-names:
        #   extract clientname from string
        #   add name to {set}, to ensure unique items
        # when done, convert set to {dict}, key=clientname, value={}

        clients = set()
        for file in fileList:
            clientName = StructureBuilder.client_name_stripper(file)
            clients.add(clientName)

        clients_dict = {clientName : {} for clientName in list(clients)} #dict.fromkeys(list(clients), {})
        return clients_dict

    @staticmethod
    def _buildFileDict(clientDict, filelist):
        # iterate over list of file-names:
        #  extract clientname from string
        #   add file-name of matched client-key to temp-list
        # when done, convert temp-list to {dict}, value=[]

        for client in clientDict:
            client_list = []
            for file in filelist:  # refactor: we should pop item from list. File can only be added once
                if client in file:
                    client_list.append(StructureBuilder.file_name_stripper(file)) 
            clientDict[client] = dict.fromkeys(client_list, [])
        return clientDict

    @staticmethod
    def CreateFileStructure(fileList):
        dict_of_clients = StructureBuilder._buildClientDict(fileList)        
        dict_of_clients_of_files = StructureBuilder._buildFileDict(dict_of_clients, fileList)
        return dict_of_clients_of_files