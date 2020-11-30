class StructureBuilder:
    """ 
    - build list of unique client-names -> create dict, key: clientname
    - build list of unique log-files pr client -> create dict, key: filename
    - for every log-file, build list of lines, then set 2. dict value to list
    """

    client_name_stripper = lambda name: (name[19:])[:-9]
    file_name_stripper = lambda filename: (filename[-8:])

    @staticmethod
    def build_clientDict(fileList):
        """
        Iterate over list of file-names:
        - extract clientname from string
        - add name to {set}, to ensure unique items
        When done, convert set to {dict}, key=clientname, value={}
        """

        clients = set()
        for file in fileList:
            clientName = StructureBuilder.client_name_stripper(file)
            clients.add(clientName)

        clients_dict = {clientName: {} for clientName in list(clients)}  # dict.fromkeys(list(clients), {})
        return clients_dict

    @staticmethod
    def build_fileDict(clientDict, filelist):
        """
        Iterate over list of file-names:
        - extract clientname from string
        - add file-name of matched client-key to temp-list
        When done, convert temp-list to {dict}, value=[]
        """

        for client in clientDict:
            client_list = []
            for file in filelist:  # TODO refactor: we should pop item from list. File can only be added once
                if client in file:
                    client_list.append(StructureBuilder.file_name_stripper(file)) 
            clientDict[client] = dict.fromkeys(client_list, [])
        return clientDict

    @staticmethod
    def CreateFileStructure(fileList):
        """
        Based on list of files, return a data-structure for storing log-lines: { client { logfile [ (timestamp, payload) ] } }
        """
        dict_of_clients = StructureBuilder.build_clientDict(fileList)        
        dict_of_clients_of_files = StructureBuilder.build_fileDict(dict_of_clients, fileList)
        return dict_of_clients_of_files
