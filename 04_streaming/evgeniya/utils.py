from models import *


def read_file(filename):
    file = open(filename, 'r')

    videos = {}
    endpoints = {}

    first_line = file.readline().strip().split(' ')
    n_of_videos = int(first_line[0])
    n_of_endpoints = int(first_line[1])
    n_of_requests = int(first_line[2])
    n_of_caches = int(first_line[3])
    cache_size = int(first_line[4])
    total_videos_size = 0

    videos_line = file.readline().strip().split(' ')
    for i in range(n_of_videos):
        size = int(videos_line[i])
        total_videos_size += size
        videos[i] = Video(i, size)

    for ei in range(n_of_endpoints):
        line = file.readline().strip().split(' ')
        endpoint = Endpoint(ei, int(line[0]))
        num_caches = int(line[1])
        for ci in range(num_caches):
            cache_line = file.readline().strip().split(' ')
            endpoint.caches[int(cache_line[0])] = int(cache_line[1])
        endpoints[ei] = endpoint
    for ri in range(n_of_requests):
        desc_line = file.readline().strip().split(' ')
        v_id = int(desc_line[0])
        e_id = int(desc_line[1])
        num_requests = int(desc_line[2])
        endpoints[e_id].requests[v_id] = num_requests
        videos[v_id].requested += num_requests

    file.close()

    return {
        'videos': videos,
        'endpoints': endpoints,
        'n_of_caches': n_of_caches,
        'cache_size': cache_size,
        'total_videos_size': total_videos_size
    }


def getMinLatency(endpoint, video_id, caches):
    min_lat = endpoint.lat_to_DC
    for c, lat in endpoint.caches.items():
        if video_id in caches[c].videos:
            if lat < min_lat:
                min_lat = lat
    return min_lat




# def write_to_file(filename, line):
#     with open(filename, 'a') as file:
#         file.write(line, '\n')

# def get_score(sol)