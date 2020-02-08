import sys
import libs

def main():
    # read input parameters
    if len(sys.argv) < 2:
        print("Not enough parameters")
        sys.exit(0)

    my_file = sys.argv[1]
    io = IO(my_file)


if __name__ == "__main__":
    main()