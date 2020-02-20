from models import *


def read_file(filename):
    file = open(filename, 'r')

    libs = {}
    books = {}


    first_line = file.readline().strip().split(' ')
    sim = Sim(int(first_line[0]), int(first_line[1]), int(first_line[2]))

    books_line = int(file.readline().strip().split(' ')[0])
    for i in range(sim.n_books):
        books[i] = Book(i, books_line[i])

    for j in range(sim.n_libs):
        lib_data = [int(v) for v in file.readline().strip().split(' ')]
        lib_books = [int(v) for v in file.readline().strip().split(' ')]

    file.close()


    return {
        'sim': sim,
        'books': books,
        'libs': libs
    }

