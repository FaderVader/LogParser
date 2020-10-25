# top-level - dict
clients = {"AX82017": {}, "AX82018": {}, "TX45046": {} }  # dict enforces uniqueness

# mid-level - dict
files = {'file1': [], 'file2': [], 'file3': []}

# bottom-level (data) - list of tuples
lines = [(10, '10-lines'), (20, '20-lines'), (30, '30-lines')]   # (timestamp, payload)

# assignment
clients['AX82018'] = files
clients['AX82018']['file2'] = lines

# retrieval
selected_line = clients['AX82018']['file2'][0] # get first line
print(selected_line)