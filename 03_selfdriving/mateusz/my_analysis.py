import matplotlib.pyplot as plt


# display distribution of distances between each node
# distances -> 2 dimensional table
def analyse_node_distances(distances):
    distance_distribution = []

    for i in range(len(distances)):
        for j in range(len(distances[0])):
            v = distances[i][j]
            d = len(distance_distribution)
            if v + 1 > d:
                distance_distribution += [0]*(v + 1 - d)
            distance_distribution[v] += 1

    print(distance_distribution)

    # craete a bar plot for our distribution
    labels = list(range(len(distance_distribution)))
    width = 0.5

    plt.bar(labels, distance_distribution, width, color='orange', edgecolor='silver')
    # plt.set_title('Distances between Nodes')
    # plt.tight_layout()
    plt.show()


    return 

