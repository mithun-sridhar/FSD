# importing the necessary libraries for our uni app
import random
import re
import json
import sys
from collections import defaultdict


# ANSI color codes
class colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    

class Student:
  def __init__(self, first_name, last_name, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.id = self.generate_id()
    self.enrolled_subjects = []

    
  # generate a random 6-digit id number for students
  def generate_id(self):
    student_id = str(random.randint(1, 999999))
    return student_id.zfill(6)

  # make sure the email is in the format first.last@university.com
  def is_valid_email(self, email):
    return bool(re.match(r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+@university\.com$", email))

  # password must start with uppercase, have 6 letters and 3 digits at the end (total 9 characaters)
  def is_valid_password(self, password):
    return bool(re.match( r"^[A-Z].{5,}[0-9]{3}$", password))

  # validate student details are correct before adding to database
  def register(self, first_name, last_name, email, password):
    if self.is_valid_email(email) and self.is_valid_password(password):
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.password = password
      self.enrolled_subjects = []
      return True
    else:
      if not self.is_valid_email(email):
          print(colors.RED + "Email format incorrect. Please ensure it is in the following format: first.last@university.com" + colors.RESET)
      if not self.is_valid_password(password):
          print(colors.RED + "Password does not meet requirements. Please ensure it is 6 characters long, starts with a letter, and ends with three digits." + colors.RESET)
      
      return False
      

    
class Subject:
  def __init__(self):
    self.id = str(random.randint(1, 999)).zfill(3)
    self.mark = random.randint(25, 100)
    self.grade = self.calculate_grade()

  def calculate_grade(self):
    if self.mark < 50:
      return "Z"
    elif self.mark < 65:
      return "P"
    elif self.mark < 75:
      return "C"
    elif self.mark < 85:
      return "D"
    else:
      return "HD"


class Database:

  def __init__(self):
     pass

  def load_students(self):
      try:
          with open("students.data", "r") as file:
              data = json.load(file)
              students = []
              for d in data:
                  student = Student(d["first_name"], d["last_name"], d["email"], d["password"])
                  student.enrolled_subjects = []
                  for subject_data in d["enrolled_subjects"]:
                      subject = Subject()
                      subject.mark = subject_data["mark"]
                      subject.grade = subject_data["grade"]
                      student.enrolled_subjects.append(subject)
                  students.append(student)
          return students
      except FileNotFoundError:
          return []
  


  def register_student(self):
      print(colors.GREEN + "Student Registration" + colors.RESET)
      first_name = input("Enter your first name: ").capitalize()
      last_name = input("Enter your last name: ").capitalize()
      email = input("Enter your email: ").lower()
      password = input("Enter your password: ").strip()
      new_student = Student(None, None, None, None) # Create empty student object
      if new_student.register(first_name, last_name, email, password):
        return new_student
      else:
        print(colors.RED + "Registration failed! Please check your email and password format." + colors.RESET)
        return False


  def save_students(self, students):
    data = [{"id": s.id, "first_name": s.first_name, "last_name": s.last_name, "email": s.email, "password": s.password, "enrolled_subjects": [{ "subject_id": subj.id, "mark": subj.mark, "grade": subj.grade } for subj in s.enrolled_subjects]} for s in students]
    with open("students.data", "w") as file:
      json.dump(data, file, indent=4)


class UniAppSystem:

  def __init__(self):
     pass

  
  def student_login(self, email, password):
    try:
      with open('students.data', 'r') as file:
        students = json.load(file)
    except FileNotFoundError:
      return []
    
    # Iterate through each student's data in the file
    for student in students:
        # Check if the email and password match
        if student['email'] == email and student['password'] == password:
            return student  # Credentials match
    return None  # No match found
    
            
  def student_menu(self, students):
      while True:
            print(colors.BLUE + "\nStudent Menu:")
            print("(l) Login as student")
            print("(r) Register as student")
            print("(x) Exit")
            choice = input("Enter your choice: " + colors.RESET).lower()

            database = Database()

            match choice:
              
              case 'l':
                print(colors.GREEN + "Student Login" + colors.RESET)
                email = input("Enter email: ").lower()
                password = input("Enter password: ")
                student = self.student_login(email, password)
                if student:
                  print(colors.YELLOW + "Login successful. Transferring to student course menu." + colors.RESET)
                  self.student_course_menu(student)
                  database.save_students(students)
                else:
                   print(colors.RED + "Login unsuccessful, please try again." + colors.RESET)
                
                  
              
              case 'r':
                students = database.load_students()

                new_student = database.register_student()
                if new_student:
                  students_data = database.load_students()
                  new_student_email = new_student.email

                  # Check if the student's email is already in the database before adding them in
                  email_exists = any(student.email == new_student_email for student in students_data)
                  if email_exists == False:
                    students.append(new_student)
                    database.save_students(students)
                    print(colors.YELLOW + "Registration successful! Please login to proceed." + colors.RESET)
                  else:
                    print(colors.RED + f"Student already exists." + colors.RESET)
                
              
              case 'x':
                  print(colors.YELLOW + "Exiting Student Menu, returning to System menu." + colors.RESET)
                  self.main()
              
              case _:
                  print(colors.RED + "Invalid choice, please try again." + colors.RESET)
                  
                  


  def student_course_menu(self, student):
      while True:
        print(colors.BLUE + "\nStudent Course Menu:")
        print("(e) Enrol into a subject")
        print("(r) Remove a subject from enrolment")
        print("(s) Show current enrolment")
        print("(c) Change password")
        print("(x) Logout")
        choice = input("Enter your choice: " + colors.RESET)

        match choice:
            # enrol into subject
            case 'e':
              try:
                with open('students.data', 'r') as file:
                  students = json.load(file)
              except FileNotFoundError:
                return []
              
              student1 = next((s for s in students if s['id'] == student['id']), None)
              
              if len(student1['enrolled_subjects']) < 4:
                new_subject = Subject()
                student1['enrolled_subjects'].append({
                    "subject_id": new_subject.id,
                    "mark": new_subject.mark,
                    "grade": new_subject.grade
                })
                num_enrolled = len(student1['enrolled_subjects'])
                print(colors.YELLOW + f"Enrolled successfully into subject {new_subject.id}" + colors.RESET)
                print(colors.GREEN + f"You are now enrolled in {num_enrolled} out of 4 subjects." + colors.RESET)
              else:
                print(colors.RED + "Maximum enrolment reached (4 subjects)" + colors.RESET)

              # Save the updated student data to the file
              with open('students.data', 'w') as file:
                json.dump(students, file, indent=4)
              

            # remove subject
            case 'r':
                try:
                  with open('students.data', 'r') as file:
                      students_data = json.load(file)
                except FileNotFoundError:
                    print(colors.RED + "File not found error. Please try again." + colors.RESET)
                    return
                
                list_ids = []
                for student1 in students_data:
                  if student1['id'] == student['id']:
                    for subject in student1['enrolled_subjects']:
                        list_ids.append(subject['subject_id'])
                
                print(colors.MAGENTA + f"Subject ID's in enrollment: {list_ids}" + colors.RESET)

                id_remove = input("Enter subject id to remove: ")

                for student2 in students_data:
                    if student2['id'] == student['id']:
                        enrolled_subjects = student2.get('enrolled_subjects', [])
                        for subject in enrolled_subjects:
                            if subject['subject_id'] == id_remove:
                                enrolled_subjects.remove(subject)
                                print(colors.YELLOW + f"Subject {id_remove} has been removed successfully." + colors.RESET)
                                break
                        else:
                            print(colors.RED + "Subject not found in student's enrollment list. Please try again." + colors.RESET)
                        break
                else:
                    print(colors.RED + f"Student with ID {student['id']} not found." + colors.RESET)

                with open('students.data', 'w') as file:
                    json.dump(students_data, file, indent=4)
                              

            # show enrolment
            case 's':
                try:
                  with open('students.data', 'r') as file:
                    students = json.load(file)
                except FileNotFoundError:
                  return []
                
                student1 = next((s for s in students if s['id'] == student['id']), None)

                for student1 in students:
                  if len(student1['enrolled_subjects']) > 0 and student1['id'] == student['id']:
                      print(colors.GREEN + "\nEnrolled Subjects:" + colors.RESET)
                      for i, subject in enumerate(student1['enrolled_subjects']):
                          print(f"{i+1}. Subject ID: {subject['subject_id']}, Mark: {subject['mark']}, Grade: {subject['grade']}")
                  elif len(student1['enrolled_subjects']) == 0 and student1['id'] == student['id']:
                      print(colors.YELLOW + "Showing 0 subjects - no subjects enrolled" + colors.RESET)
                
            # change password
            case 'c':
                while True:
                  new_password = input("Enter new password: ")
                  confirm_password = input("Confirm password: ")
                  if new_password != confirm_password:
                     print(colors.RED + "Passwords do not match, please try again." + colors.RESET)
                     continue
                  else:
                     break
  
                try:
                  with open('students.data', 'r') as file:
                    students = json.load(file)
                except FileNotFoundError:
                  print("File not found error. Please check the file path.")
                  return
                
                # creating an empty instance of the object student so we can use the is_valid_password function
                function = Student(None, None, None, None)

                # Find the student with the specified ID
                for student1 in students:
                    if student1['id'] == student['id'] and function.is_valid_password(new_password):
                        # Update the password
                        student1['password'] = new_password
                        print(colors.GREEN + f"Password updated successfully." + colors.RESET)
                        break
                else:
                    print(colors.RED + "Invalid password format! Please try again." + colors.RESET)
                    print(colors.MAGENTA + "Note: Password must have at least 6 characters total, beginning with an uppercase, and last three characters must be digits." + colors.RESET)

                # Save the modified data back to the file
                with open('students.data', 'w') as file:
                    json.dump(students, file, indent=4)

            # exit system
            case 'x':
                print(colors.YELLOW + "Logged out!" + colors.RESET)
                self.student_menu(students)

            case _:
                print(colors.RED + "Invalid choice, please try again." + colors.RESET)

          
  def group_by_grade(self):

      students1 = []
      
      # Print if there are no students
      try:
          with open('students.data', 'r') as file:
              students1 = json.load(file)
      except FileNotFoundError:
          print(colors.RED + "File not found error --> file has been created, please login to system again." + colors.RESET)
          return []

      if len(students1) == 0:
          print("\t<Nothing to display>")
          return

        # Group subjects by grade
      subjects_by_grade = defaultdict(list)
      for student in students1:
          for subject in student['enrolled_subjects']:
              grade = subject['grade']
              subjects_by_grade[grade].append({
                  "student_name": f"{student['first_name']} {student['last_name']}",
                  "email": student['email'],
                  "subject_id": subject['subject_id'],
                  "mark": subject['mark']
              })

      # Define the custom order for grades
      grade_order = ["HD", "D", "C", "P", "Z"]

      # Print subjects grouped by grade in the custom order
      for grade in grade_order:
          if grade in subjects_by_grade and subjects_by_grade[grade]:
              print("\n")
              print(colors.YELLOW + f"Subjects with grade {grade}:" + colors.RESET)
              for subject in subjects_by_grade[grade]:
                  print(f"Student: {subject['student_name']}, Email: {subject['email']}, Subject: {subject['subject_id']}, Subject Mark: {subject['mark']}")



  def partition_pass_fail(self):

    passed_students = []
    failed_students = []

    try:
      with open('students.data', 'r') as file:
        students = json.load(file)
    except FileNotFoundError:
      print(colors.RED + "File not found error --> file has been created, please login to system again." + colors.RESET)
      return []

    for student in students:
        total_marks = sum(subject['mark'] for subject in student['enrolled_subjects'])
        average_score = total_marks / len(student['enrolled_subjects']) if student['enrolled_subjects'] else 0

        if average_score >= 50:
            passed_students.append(student)
        else:
            failed_students.append(student)

    print(colors.YELLOW + "\nPASS:" + colors.RESET)
    if len(passed_students) == 0:
           print("\t<Nothing to display>")
    # Create a set to store unique student names who passed
    student_names_passed = set()

    for student in passed_students:
        total_marks = sum(subject['mark'] for subject in student['enrolled_subjects'])
        average_score = total_marks / len(student['enrolled_subjects']) if student['enrolled_subjects'] else 0
        name = f"ID: {student['id']} {student['first_name']} {student['last_name']}, GPA: {average_score:.2f}"
        student_names_passed.add(name)
        

    # Print each unique student name
    for name in student_names_passed:
        print(f"- {name}")
    
    print(colors.YELLOW + "\nFAIL:" + colors.RESET)
    if len(failed_students) == 0:
        print("\t<Nothing to display>")
    else:
        # Create a set to store unique student names who failed
        student_names_failed = set()
        for student in failed_students:
            total_marks = sum(subject['mark'] for subject in student['enrolled_subjects'])
            average_score = total_marks / len(student["enrolled_subjects"]) if student['enrolled_subjects'] else 0
            name = f"ID: {student['id']} {student['first_name']} {student['last_name']}, GPA: {average_score:.2f}"
            student_names_failed.add(name)

        # Print each unique student name
        for name in student_names_failed:
            print(f"- {name}")

    

        
        


  def admin_menu(self, students):
        while True:
            print(colors.BLUE + "\nAdmin Menu:")
            print("(s) Show all students")
            print("(g) Group students by grade")
            print("(p) Partition students by PASS/FAIL category")
            print("(r) Remove a student")
            print("(c) Clear all student data")
            print("(x) Exit")
            choice = input("Enter your choice: " + colors.RESET).lower()

            match choice:
                # show all students
                case 's':
                    try:
                      with open('students.data', 'r') as file:
                        students1 = json.load(file)
                    except FileNotFoundError:
                      print(colors.RED + "File not found error --> file has been created, please login to system again." + colors.RESET)
                      return []


                    print(colors.YELLOW + "\nAll Students:" + colors.RESET)
                    for student in students1:
                        print(f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, Email: {student['email']}")
                    if len(students1) == 0:
                      print("\t<Nothing to display>")

                # group students by grade
                case 'g':
                    self.group_by_grade()

                # partition students by pass/fail category
                case 'p':
                    self.partition_pass_fail()

                # remove a student
                case 'r':
                    print(colors.GREEN + "Remove Student Account" + colors.RESET)

                    with open('students.data', 'r') as file:
                      students = json.load(file)

                    list_ids = []
                    for student in students:
                       list_ids.append(student['id'])
                    
                    print(colors.MAGENTA + f"Student ID's in database: {list_ids}" + colors.RESET)

                    id = input("Enter student id to remove: ")
                    
                    for student in students:
                      if student['id'] == id:
                        students.remove(student)
                        print(colors.YELLOW + "Student has been removed successfully." + colors.RESET)
                        break
                    
                    if id not in list_ids:
                      print(colors.RED + "Student not found in database. Please try again." + colors.RESET)  
                      
                    # Write the modified data back to the original file
                    with open('students.data', 'w') as file:
                        json.dump(students, file, indent=4) 

          

                # clear all student data
                case 'c':
                    confirmation = input(colors.RED + "Are you sure you want to clear all student data? (y/n): " + colors.RESET)
                    if confirmation.lower() == "y":
                      try:
                        with open("students.data", "w") as file:
                            json.dump([], file)
                        print(colors.YELLOW + "All student data cleared!" + colors.RESET)
                      except FileNotFoundError:
                        print(colors.RED + "Unable to clear student data." + colors.RESET)

                #exit admin system, return to main menu
                case 'x':
                    print(colors.YELLOW + "Exiting admin menu" + colors.RESET)
                    self.main()
        
                # catch any invalid input
                case _:
                    print(colors.RED + "Invalid input, please try again." + colors.RESET)


  def main(self):
      
      database = Database()
      students = database.load_students()

      while True:
        print(colors.BLUE + "\nCLIUniApp - University Enrolment System")
        print("(S) Enter Student System")
        print("(A) Enter Admin System")
        print("(X) Exit")
        choice = input("Enter your choice: " + colors.RESET).lower()
        
        match choice:
          
          case 's':
            self.student_menu(students)
            database.save_students(students)
            break

          case 'a':
            self.admin_menu(students)
            database.save_students(students)
            break

          case 'x':
            print(colors.YELLOW + "Exiting CLIUniApp!" + colors.RESET)
            sys.exit()
          
          case _:
            print(colors.RED + "Invalid choice!" + colors.RESET)
            
   



if __name__ == "__main__":
  app = UniAppSystem()
  app.main()