class Sim:
    def __init__(self, books, libs, days):
        self.n_books = books
        self.n_libs = libs
        self.n_days = days


class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score


class Library:
    def __init__(self, id, signup_days, books, rate):
        self.id = id
        self.signup_days = signup_days
        self.books = books
        self.rate = rate


class Day:

    def __init__(self, id):
        self.id = id



