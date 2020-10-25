# 1 - build list of unique client-names -> create dict, key: clientname
# 2 - build list of unique log-files pr client -> create dict, key: filename
# for every log-file, build list of lines, then set 2. dict value to list

namestripper = lambda name: (name[19:])[:-9]

def BuildClientDict(fileList):
    # iterate over list of file-names:
    #   extract clientname from string
    #   add name to {set}, to ensure unique items
    # when done, convert set to {dict}, key=clientname, value={}

    clients = set()
    for file in fileList:
        clientName = namestripper(file)
        clients.add(clientName)

    clients_dict = {clientName : {} for clientName in list(clients)} #dict.fromkeys(list(clients), {})

    return clients_dict


def BuildFileDict(clientDict, filelist):
    # iterate over list of file-names:
    #  extract clientname from string
    #   add file-name of matched client-key to temp-list
    # when done, convert temp-list to {dict}, value=[]

    for client in clientDict:
        client_list = []
        for file in fileList:
            if client in file:
                client_list.append(file) # we should pop item from list. File can only be added once
        clientDict[client] = dict.fromkeys(client_list, [])
    
    return clientDict


fileList = ['GalaxySiteSelector-AX82017-20200929',
'GalaxySiteSelector-AX82017-20200930',
'GalaxySiteSelector-AX82020-20200928',
'GalaxySiteSelector-AX82020-20200930',
'GalaxySiteSelector-JAKOB-LAPTOP-20201001' ]

dict_of_clients = BuildClientDict(fileList)
dict_of_clients_of_files = BuildFileDict(dict_of_clients, fileList)

# structure demo
for client in dict_of_clients_of_files:
    print(client)
    for files in dict_of_clients_of_files[client]:
        print(' '*3, files)

selected_client = dict_of_clients['AX82017']
for filename in selected_client:
    if '20200929' in filename:
        print(filename)

