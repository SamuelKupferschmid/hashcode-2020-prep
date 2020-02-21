import sys
import libs
from datetime import datetime

# to run from VS Code add following entries to launch.json in main folder
# "args": ["file1.in", "/10_qualification"]
# // "args": ["file2.in", "/10_qualification"]
# // "args": ["file3.in", "/10_qualification"]
# // "args": ["file4.in", "/10_qualification"]

# to run from command line go to specific folder and then just run with file name 
# python3 main.py input_file.in

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
    solution = libs.Solution(problem)
    # solution.rank_libraries()
    # solution.find_solution()

    solution.rank_libraries_len()
    solution.find_solution_d()


    io.write_output(problem, solution)

if __name__ == "__main__":
    main()