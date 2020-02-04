class Video:
    id
    size = 0
    requested = 0

    def __init__(self, id, size):
        self.id = id
        self.size = size


class Endpoint:
    id
    lat_to_DC = 0
    caches = {}
    requests = {}

    def __init__(self, id, lat_to_DC):
        self.id = id
        self.lat_to_DC = lat_to_DC


class Cache:
    id
    capacity_left = 0
    videos = {}

    def __init__(self, id, capacity):
        self.id = id
        self.capacity_left = capacity
        self.videos = {}

