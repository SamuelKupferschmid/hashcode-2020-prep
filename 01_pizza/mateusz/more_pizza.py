def read_input(file_name):
    f = open(file_name, "r")
    
    l1 = f.readline()
    n1 = l1.split(" ")
    slices = int(n1[0])
    types = int(n1[1])
    
    l2 = f.readline()
    n2 = l2.split(" ")
    
    slice_list = []
    for x in n2:
        slice_list.append(int(x))
    
    return slices, types, slice_list

# special case - check if available slices do form a total solution
def whole_pizza():
    local_sum = 0
    for x in slice_list:
        local_sum += x
    
    if local_sum == max_slices:
        print("Eat all pizza slices %d" %(local_sum))
    else:
        print("I can't eat that much :( %d" %(local_sum))
    
# iterative solution
def iter_pizza():
    # we will go through each possible state, pizza can be turned on / off, obviously this will lead to O(n^2) solution
    # but let's do it for a training and possible narrow cases checks, if we would have enough power we could divide 
    # and resolve it on multiple platforms, let's see how it will perform for 1000 entries 
    #
    # first all markers are set to 0 and we iterate from the end adding one to each cell
    marker = [0] * types_no
    
    # count maximum iterations
    max_checks = 2 ** types_no 
    max_sum = 0
    max_slice_list = []
    
    i = 0
    while True:
        # do check even for initial setup cause we want to have all nice round number of cases
        # some checks, total sum, need to iterate through whole list
        # count a local sum and compare with 
        # here would be good to do some filtering on operations on 2 matrixes

        local_sum = 0
        j = 0
        while True:
            local_sum += marker[j] * slice_list[j]

            j += 1
            if j >= types_no:
                break

        # check if conditions are fulfilled, if yes overwrite max_slice_list
        if local_sum > max_sum and local_sum <=max_slices:
            max_sum = local_sum
            max_slice_list = []

            print("%d: %s -> %s" %(i, max_slice_list, max_sum))

            j = 0
            while True:
                if marker[j] != 0:
                    max_slice_list.append(slice_list[j])
                    
                j += 1
                if j >= types_no:
                    break
        
        # in case we find an optimal solution we finish 
        if max_sum == max_slices:
            break

#         print("%d: %s -> %s" %(i, marker, local_sum))
            
        i += 1
        # check if we reached the end
        if i >= max_checks:
            break
        
        # modify marker table
        # first set an index and add '1' to last element, we don't have to check first state it's empty so and so 
        index = types_no - 1
        
        while True:
            marker[index] = (marker[index] + 1) % 2
            
            if marker[index] == 1:
                break
            else:
                index = index - 1
                
    print(max_slice_list)

# TODO - work in progress
# greedy algorithm pizza
def greedy_pizza():
    # we initiate a list with total sums till this element may come in handy to evaluate when to start some detailed computation
    # it could be at 20 - 40 items to go to have a realistic valuec
    slices_sum = [0] * types_no
    i = 0

    # init to not fall outside
    slices_sum[i] = slice_list[i]
    i += 1
    
    # we start with second cell
    while True:
        slices_sum[i] = slice_list[i] + slices_sum[i-1] 
        
        i += 1
        if i >= types_no:
            break
            
    print(slice_list)
    print(slices_sum)
    
    # first we start with largest pieces and we go down with pointer


#############
### Main Part
#############

import sys

# statics definition
file = ["a_example.in", "b_small.in", "c_medium.in", "d_quite_big.in", "e_also_big.in"] 

if len(sys.argv) < 2:
    print("Not enough parameters")
    sys.exit(0)

pizza_file = sys.argv[1]

max_slices, types_no, slice_list = read_input(pizza_file)
# print(max_slices)
# print(types_no)
# print(slice_list)

whole_pizza()
iter_pizza()
# greedy_pizza()


