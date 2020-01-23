def read_input(filename):
    # returns:
    # M: max number of slices
    # N: number of pizza types
    # pizzas: number of slices in each type of pizza
    lines = open(filename).readlines()
    M, N = [int(val) for val in lines[0].split()]
    pizzas = [int(val) for val in lines[1].split()]
    return M, N, pizzas

def write_output(filename, pizzas_to_order, types_to_order):
    with open(filename, 'w') as f:
        f.write(f"{pizzas_to_order}\n")
        types = " ".join(str(x) for x in types_to_order)
        f.write(f"{types}")

def backtracking (M, N, pizzas, m):
    res = []

    i = N - 1
    j = M
    while i >= 0:
        if i == 0 and j >= pizzas[i]:
            res.append(pizzas[i])
        if m[i - 1][j - pizzas[i]] + pizzas[i] > m[i - 1][j]:
            if j >= pizzas[i]:
                res.append(pizzas[i])
                j = j - pizzas[i]
        i = i - 1
    return res



def dynamic(filename):
    M, N, pizzas = read_input(filename)
    m = [[0 for j in range(M + 1)] for i in range(N)]

    for i in range(N):
        for j in range(M + 1):
            if pizzas[i] > j:
                m[i][j] = m[i - 1][j]
            else:
                m[i][j] = max(m[i - 1][j], m[i - 1][j - pizzas[i]] + pizzas[i])

    file_out = filename[:-3] + '.out'
    # print(m[-1][-1])
    write_output(file_out,  m[-1][-1], backtracking(M, N, pizzas, m))

dynamic('files/d_quite_big.in')
