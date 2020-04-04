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
    def __init__(self, id, n_books, signup_days, rate, books):
        self.id = id
        self.n_books = n_books
        self.signup_days = signup_days
        self.books = books
        self.rate = rate
        self.books_score = 0
        self.rating = 0
        self.books_sent_ids = []


class Day:

    def __init__(self, id):
        self.id = id



