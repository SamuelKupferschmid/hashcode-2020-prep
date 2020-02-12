import sys
import libs
from datetime import datetime

def main():
    # read input parameters
    if len(sys.argv) < 2:
        print("Not enough parameters")
        sys.exit(0)

    my_file = sys.argv[1]

    if len(sys.argv) > 2:
        my_folder = sys.argv[2]
        io = libs.IO(my_file, my_folder)
    else: 
        io = libs.IO(my_file)
    
    
    problem = io.read_input()

    print("Videos: %d" %(problem.videos_no))
    print("Endpoints: %d" %(problem.endpoints_no))
    print("Descriptions: %d" %(problem.request_descriptions_no))
    print("Cache Servers: %d" %(problem.cache_servers_no))
    print("Cache Capacity: %d" %(problem.cache_server_capacity))
    print("Videos %d" %(len(problem.video_sizes)))
    # print(problem.video_sizes)
    print("Endpoints %d" %(len(problem.endpoints.keys())))
    # for k in sorted(problem.endpoints.keys()):
    #     e = problem.endpoints[k]
    #     print("Endpoint id: %d" %(e.id))
    #     print("Endpoint latency: %d" %(e.latency))
    #     print("Endpoint connected cache server no: %d" %(e.connnected_cache_servers_no))
    #     print(e.cache_servers)
    print("Requests %d" %(len(problem.requests)))
    # for r in problem.requests:
    #     print("%d -> %d | %d" %(r.video_id, r.endpoint_id, r.requests_no))
    print("Cache Servers %d" %(len(problem.cache_servers.keys())))
    # for k in sorted(problem.cache_servers.keys()):
    #     cs = problem.cache_servers[k]
    #     print("%d %d / %d" %(cs.server_id, cs.size, cs.capacity))
    #     print(cs.videos)

    solution = libs.Solution(problem)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Map videos to cache", current_time)
    solution.map_videos_to_cache()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Create Cache Clusters", current_time)
    solution.create_cache_clusters()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Rank Videos", current_time)
    solution.rank_videos()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Find Solution Premium Only", current_time)
    solution.find_solution_premium_only()

    print("Final Score %s: %d" %(my_file, solution.count_score()))


if __name__ == "__main__":
    main()