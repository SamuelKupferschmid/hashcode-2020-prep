class Problem:
    def __init__(self, videos_no, endpoints_no, request_descriptions_no, cache_servers_no, cache_server_capacity):
        self.videos_no = videos_no
        self.endpoints_no = endpoints_no
        self.request_descriptions_no = request_descriptions_no
        self.cache_servers_no = cache_servers_no
        self.cache_server_capacity = cache_server_capacity
        self.video_sizes = {}
        self.endpoints = {}
        self.requests = []
        self.cache_servers = {}

    def init_cache_servers(self):
        for i in range(self.cache_servers_no):
            cs = CacheServer(i, self.cache_server_capacity)
            self.cache_servers[i] = cs

    def add_video_sizes(self, sizes):
        id = 0
        while id < len(sizes):
            self.video_sizes[id] = sizes[id]
            id += 1

    def add_endpoint(self, endpoint):
        self.endpoints[endpoint.id] = endpoint

    def add_request(self, request):
        self.requests.append(request)

class Endpoint:
    def __init__(self, id, latency, connnected_cache_servers_no):
        self.id = id
        self.latency = latency
        self.connnected_cache_servers_no = connnected_cache_servers_no
        self.cache_servers = {}
    
    def add_cache_server(self, cache_server_id, cache_server_latency):
        self.cache_servers[cache_server_id] = cache_server_latency

class Request:
    def __init__(self, video_id, endpoint_id, requests_no):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.requests_no = requests_no

class CacheServer:
    def __init__(self, server_id, capacity):
        self.server_id = server_id
        self.capacity = capacity
        self.videos = set()
        self.size = 0

    def add_video(self, video_id, video_size):
        self.videos.add(video_id)
        self.size += video_size

    def remove_video(sefl, video_id, video_size):
        self.videos.remove(video_id)
        self.size -= video_size
