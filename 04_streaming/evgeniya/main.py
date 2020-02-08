import os
import models
from utils import *
from operator import attrgetter

INPUT_DIR = '../input/'
OUTPUT_DIR = '../output/'


def solve(filename):
    data = read_file(INPUT_DIR + filename)
    videos = data['videos']
    endpoints = data['endpoints']
    n_of_caches = data['n_of_caches']
    cache_size = data['cache_size']
    total_videos_size = data['total_videos_size']
    print("Finished reading the file")

    caches = []
    for i in range(n_of_caches):
        c = Cache(i, cache_size)
        caches.append(c)

    # videos_sorted = sorted(videos.values(), key=lambda x: x.requested, reverse=True)
    #
    # while len(videos_sorted):
    #     v = videos_sorted.pop(0)
    #     print("Left to process ", len(videos_sorted))
    #     for c in caches:
    #         if v.size <= c.capacity_left:
    #             c.videos[v.id] = True
    #             c.capacity_left -= v.size
    #             break


    print("Calculating score")
    total_profit_in_ms = 0
    total_requests_num = 0
    for e in endpoints.values():
        # sort caches by latency and get ids as a list
        caches_sorted = sorted(e.caches, key=e.caches.get)
        # sort videos by number of requests and get ids as a list
        videos_sorted = sorted(e.requests, key=e.requests.get, reverse=True)
        for vid in videos_sorted:
            lat = e.lat_to_DC
            video = videos[vid]
            for cid in caches_sorted:
                cache = caches[cid]
                if vid in cache.videos:
                    lat = e.caches[cid]
                    break
                if video.size <= cache.capacity_left:
                    cache.videos[vid] = True
                    cache.capacity_left -= video.size
                    lat = e.caches[cid]
                    break
            requests_num = e.requests[vid]
            latency = lat
            profit = e.lat_to_DC - latency
            total_profit_in_ms += profit * requests_num
            total_requests_num += requests_num
        # for vid, requests_num in e.requests.items():
        #     latency = getMinLatency(e, vid, caches)
        #     profit = e.lat_to_DC - latency
        #     total_profit_in_ms += profit * requests_num
        #     total_requests_num += requests_num

    score = 1000 * total_profit_in_ms/total_requests_num

    caches_used = [cache for cache in caches if len(cache.videos.keys()) > 0]
    with open(OUTPUT_DIR + filename[0:-3] + '_' + str(score) + '_evgeniya.out', 'a') as file:
        file.write(str(len(caches_used)) + '\n')
        for c in caches_used:
            file.write(str(c.id) + ' ' + ' '.join([str(v) for v in c.videos.keys()]) + '\n')

# solve('example.in')
# solve('me_at_the_zoo.in')
# solve('trending_today.in')
# solve('videos_worth_spreading.in')
solve('kittens.in.txt')


# for filename in os.listdir(INPUT_DIR):
#     if not filename.startswith('.'):
#         solve(filename)
