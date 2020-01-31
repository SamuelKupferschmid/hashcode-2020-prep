def print_parameters(params):
    for k in params.keys():
        print("%s -> %s" %(k, params[k]))

def print_entries_arr(name, entries):
    for entry in entries:
        print("%s -> %s" %(name, entry))

def print_entries_dict(name, entries):
    for k in sorted(entries.keys()):
        print("%s %d -> %s" %(name, k, entries[k]))
