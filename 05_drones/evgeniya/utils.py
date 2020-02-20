from models import *


def read_file(filename):
    file = open(filename, 'r')

    orders = {}
    warehouses = {}

    first_line = file.readline().strip().split(' ')
    sim = Sim(int(first_line[0]), int(first_line[1]), int(first_line[2]), int(first_line[3]), int(first_line[4]))

    # read products
    n_products = int(file.readline().strip().split(' ')[0])
    product_types = file.readline().strip().split(' ')
    products = {}
    for i in range(n_products):
        products[i] = product_types[i]

    # read warehouses
    n_wh = int(file.readline().strip().split(' ')[0])
    for i in range(n_wh):
        wh_location = [int(v) for v in file.readline().strip().split(' ')]
        wh_products = [int(v) for v in file.readline().strip().split(' ')]
        warehouses[i] = Warehouse(i, wh_location, wh_products)

    n_orders = int(file.readline().strip().split(' ')[0])
    for i in range(n_orders):
        o_location = [int(v) for v in file.readline().strip().split(' ')]
        o_items = int(file.readline().strip().split(' ')[0])
        o_product_types = [int(v) for v in file.readline().strip().split(' ')]
        orders[i] = Order(i, o_location, o_items, o_product_types)

    file.close()

    return {
        'sim': sim,
        'products': products,
        'warehouses': warehouses,
        'orders': orders
    }

