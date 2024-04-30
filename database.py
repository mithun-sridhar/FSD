"""

The Database Class
The Database class should contain the functionalities to:
• check if the file "students.data" exists before using it
• create the file "students.data" if it doesn’t exists
• write objects to the file "students.data"
• read objects from the file "students.data"
• clear the objects from the file “students.data”

"""
import os


class Database:

    def __init__(self):
        pass
    
    def check_create_file(self):
        file_name = "students.data"
        if not os.path.exists(file_name):
            with open(file_name, 'w'):
                print(f"File '{file_name}' created successfully.")
        else:
            print(f"File '{file_name}' already exists.")



    def write_file(self):
        ...



    
    def read_file(self):
        ...
    


    def clear_file_object(self):
        ...