# import libs
import math
from datetime import datetime, timedelta

SEPARATOR = ":"

class Solution: 
    def __init__(self, problem=None):
        self.problem = problem

        self.video_to_cache_server = {}
        self.cache_server_clusters = {}
        self.video_distribution = {}

    
    def count_score(self):
        total_requests = 0
        total_save = 0
        final_score = 0

        for request in self.problem.requests:
            video_id = request.video_id
            endpoint_id = request.endpoint_id
            requests_no = request.requests_no

            endpoint = self.problem.endpoints[endpoint_id]

            latency = []
            latency.append(endpoint.latency)

            for k in endpoint.cache_servers.keys():
                cs = self.problem.cache_servers[k]    

                if video_id in cs.videos:
                    latency.append(endpoint.cache_servers[k])
            
            min_latency = min(latency)
            save_per_request = endpoint.latency - min_latency
            save_per_description = requests_no * save_per_request
            
            total_requests += requests_no
            total_save += save_per_description

        final_score = total_save / total_requests
        final_score *= 1000
        
        return int(final_score)

    def string_to_set(self, str_key):
        set_key = set(int(x) for x in str_key.split(SEPARATOR))
        return set_key

    def set_to_string(self, set_key):
        sorted_set = sorted(set_key)
        str_key = SEPARATOR.join(str(x) for x in sorted_set)
        return str_key

    # what happenes if we have zone 5.5?
    def local_to_utc(self, local_time, zone):
        utc_time = local_time - timedelta(hours=zone)
        return utc_time

    def utc_to_local(self, utc_time, zone):
        local_time = utc_time + timedelta(hours=zone)
        return local_time

    def distance_matrix(self, x1, y1, x2, y2):
        result = abs(x1 - x2) + abs(y1 - y2)
        return result

    def distance_euclidan(self, x1, y1, x2, y2):
        x = abs(x1 - x2) ** 2
        y = abs(y1 - y2) ** 2
        result = math.sqrt(x + y)
        return result

    def distance_euclidan_3d(self, x1, y1, z1, x2, y2, z2):
        x = abs(x1 - x2) ** 2
        y = abs(y1 - y2) ** 2
        z = abs(z1 - z2) ** 2
        result = math.sqrt(x + y + z)
        return result

    def convert_to_angle(self, degree, arcminute, arcsecond):
        # maybe later 
        # we need to consider a negative in terms of nort and south

        return angle

    def distance_geo(self, latitude1, longitude1, latitude2, longitude2):
        r = 6371
        # ratio = 180 / math.pi
        # long1 = longitude1 / ratio
        # lat1 = latitude1 / ratio
        # long2 = longitude2 / ratio
        # lat2 = latitude2 / ratio
        lat1 = math.radians(latitude1)
        long1 = math.radians(longitude1)
        lat2 = math.radians(latitude2)
        long2 = math.radians(longitude2)

        a = math.sin(lat1) * math.sin(lat2)
        b = math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)
        d = r * math.acos(a + b)

        # dlon = long2 - long1  
        # dlat = lat2 - lat1 
        # a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        # c = 2 * math.asin(math.sqrt(a))
        # d = c * r

        return d


def main():
    solution = Solution()
    
    print(solution.distance_matrix(1, 2, 3, 4))
    print(solution.distance_matrix(0, 4, 3, 0))
    print(solution.distance_euclidan(0, 4, 3, 0))
    print(solution.distance_geo(53.32055555555556, -1.7297222222222221, 53.31861111111111, -1.6997222222222223))

    # now.strftime("%H:%M:%S")
    print(datetime.now())
    print(solution.utc_to_local(datetime.now(), 4))
    print(solution.utc_to_local(datetime.now(), -2))
    print(solution.utc_to_local(datetime.now(), 0.5))

    print(solution.local_to_utc(datetime.now(), 2))
    print(solution.local_to_utc(datetime.now(), -6))


