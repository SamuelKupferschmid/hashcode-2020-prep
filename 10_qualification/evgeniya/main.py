import os
import models
from utils import *
from operator import attrgetter

INPUT_DIR = '../input/'
OUTPUT_DIR = '../output/'


def solve(filename):
    data = read_file(INPUT_DIR + filename)
    # videos = data['videos']
    # endpoints = data['endpoints']
    # n_of_caches = data['n_of_caches']
    # cache_size = data['cache_size']
    # total_videos_size = data['total_videos_size']
    print("Finished reading the file")


    # with open(OUTPUT_DIR + filename[0:-3] + '_' + str(score) + '_evgeniya.out', 'a') as file:
    #     file.write(str(len(caches_used)) + '\n')
    #     for c in caches_used:
    #         file.write(str(c.id) + ' ' + ' '.join([str(v) for v in c.videos.keys()]) + '\n')

# solve('busy_day.in')
# solve('redundancy.in')
# solve('mother_of_all_warehouses.in')


# for filename in os.listdir(INPUT_DIR):
#     if not filename.startswith('.'):
#         solve(filename)
