import sys

import my_io
import my_debug
import my_init
import my_analysis


# read input parameters
if len(sys.argv) < 2:
    print("Not enough parameters")
    sys.exit(0)

my_file = sys.argv[1]

n_rows,  n_columns, n_vechicles, n_rides, bonus, n_steps, rides_raw = my_io.read_input(my_file)
my_debug.print_parameters({
    "n_rows": n_rows, 
    "n_columns": n_columns, 
    "n_vechicles": n_vechicles, 
    "n_rides": n_rides, 
    "bonus": bonus, 
    "n_steps": n_steps
    })
my_debug.print_entries_arr('ride', rides_raw)

# collect and display metrics
# - distribution of distances at rides
# - distribution of max time for each ride
# - distribution of distances between each node - this we need to write with algorithm

nodes_arr, nodes_dict = my_init.create_nodes(n_rows, n_columns)
rides_dict = my_init.process_rides(rides_raw, nodes_arr)
my_debug.print_entries_dict('ride', rides_dict)


