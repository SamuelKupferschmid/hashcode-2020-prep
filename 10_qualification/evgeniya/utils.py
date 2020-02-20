from models import *


def read_file(filename):
    file = open(filename, 'r')

    first_line = file.readline().strip().split(' ')
    sim = Sim(int(first_line[0]), int(first_line[1]), int(first_line[2]), int(first_line[3]), int(first_line[4]))

    file.close()

    return {
        'sim': sim
    }

