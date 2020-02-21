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
        h = [int(x) for x in l1.strip().split(" ")]
        problem = libs.Problem(h[0], h[1], h[2])

        l2 = f.readline()
        v = [int(x) for x in l2.strip().split(" ")]
        problem.add_books_score(v)

        library = None
        total = 0
        id = 0

        for l in f:
            if l.strip() == "":
                continue

            if library is None:
                # print(l)
                l = [int(x) for x in l.strip().split(" ")]
                library = libs.Library(problem, id, l[0], l[1], l[2])
                
            else:
                b = [int(x) for x in l.strip().split(" ")]
                library.add_books(b)
                library.order_books()

                problem.add_library(id, library)
                library = None
                id += 1

        return problem

    def write_output(self, problem, solution, suffix='mateusz'):
        new_file_name = self.file_name.replace('.txt', '')

        f = open(self.problem_folder + '/output/' + new_file_name + '_' + suffix + '.out', "w")

        total = 0 
        for lib in solution.scheduled_libraries:
            if len(lib.books_to_deliver) > 0:
                total += 1

        f.write(str(total) + '\n')
        for lib in solution.scheduled_libraries:
            if len(lib.books_to_deliver) == 0:
                continue

            f.write(str(lib.id) + ' ' + str(len(lib.books_to_deliver)) + '\n')
            s = " "
            l = s.join(str(x) for x in lib.books_to_deliver)
            f.write(l + '\n')

        f.close()
