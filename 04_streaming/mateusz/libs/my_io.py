import os

LOCAL_FOLDER = "mateusz"

class IO:
    def __init__(self, file_name):
        self.file_name = file_name

        cwd = os.getcwd()
        if cwd.endswith(LOCAL_FOLDER):
            self.current_folder = cwd
            self.ide = False
        else: 
            self.current_folder = cwd
            self.ide = True

        print(self.file_name)
        print(self.current_folder)
        print(self.ide)

    def read_input():
        print("foo")

            


    def write_output():
        print("bar")



