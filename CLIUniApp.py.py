import random
import re
import json

class Student:
  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password
    self.id = self.generate_id()
    self.enrolled_subjects = []

  def generate_id(self):
    student_id = str(random.randint(1, 999999))
    return student_id.zfill(6)

  def is_valid_email(self, email):
    return bool(email.endswith("@university.com") and ("@" in email) and ("." in email))

  def is_valid_password(self, password):
    return bool(re.match( r"^[A-Z].{4,}[0-9]{3}$", password))

  def register(self, name, email, password):
    if self.is_valid_email(email) and self.is_valid_password(password):
      self.name = name
      self.email = email
      self.password = password
      self.id = self.generate_id()
      self.enrolled_subjects = []
      return True
    else:
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
    
def load_students():
    try:
        with open("students.data", "r") as file:
            data = json.load(file)
            students = []
            for d in data:
                student = Student(d["name"], d["email"], d["password"])
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

def save_students(students):
  data = [{"name": s.name, "email": s.email, "password": s.password, "enrolled_subjects": [{ "mark": subj.mark, "grade": subj.grade } for subj in s.enrolled_subjects]} for s in students]
  with open("students.data", "w") as file:
    json.dump(data, file)


def student_login(students):
  email = input("Enter email: ")
  password = input("Enter password: ")
  for student in students:
    if student.email == email and student.password == password:
      return student
  print("Invalid login credentials!")
  return None

            
def student_menu(students):
   while True:
        print("\nStudent Menu:")
        print("(l) Login as student")
        print("(r) Register as student")
        print("(x) Exit")
        choice = input("Enter your choice: ").lower()

        match choice:
           
          case 'l':
            student = student_login(students)
            if student:
              student_course_menu(student)
              save_students(students)
          
          case 'r':
            new_student = register_student()
            if new_student:
              students.append(new_student)
              save_students(students)
              print("Registration successful! Please login to proceed.")
          
          case 'x':
              print("Exiting Student Menu, returning to System menu.")
              main()
          
          case _:
              print("Invalid input, please try again.")
              return


def student_course_menu(student):
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
                print(f"Enrolled successfully into subject {subject_enrolled.id}")
            else:
                print("Maximum enrolment reached (4 subjects)")

        # remove subject
        case 'r':
            if student.enrolled_subjects:
                student.enrolled_subjects.pop()
                print("Subject removed!")
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
            new_password = input("Enter new password: ")
            if student.is_valid_password(new_password):
                student.password = new_password
                print("Password changed successfully!")
            else:
                print("Invalid password format! Please try again.")

        # exit system
        case 'x':
            print("Logged out!")
        case _:
            print("Invalid choice, please try again.")

      #system_menu()

   
def admin_menu(students):
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
                    print(f"Name: {student.name}, Email: {student.email}, ID: {student.id}")

            # group students by grade
            case 'g':
                graded_students = {}
                for student in students:
                    for subject in student.enrolled_subjects:
                        grade = subject.grade
                        if grade in graded_students:
                            graded_students[grade].append(student)
                        else:
                            graded_students[grade] = [student]

                for grade, students in graded_students.items():
                    print(f"\nGrade: {grade}")
                    for student in students:
                        print(f"- Name: {student.name}, Email: {student.email}, ID: {student.id}")

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
                    print(f"- Name: {student.name}, Email: {student.email}, ID: {student.id}")

                print("\nFailed Students:")
                for student in failed_students:
                    print(f"- Name: {student.name}, Email: {student.email}, ID: {student.id}")

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

def register_student():
  name = input("Enter your name: ")
  email = input("Enter your email: ")
  password = input("Enter your password: ")
  new_student = Student(None, None, None)  # Create empty student object
  if new_student.register(name, email, password):
    return new_student
  else:
    print("Registration failed! Please check your email and password format.")

def main():
  students = load_students()

  while True:
    print("\nCLIUniApp - University Enrolment System")
    print("(S) Enter Student System")
    print("(A) Enter Admin System")
    print("(X) Exit")
    choice = input("Enter your choice: ").lower()
    
    match choice:
       
      case 's':
        #student = student_login(students)
        #if student:
        student_menu(students)
        save_students(students)

      case 'a':
        admin_menu(students)
        save_students(students)

      case 'x':
        print("Exiting CLIUniApp!")
        break
      
      case _:
        print("Invalid choice!")

if __name__ == "__main__":
  main()