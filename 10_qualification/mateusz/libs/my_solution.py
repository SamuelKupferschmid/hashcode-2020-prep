import math

SEPARATOR = ":"

class Solution: 
    def __init__(self, problem=None):
        self.problem = problem

        self.library_rank = {}
        self.libraries_ranked = []
        self.scheduled_libraries = []

        self.library_rank_len = {}
        self.libraries_ranked_len = []

    def rank_libraries(self):
        for k in self.problem.libraries.keys():
            l = self.problem.libraries[k]
            l.rank_myself()

            self.library_rank[k] = l.rank

        for k in sorted(self.library_rank, key=self.library_rank.get, reverse=True):
            self.libraries_ranked.append(k)

    def re_rank_libraries(self):
        # iterate through libraries which are still present
        # rank was already recalculated

        # init empty with 0
        self.library_rank = {}
        for k in self.libraries_ranked:
            l = self.problem.libraries[k]
            self.library_rank[k] = l.rank

        # init with empty
        self.libraries_ranked = []
        for k in sorted(self.library_rank, key=self.library_rank.get, reverse=True):
            self.libraries_ranked.append(k)

    def find_solution(self):
        current_day = 0
        
        # first we schedule from the highest rank library
        while current_day < self.problem.days_no:
            if not len(self.libraries_ranked) > 0:
                break

            l1 = self.libraries_ranked.pop(0)
            library1 = self.problem.libraries[l1]

            self.scheduled_libraries.append(library1)
            current_day += library1.signup_days
            library1.schedule_books(current_day)

            # remove scheduled books from each other library and re rank them
            for l2 in self.libraries_ranked:
                library2 = self.problem.libraries[l2]
                library2.remove_books(library1.books_to_deliver)
                library2.rank_myself()

            # reranking libraries according to new values
            self.re_rank_libraries()

    def rank_libraries_len(self):
        for k in self.problem.libraries.keys():
            l = self.problem.libraries[k]
            l.rank_myself_len()

            self.library_rank_len[k] = l.rank

        for k in sorted(self.library_rank_len, key=self.library_rank_len.get, reverse=True):
            self.libraries_ranked_len.append(k)

    def re_rank_libraries_len(self):
        self.library_rank_len = {}
        for k in self.libraries_ranked_len:
            l = self.problem.libraries[k]
            self.library_rank_len[k] = l.rank

        self.libraries_ranked_len = []
        for k in sorted(self.library_rank_len, key=self.library_rank_len.get, reverse=True):
            self.libraries_ranked_len.append(k)

    # special case for finding a solution D - here we need to have a rank in different way done 
    # from longest to shortest
    def find_solution_d(self):
        current_day = 0

        # first we schedule from the highest rank library
        while current_day < self.problem.days_no:
            if not len(self.libraries_ranked_len) > 0:
                break

            l1 = self.libraries_ranked_len.pop(0)
            library1 = self.problem.libraries[l1]

            self.scheduled_libraries.append(library1)
            current_day += library1.signup_days
            library1.schedule_books(current_day)

            # remove scheduled books from each other library and re rank them
            # for l2 in self.libraries_ranked_len:
            #     library2 = self.problem.libraries[l2]
                # library2.remove_books(library1.books_to_deliver)
                # library2.rank_myself_len()

            # reranking libraries according to new values
            # self.re_rank_libraries_len()

    # def string_to_set(self, str_key):
    #     set_key = set(int(x) for x in str_key.split(SEPARATOR))
    #     return set_key

    # def set_to_string(self, set_key):
    #     sorted_set = sorted(set_key)
    #     str_key = SEPARATOR.join(str(x) for x in sorted_set)
    #     return str_key

    # # what happenes if we have zone 5.5?
    # def local_to_utc(self, local_time, zone):
    #     utc_time = local_time - timedelta(hours=zone)
    #     return utc_time

    # def utc_to_local(self, utc_time, zone):
    #     local_time = utc_time + timedelta(hours=zone)
    #     return local_time

    # def distance_matrix(self, x1, y1, x2, y2):
    #     result = abs(x1 - x2) + abs(y1 - y2)
    #     return result

    # def distance_euclidan(self, x1, y1, x2, y2):
    #     x = abs(x1 - x2) ** 2
    #     y = abs(y1 - y2) ** 2
    #     result = math.sqrt(x + y)
    #     return result

    # def distance_euclidan_3d(self, x1, y1, z1, x2, y2, z2):
    #     x = abs(x1 - x2) ** 2
    #     y = abs(y1 - y2) ** 2
    #     z = abs(z1 - z2) ** 2
    #     result = math.sqrt(x + y + z)
    #     return result

    # def convert_to_angle(self, degree, arcminute, arcsecond):
    #     # maybe later 
    #     # we need to consider a negative in terms of nort and south

    #     return angle

    # def distance_geo(self, latitude1, longitude1, latitude2, longitude2):
    #     r = 6371
    #     # ratio = 180 / math.pi
    #     # long1 = longitude1 / ratio
    #     # lat1 = latitude1 / ratio
    #     # long2 = longitude2 / ratio
    #     # lat2 = latitude2 / ratio
    #     lat1 = math.radians(latitude1)
    #     long1 = math.radians(longitude1)
    #     lat2 = math.radians(latitude2)
    #     long2 = math.radians(longitude2)

    #     a = math.sin(lat1) * math.sin(lat2)
    #     b = math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)
    #     d = r * math.acos(a + b)

    #     # dlon = long2 - long1  
    #     # dlat = lat2 - lat1 
    #     # a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    #     # c = 2 * math.asin(math.sqrt(a))
    #     # d = c * r

    #     return d


