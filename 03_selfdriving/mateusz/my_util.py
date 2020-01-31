def distance(nodes_dict, n1, n2):
    x1 = nodes_dict[n1][1]
    y1 = nodes_dict[n1][0]
    y2 = nodes_dict[n2][1]
    x2 = nodes_dict[n2][0]

    return distance(y1, x1, y2, x2)


def distance(y1, x1, y2, x2):
    d = abs(x2 - x1) + abs(y2 - y1)

    return d