if __name__ == "__main__":
    main()



    # def map_videos_to_cache(self):
    #     # iterate through all videos
    #     for req in self.problem.requests:
    #         video_id = req.video_id
    #         endpoint_id = req.endpoint_id
    #         requests_no = req.requests_no

    #         endpoint = self.problem.endpoints[endpoint_id]
    #         cache_server_keys = set(endpoint.cache_servers.keys())

    #         # HOTFIX
    #         # if there are no cache servers for this endpoint we can simple skip it
    #         if not len(cache_server_keys) > 0:
    #             continue

    #         if video_id not in self.video_to_cache_server.keys():
    #             # if first one we can initiate here 
    #             # at least one cache server
    #             # and first set is on the first location
    #             k = self.set_to_string(cache_server_keys) 
    #             self.video_to_cache_server[video_id] = {k: 1}
    #         else:
    #             common = False

    #             # we iterate through each key set already present if one of the values repeats with that particular one
    #             # we increase that one by one
    #             # at the end minimum number of cache servers needed should be all with values different than 0
    #             # we start with ordered keys by value from higher to lower
    #             for k in sorted(self.video_to_cache_server[video_id], key=self.video_to_cache_server[video_id].get, reverse=True):
    #                 # first split a key into a set of integers
    #                 # but do we have to convert them to integers really? I think yes as we will be sorting them back 
                    
    #                 # if k == '':
    #                 #     print("Dupa")
                    
    #                 key_set = self.string_to_set(k)

    #                 # if we have a commont part increase that by one key set by one 
    #                 # and set the flag to True if it even makes any difference now
    #                 if len(cache_server_keys & key_set) > 0:
    #                     # we can increase it only for the first match in given iteration
    #                     if not common:
    #                         self.video_to_cache_server[video_id][k] += 1
    #                     cache_server_keys = cache_server_keys - key_set
                        
    #                     common = True

    #             # if there were some reminders from cache_server_keys we add them at the end
    #             # and if previously we didn't find any common part we increase this one by 1 because it's a separate family
    #             if len(cache_server_keys) > 0:
    #                 occur = 0
    #                 if not common:
    #                     occur = 1

    #                 k = self.set_to_string(cache_server_keys)
    #                 self.video_to_cache_server[video_id].update( {k: occur} )


    #     # count how many values are above 0 and store it in video distribution 
    #     for video_id in self.video_to_cache_server.keys():
    #         count = [v for v in self.video_to_cache_server[video_id].values() if v > 0]

    #         # temporary fix to not end with 0 for count which may happen
    #         # if it's empty it must very high number, to make it less appealing
    #         # in next version they won't be taken under consideration at all
    #         minimum_count = len(count)
    #         # HOTFIX
    #         # if minimum_count == 0: 
    #         #     minimum_count = 1000000

    #         self.video_distribution[video_id] = [minimum_count, 0]

    #     # for vk in sorted(self.video_to_cache_server.keys()):
    #     #     print("Video %d Cache Servers %d" %(vk, self.video_distribution[vk][0]))
    #     #     for key_set in sorted(self.video_to_cache_server[vk], key=self.video_to_cache_server[vk].get, reverse=True):
    #     #         print("%s -> %d" %(key_set, self.video_to_cache_server[vk][key_set]))

    # def create_cache_clusters(self):
    #     # iterate through all videos
    #     for req in self.problem.requests:
    #         video_id = req.video_id
    #         endpoint_id = req.endpoint_id
    #         requests_no = req.requests_no

    #         endpoint = self.problem.endpoints[endpoint_id]
    #         cache_server_keys = set(endpoint.cache_servers.keys())

    #         # if there are no cache servers for this endpoint we can simple skip it
    #         if not len(cache_server_keys) > 0:
    #             continue
    
    #         if video_id not in self.cache_server_clusters.keys():
    #             # this is a simple structure than in mapping, here we are only interested in exclusive sets, and how often each set if pinged
    #             # initialize with first one
    #             k = self.set_to_string(cache_server_keys) 
    #             self.cache_server_clusters[video_id] = { k: 1 }
    #         else:
    #             # we iterate through each existing cluster and we create new ones with specific keys and values
    #             new_clusters = {}
    #             for k in sorted(self.cache_server_clusters[video_id], key=self.cache_server_clusters[video_id].get, reverse=True):
    #                 # first let's convert key to keys_set
    #                 # after that we have 3 possibilities: A&B, A-B, B-A
    #                 key_set = self.string_to_set(k)
    #                 current_value = self.cache_server_clusters[video_id][k]

    #                 set1 = cache_server_keys & key_set
    #                 set2 = key_set - cache_server_keys
    #                 set3 = cache_server_keys - key_set
                    
    #                 if len(set1) > 0:
    #                     key1 = self.set_to_string(set1)
    #                     new_clusters[key1] = current_value + 1
                    
    #                 if len(set2) > 0:
    #                     key2 = self.set_to_string(set2)
    #                     new_clusters[key2] = current_value

    #                 cache_server_keys = set3
                
    #             # first occurence of this set if it even exist
    #             if len(cache_server_keys) > 0:
    #                 key3 = self.set_to_string(cache_server_keys)
    #                 new_clusters[key3] = 1

    #             # update reference with new clusters
    #             self.cache_server_clusters[video_id] = new_clusters
        
    #     # for v in sorted(self.cache_server_clusters.keys()):
    #     #     print("Video %d" %(v))
    #     #     for k in sorted(self.cache_server_clusters[v], key=self.cache_server_clusters[v].get, reverse=True):
    #     #         print("%s -> %d" %(k, self.cache_server_clusters[v][k]))

    # def rank_videos(self):
    #     # iterate through each description and count potential saving for each description 
    #     for req in self.problem.requests:
    #         video_id = req.video_id
    #         endpoint_id = req.endpoint_id
    #         requests_no = req.requests_no
    #         video_size = self.problem.video_sizes[video_id]

    #         # find how many different cache servers are minimum to cover
    #         # iterate through each cache server connected to each endpoints
    #         if video_id not in self.videos_rank.keys():
    #             self.videos_rank[video_id] = 0

    #         req_rank = requests_no / video_size

    #         if video_id not in self.videos_rank.keys():
    #             self.videos_rank[video_id] = 0

    #         self.videos_rank[video_id] += req_rank

    #     # once we have all videos initially ranked we have to take under consideration on how many servers they are located
    #     for video_id in self.videos_rank.keys():
    #         # HOTFIX
    #         # Looks that above fix for mapping didn't work here
    #         # we need to check manually if key is in video_distribution
    #         if video_id in self.video_distribution.keys():
    #             self.videos_rank[video_id] /= self.video_distribution[video_id][0]
    #         else: 
    #             self.videos_rank[video_id] = 0

    #     # ok so now we have sorted videos, plenty of them have weight 0 and for sure should be taken out, some others 
    #     # should be 
    #     # for k in sorted(self.videos_rank, key=self.videos_rank.get, reverse=True):
    #     #     print("Video %d -> Rank %d" %(k, self.videos_rank[k]))
        
    # def find_solution_premium_only(self):
    #     # Algorithm 
    #     # - iterate from top to bottom with ranked videos
    #     # - in this simple version we are not running re-ranking, which means we may not get an optimal solution
    #     # - we add videos as much as we have place on cache servers
    #     # - once we reach specific point we need to look for optimal solution with recursion for a moment we just go down the line

    #     # first iterate through videos
    #     for v in sorted(self.videos_rank, key=self.videos_rank.get, reverse=True):
    #         # now iterate through videos and check how many cache servers we have to visit 
    #         # and from each of these cache server go with clusters with higher number

    #         # expected_number_of_cache_servers = self.video_distribution[v][0]
    #         v_size = self.problem.video_sizes[v]

    #         # we go through each larger group of sets
    #         # for each of such group we have to have at least one entry

    #         # HOTFIX
    #         if v not in self.video_to_cache_server.keys():
    #             continue

    #         for k1 in sorted(self.video_to_cache_server[v], key=self.video_to_cache_server[v].get, reverse=True):
    #             # if we reach end of > 0 slots we have distributed inside 'premium' slots
    #             if not self.video_to_cache_server[v][k1] > 0:
    #                 break

    #             set1 = self.string_to_set(k1)
    #             added = False    

    #             # HOTFIX
    #             if v not in self.cache_server_clusters.keys():
    #                 continue

    #             # now we go down the list of all ranked cache servers from top to bottom
    #             # keep in mind set2 may have more than one entry, but we just need a one entry
    #             for k2 in sorted(self.cache_server_clusters[v], key=self.cache_server_clusters[v].get, reverse=True):
    #                 if added: break

    #                 set2 = self.string_to_set(k2)

    #                 for cs in set2:
    #                     if added: break

    #                     if (cs in set1):
    #                         cache_server = self.problem.cache_servers[cs]

    #                         # video will still make on this server
    #                         # yuppi :)
    #                         # no need to go further this loop
    #                         if cache_server.size + v_size <= cache_server.capacity:
    #                             # premium slot taken
    #                             # we increase a number of videos added
    #                             cache_server.add_video(v, v_size)
    #                             self.video_distribution[v][1] += 1
    #                             added = True

    #                             break

    #     for k in sorted(self.problem.cache_servers.keys()):
    #         cache_server = self.problem.cache_servers[k]
    #         print("Cache Server %d Size %d" %(k, cache_server.size))
    #         print(cache_server.videos)



