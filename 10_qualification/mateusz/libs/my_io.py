import os
import libs

LOCAL_FOLDER = "/mateusz"

class IO:
    def __init__(self, file_name, folder_name=""):
        self.file_name = file_name

        cwd = os.getcwd()
        if cwd.endswith(LOCAL_FOLDER):
            self.problem_folder = cwd.replace(LOCAL_FOLDER, '')
        else: 
            self.problem_folder = cwd + folder_name

        # print(self.file_name)
        # print(self.problem_folder)

    def read_input(self):
        f = open(self.problem_folder + '/input/' + self.file_name, "r")

        l1 = f.readline()
        # header = l1.strip().split(" ")
        # problem = Problem(int(header[0]), int(header[1]), int(header[2]), int(header[3]), int(header[4]))
        h = [int(x) for x in l1.strip().split(" ")]
        problem = libs.Problem(h[0], h[1], h[2], h[3], h[4])

        l2 = f.readline()
        v = [int(x) for x in l2.strip().split(" ")]
        problem.add_video_sizes(v)

        endpoint = None
        total = 0
        id = 0

        for l in f:
            if endpoint is None:
                e = [int(x) for x in l.strip().split(" ")]
                endpoint = libs.Endpoint(id, e[0], e[1])
                id += 1
            else: 
                c = [int(x) for x in l.strip().split(" ")]
                endpoint.add_cache_server(c[0], c[1])
                total += 1

            if total == endpoint.connnected_cache_servers_no:
                problem.add_endpoint(endpoint)

                endpoint = None
                total = 0
                
                if id == problem.endpoints_no:
                    break

        for l in f:
            r = [int(x) for x in l.strip().split(" ")]
            request = libs.Request(r[0], r[1], r[2])
            problem.add_request(request)

        problem.init_cache_servers()

        return problem


    def write_output(self, problem, score, suffix='mateusz'):
        new_file_name = self.file_name.replace('.in', '')
        f = open(self.problem_folder + '/output/' + new_file_name + '_' + str(score) + '_' + suffix + '.out', "w")

        cache_servers_count = 0
        for k in problem.cache_servers.keys():
            if problem.cache_servers[k].size > 0:
                cache_servers_count += 1
        
        f.write(str(cache_servers_count) + '\n')
        for k in problem.cache_servers.keys():
            cache_server = problem.cache_servers[k]
            if cache_server.size > 0:
                sorted_set = sorted(cache_server.videos)
                str_videos = ' '.join(str(x) for x in sorted_set)
                str_final = str(k) + ' ' + str_videos + '\n'
                f.write(str_final)


        f.close()
    
