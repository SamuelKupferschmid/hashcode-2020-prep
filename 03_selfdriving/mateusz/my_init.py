import my_util

# 0 0 1 3 2 9 
# 1 2 1 0 0 9 
# 2 0 2 2 0 9
START_ROW = 0
START_COL = 1
FINISH_ROW = 2
FINISH_COL = 3
START_TIME = 4
FINISH_TIME = 5

D_INDEX = 0
D_START_ROW = 1
D_START_COL = 2
D_FINISH_ROW = 3
D_FINISH_COL = 4
D_START_TIME = 5
D_FINISH_TIME = 6
D_START_NODE = 7
D_FINISH_NODE = 8
D_DISTANCE = 9

# create a dict of nodes and a matrix of distances between each of them
# distances are too much, we don't have so much memory, if we want to figure it out what is actual distribution 
# we need to create a separate algorithm - maybe I won't be be doing that atm
# def create_nodes_with_distances(n_rows, n_cols):
#     nodes_arr = [[0] * n_cols for i in range(n_rows)]
#     size = n_rows * n_cols
#     distances = [[0] * size for i in range(size)]

#     nodes_dict = {}
#     id = 0
#     for y in range(n_rows):
#         print("row")
#         for x in range(n_cols):
#             nodes_arr[y][x] = id
#             nodes_dict[id] = [y, x]
#             id += 1

#     # x1, x2, y1, y2 are mathematical co-ordinates
#     for k1 in sorted(nodes_dict.keys()):
#         print("node")
#         for k2 in sorted(nodes_dict.keys()):
#             x1 = nodes_dict[k1][1]
#             y1 = nodes_dict[k1][0]
#             y2 = nodes_dict[k2][1]
#             x2 = nodes_dict[k2][0]

#             d = abs(x2 - x1) + abs(y2 - y1)
#             distances[k1][k2] = d

#     return nodes_arr, nodes_dict, distances

# create a dict of nodes
def create_nodes(n_rows, n_cols):
    nodes_arr = [[0] * n_cols for i in range(n_rows)]

    nodes_dict = {}
    id = 0
    for y in range(n_rows):
        for x in range(n_cols):
            nodes_arr[y][x] = id
            nodes_dict[id] = [y, x]
            id += 1

    return nodes_arr, nodes_dict




# return a dict of rides with nodes instead of x, y co-ordinates
def process_rides(rides_raw, nodes_arr):
    rides_dict = {}
    id = 0

    # we replace x, y co-ordinates with nodes id
    for ride in rides_raw:
        x1 = ride[START_COL]
        x2 = ride[FINISH_COL]
        y1 = ride[START_ROW]
        y2 = ride[FINISH_ROW]

        n1 = nodes_arr[y1][x1]
        n2 = nodes_arr[y2][x2]
        d = my_util.distance(y1, x1, y2, x2)

        rides_dict[id] = [id] + ride + [n1, n2, d]
        id += 1

    return rides_dict