class Sim:
    rows = 0
    cols = 0
    n_drones = 0
    T = 0
    drone_max_load = 0

    def __init__(self, rows, cols, n_drones, T, drone_max_load):
        self.rows = rows
        self.cols = cols
        self.n_drones = n_drones
        self.T = T
        self.drone_max_load = drone_max_load


class Product:
    id
    size = 0

    def __init__(self, id, size):
        self.id = id
        self.size = size


class Warehouse:
    id
    location = []
    products = []

    def __init__(self, id, location, products):
        self.id = id
        self.location = location
        self.products = products


class Order:
    id
    location = []
    n_items = 0
    items = []

    def __init__(self, id, location, n_items, items):
        self.id = id
        self.location = location
        self.n_items = n_items
        self.items = items


class Drone:
    id
