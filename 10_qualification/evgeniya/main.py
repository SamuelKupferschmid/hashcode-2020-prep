import os
import models
from utils import *
from operator import attrgetter
from collections import deque

INPUT_DIR = '../input/'
OUTPUT_DIR = '../output/'


def solve(filename):
    data = read_file(INPUT_DIR + filename)
    sim = data['sim']
    libs = data['libs']
    books = data['books']
    print("Finished reading the file")

    libs_sorted = sorted(libs.values(), key=lambda l: l.rating, reverse=True)
    libs_signed_ids = []

    days_left = sim.n_days

    # while days > 0:

    for lib in libs_sorted:
        # signup if can
        if days_left > lib.signup_days:
            # send books with highest scores that are not sent yet
            # subtract score of sent book
            days_left -= lib.signup_days
            libs_signed_ids.append(lib.id)
            books_sorted = deque(sorted(lib.books.keys(), key=lambda x: books[x].score, reverse=True))
            # print(lib.id, len(books_sorted))
            for d in range(days_left):
                for r in range(lib.rate + 1):
                    if len(books_sorted) > 0:
                        sent = books_sorted.popleft()
                        books[sent].score = 0
                        lib.books_sent_ids.append(sent)
                    else:
                        break
        else:
            continue

    # print(libs)


    with open(OUTPUT_DIR + filename[0:-4] + '_evgeniya.out', 'a') as file:
        file.truncate()
        file.write(str(len(libs_signed_ids)) + '\n')
        for id in libs_signed_ids:
            current_lib = libs[id]
            file.write(str(current_lib.id) + ' ' + str(len(current_lib.books_sent_ids)) + '\n')
            file.write(' '.join([str(v) for v in current_lib.books_sent_ids]) + '\n')

# solve('a_example.txt')
# solve('b_read_on.txt')
# solve('c_incunabula.txt')
# solve('d_tough_choices.txt')
# solve('e_so_many_books.txt')
# solve('f_libraries_of_the_world.txt')


for filename in os.listdir(INPUT_DIR):
    if not filename.startswith('.'):
        print('solving ', filename)
        solve(filename)
        print('solved ', filename)
