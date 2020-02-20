from models import *


def read_file(filename):
    file = open(filename, 'r')

    libs = {}
    books = {}


    first_line = file.readline().strip().split(' ')
    sim = Sim(int(first_line[0]), int(first_line[1]), int(first_line[2]))

    books_line = file.readline().strip().split(' ')
    for i in range(sim.n_books):
        books[i] = Book(i, int(books_line[i]))

    for j in range(sim.n_libs):
        lib_data = [int(v) for v in file.readline().strip().split(' ')]
        lib_books = [int(v) for v in file.readline().strip().split(' ')]
        libs[j] = Library(j, lib_data[0], lib_data[1], lib_data[2], dict(zip(lib_books, [False] * lib_data[0])))
        libs[j].books_score = sum([books[id].score for id in lib_books])
        libs[j].rating = get_lib_rating(libs[j], sim.n_days)

    file.close()


    return {
        'sim': sim,
        'books': books,
        'libs': libs
    }


def get_lib_rating (lib, total_days):
    # return - lib.signup_days + lib.books_score * lib.rate / lib.n_books
    return (lib.books_score * lib.rate / lib.n_books) * (1  - lib.signup_days / total_days)