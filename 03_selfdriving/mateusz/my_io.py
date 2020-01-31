# 0 0 1 3 2 9 
# 1 2 1 0 0 9 
# 2 0 2 2 0 9
START_ROW = 0
START_COL = 1
FINISH_ROW = 2
FINISH_COL = 3
START_TIME = 4
FINISH_TIME = 5

problem_folder = './03_selfdriving'

def read_input(file_name):
    f = open(problem_folder + '/input/' + file_name, "r")

    l1 = f.readline().strip()
    header = l1.strip().split(" ")

    entries = []

    for l in f:
        e = l.strip().split(" ")
        entries.append([
            int(e[0]),
            int(e[1]),
            int(e[2]),
            int(e[3]),
            int(e[4]),
            int(e[5])
        ])

    f.close()

    return int(header[0]), int(header[1]), int(header[2]), int(header[3]), int(header[4]), int(header[5]), entries

