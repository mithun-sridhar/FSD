# importing the necessary libraries for our uni app
import random
import re
import json
import sys

class Student:
  def __init__(self, first_name, last_name, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.id = self.generate_id()
    self.enrolled_subjects = []

  def generate_id(self):
    student_id = str(random.randint(1, 999999))
    return student_id.zfill(6)


  def is_valid_email(self, email):
    return bool(email.endswith("@university.com") and ("@" in email) and ("." in email))

  #password must start with uppercase, have 6 letters and 3 digits at the end (total 9 characaters)
  def is_valid_password(self, password):
    return bool(re.match( r"^[A-Z].{5,}[0-9]{3}$", password))


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
          print("Email format incorrect. Please ensure it is in the following format: first.last@university.com")
      if not self.is_valid_password(password):
          print("Password does not meet requirements. Please ensure it is 6 characters long, starts with a letter, and ends with three digits.")
      
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
  
  def load_student_file(self):
    try:
      with open('students.data', 'r') as file:
          data = json.load(file)
          return data
    except FileNotFoundError:
       return [] 

  def register_student(self):
      first_name = input("Enter your first name: ").capitalize()
      last_name = input("Enter your last name: ").capitalize()
      email = input("Enter your email: ").lower()
      password = input("Enter your password: ").strip()
      new_student = Student(None, None, None, None) # Create empty student object
      if new_student.register(first_name, last_name, email, password):
        return new_student
      else:
        print("Registration failed! Please check your email and password format.")
        return False


  def save_students(self, students):
    data = [{"id": s.id, "first_name": s.first_name, "last_name": s.last_name, "email": s.email, "password": s.password, "enrolled_subjects": [{ "mark": subj.mark, "grade": subj.grade } for subj in s.enrolled_subjects]} for s in students]
    with open("students.data", "w") as file:
      json.dump(data, file)


class UniAppSystem:

  def __init__(self):
     pass

  
  def student_login(self, students):
    email = input("Enter email: ").lower()
    password = input("Enter password: ")
    for student in students:
      if student.email != email or student.password != password or not student:
          print("Invalid login credentials!")
          return None
      else:
        return student

    
            
  def student_menu(self, students):
      while True:
            print("\nStudent Menu:")
            print("(l) Login as student")
            print("(r) Register as student")
            print("(x) Exit")
            choice = input("Enter your choice: ").lower()

            database = Database()

            match choice:
              
              case 'l':
                student = self.student_login(students)
                if student:
                  print("Login successful. Transferring to student course menu.")
                  self.student_course_menu(student)
                  database.save_students(students)
                  
              
              case 'r':
                students = database.load_students()

                new_student = database.register_student()
                if new_student:
                  students_data = database.load_student_file()
                  new_student_email = new_student.email

                  # Check if the student's email is already in the database before adding them in
                  email_exists = any(student.get("email") == new_student_email for student in students_data)
                  if email_exists == False:
                    students.append(new_student)
                    database.save_students(students)
                    print("Registration successful! Please login to proceed.")
                  else:
                    print(f"Student already exists.")
                
              
              case 'x':
                  print("Exiting Student Menu, returning to System menu.")
                  self.main()
              
              case _:
                  print("Invalid choice, please try again.")
                  
                  


  def student_course_menu(self, student):
      while True:
        print("\nStudent Course Menu:")
        print("(e) Enrol into a subject")
        print("(r) Remove a subject from enrolment")
        print("(s) Show current enrolment")
        print("(c) Change password")
        print("(x) Logout")
        choice = input("Enter your choice: ")

        match choice:
            # enrol into subject
            case 'e':
                if len(student.enrolled_subjects) < 4:
                    subject_enrolled = Subject()
                    student.enrolled_subjects.append(subject_enrolled)
                    num_enrolled = len(student.enrolled_subjects)
                    print(f"Enrolled successfully into subject {subject_enrolled.id}")
                    print(f"You are now enrolled in {num_enrolled} out of 4 subjects.")
                else:
                    print("Maximum enrolment reached (4 subjects)")

            # remove subject
            case 'r':
                if student.enrolled_subjects:
                    subject_removed = student.enrolled_subjects.pop()
                    print(f"Subject {subject_removed.id} removed!")
                else:
                    print("No subjects enrolled!")

            # show enrolment
            case 's':
                if student.enrolled_subjects:
                    print("\nEnrolled Subjects:")
                    for i, subject in enumerate(student.enrolled_subjects):
                        print(f"{i+1}. Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
                else:
                    print("No subjects enrolled!")

            # change password
            case 'c':
                while True:
                  new_password = input("Enter new password: ")
                  confirm_password = input("Confirm password: ")
                  if new_password != confirm_password:
                     print("Passwords do not match, please try again.")
                     continue
                  else:
                     break
                if student.is_valid_password(new_password):
                    student.password = new_password
                    print("Password changed successfully!")
                else:
                    print("Invalid password format! Please try again.")
                    print("Note: Password must have at least 6 characters total, beginning with an uppercase, and last three characters must be digits.")

            # exit system
            case 'x':
                print("Logged out!")
                return

            case _:
                print("Invalid choice, please try again.")

          
  def group_by_grade(self, database):

    students_data = database.load_student_file()

    # Define a dictionary to store students grouped by grade
    students_by_grade = {"HD": [], "D": [], "C": [], "P": [], "Z": []}

    # Group students by grade
    for student in students_data:
        enrolled_subjects = student.get("enrolled_subjects", [])
        for subject in enrolled_subjects:
            grade = subject.get("grade")
            if grade in students_by_grade:
                students_by_grade[grade].append(student)

    # Print students grouped by grade
    for grade, students in students_by_grade.items():
        if students:
            print("\n")
            print(f"Students with grade {grade}:")
            for student in students:
                for subject in student["enrolled_subjects"]:
                  print(f"{student['first_name']} {student['last_name']} - {student['email']} - {student['id']}: {subject['mark']}")
            return print()


  def admin_menu(self, students):
        while True:
            print("\nAdmin Menu:")
            print("(s) Show all students")
            print("(g) Group students by grade")
            print("(p) Partition students by PASS/FAIL category")
            print("(r) Remove a student")
            print("(c) Clear all student data")
            print("(x) Exit")
            choice = input("Enter your choice: ").lower()

            match choice:
                # show all students
                case 's':
                    print("\nAll Students:")
                    for student in students:
                        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Email: {student.email}")

                # group students by grade
                case 'g':
                    self.group_by_grade(database = Database())

                # partition students by pass/fail category
                case 'p':
                    passed_students = []
                    failed_students = []

                    for student in students:
                      failed = False
                      for subject in student.enrolled_subjects:
                            if subject.grade in ["Z", "F"]:
                              failed = True
                              break
                      if failed:
                          failed_students.append(student)
                      else:
                          passed_students.append(student)

                    print("\nPassed Students:")
                    for student in passed_students:
                        print(f"- Name: {student.first_name} {student.last_name}, Email: {student.email}, ID: {student.id}")

                    print("\nFailed Students:")
                    for student in failed_students:
                        print(f"- Name: {student.first_name} {student.last_name}, Email: {student.email}, ID: {student.id}")

                # remove a student
                case 'r':
                    email = input("Enter student email to remove: ")
                    found = False
                    for i, student in enumerate(students):
                        if student.email == email:
                            students.pop(i)
                            found = True
                            print("Student removed!")
                            break
                    if not found:
                        print("Student not found!")

                # clear all student data
                case 'c':
                    confirmation = input("Are you sure you want to clear all student data? (y/n): ")
                    if confirmation.lower() == "y":
                        students.clear()
                        print("All student data cleared!")
                    else:
                        print("Data clearing canceled.")

                #exit admin system, return to main menu
                case 'x':
                    print("Exiting admin menu")
                    return
        
                # catch any invalid input
                case _:
                    print("Invalid input, please try again.")


  def main(self):
      
      database = Database()
      students = database.load_students()

      while True:
        print("\nCLIUniApp - University Enrolment System")
        print("(S) Enter Student System")
        print("(A) Enter Admin System")
        print("(X) Exit")
        choice = input("Enter your choice: ").lower()
        
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
            print("Exiting CLIUniApp!")
            sys.exit()
          
          case _:
            print("Invalid choice!")
            
   



if __name__ == "__main__":
  app = UniAppSystem()
  app.main()