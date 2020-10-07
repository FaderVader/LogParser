# top-level - dict
clients = {"AX82017": {}, "AX82018": {}, "TX45046": {} }  # dict enforces uniqueness

# mid-level - dict
file = {'file1': [], 'file2': [], 'file3': []}

# bottom-level (data) - list of tuples
lines = [(10, '10-lines'), (20, '20-lines'), (30, '30-lines')]   # (timestamp, payload)

# assignment
clients['AX82018'] = file
clients['AX82018']['file2'] = lines

print(clients['AX82018']['file2'])