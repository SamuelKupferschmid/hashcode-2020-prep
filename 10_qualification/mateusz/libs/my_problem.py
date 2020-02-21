import math

class Problem:
    def __init__(self, books_no, libs_no, days_no):
        self.books_no = books_no
        self.libs_no = libs_no
        self.days_no = days_no

        self.books_score = {}
        self.libraries = {}

        self.current_books_score = {}

    def add_books_score(self, scores):
        id = 0
        while id < len(scores):
            self.books_score[id] = scores[id]
            id += 1

    def add_library(self, id, library):
        self.libraries[id] = library

class Library:
    def __init__(self, problem, id, books_no, signup_days, ship_per_day):
        self.problem = problem
        self.id = id
        self.books_no = books_no
        self.signup_days = signup_days
        self.ship_per_day = ship_per_day

        self.books = []
        self.ordered_books = []
        # fill it after we signup
        self.books_to_deliver = []

        self.rank = -1
    
    def add_books(self, books):
        self.books = books

    def order_books(self):
        temp = {}

        for b in self.books: 
            temp[b] = self.problem.books_score[b]

        for k in sorted(temp, key=temp.get, reverse=True):
            self.ordered_books.append(k)
    
    def rank_myself(self):
        val = 0
        for b in self.ordered_books:
            val += self.problem.books_score[b]

        # changed signup days to ratio instead of adding them directly
        ratio = self.problem.days_no / self.signup_days
        ratio = math.sqrt(ratio)
        val *= ratio

        ratio2 = self.problem.days_no / math.ceil(len(self.ordered_books) / self.ship_per_day)
        ratio2 *= math.sqrt(ratio2)
        val *= ratio2

        self.rank = val


        # days = math.ceil(len(self.ordered_books) / self.ship_per_day)

        # days = self.signup_days + math.ceil(len(self.ordered_books) / self.ship_per_day)

        # only signup days taken under consideration
        # days = math.ceil(len(self.ordered_books) / self.ship_per_day)

        # self.rank = val / days

    def rank_myself_simple(self):
        val = 0
        for b in self.ordered_books:
            val += self.problem.books_score[b]

        self.rank = val

    def rank_myself_len(self):
        val = len(self.ordered_books)
        self.rank = val

    # after whole iteration we need to rerun ranking one more time
    # probably we have to use second one 
    def remove_book(self, book_id):
        if book_id in ordered_books:
            self.ordered_books.remove(book_id)

    def remove_books(self, book_list):
        self.ordered_books = [x for x in self.ordered_books if x not in book_list]

    def schedule_books(self, current_day):
        delta_days = self.problem.days_no - current_day

        for i in range(delta_days):
            if i * self.ship_per_day > len(self.ordered_books):
                break

            a = i * self.ship_per_day
            b = (i+1) * self.ship_per_day
            self.books_to_deliver.extend(self.ordered_books[a:b])

        # score1 = self.problem.books_score[book_id]

        # for b in self.ordered_books:
        #     score2 = self.problem.books_score[b]
        #     if score1 == score2:
        #         self.order_books.remove(b)
        #         break
        #     elif score1 < score2:
        #         break
