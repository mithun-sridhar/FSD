import random
import re
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
    return email.endswith("@university.com") and ("@" in email) and ("." in email)

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
import json

def load_students():
  try:
    with open("students.data", "r") as file:
      data = json.load(file)
      students = [Student(d["name"], d["email"], ["password"]) for d in data]
      for student in students:
        student.enrolled_subjects = [Subject() for _ in range(len(["enrolled_subjects"]))]
        for i, subject in enumerate(["enrolled_subjects"]):
          student.enrolled_subjects[i].mark = subject["mark"]
          student.enrolled_subjects[i].grade = subject["grade"]
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

def student_menu(student):
  while True:
    print("\nStudent Menu:")
    print("1. Enrol into a subject")
    print("2. Remove a subject from enrolment")
    print("3. Show current enrolment")
    print("4. Change password")
    print("5. Logout")
    choice = input("Enter your choice: ")

    if choice == "1":
      if len(student.enrolled_subjects) < 4:
        student.enrolled_subjects.append(Subject())
        print("Enrolled successfully!")
      else:
        print("Maximum enrolment reached (4 subjects)")
    elif choice == "2":
      if student.enrolled_subjects:
        student.enrolled_subjects.pop()
        print("Subject removed!")
      else:
        print("No subjects enrolled!")
    elif choice == "3":
      if student.enrolled_subjects:
        print("\nEnrolled Subjects:")
        for i, subject in enumerate(student.enrolled_subjects):
          print(f"{i+1}. Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
      else:
        print("No subjects enrolled!")
    elif choice == "4":
      new_password = input("Enter new password: ")
      if student.is_valid_password(new_password):
        student.password = new_password
        print("Password changed successfully!")
      else:
        print("Invalid password format! Please try again.")
    elif choice == "5":
      print("Logged out!")
      return
    else:
      print("Invalid choice!")

def admin_menu(students):
  while True:
    print("\nAdmin Menu:")
    print("1. View all students")
    print("2. Organize students by grade")
    print("3. View students by PASS/FAIL category")
    print("4. Remove a student")
    print("5. Clear all student data")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
      print("\nAll Students:")
      for student in students:
        print(f"Name: {student.name}, Email: {student.email}, ID: {student.id}")
    elif choice == "2":
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
    elif choice == "3":
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
    elif choice == "4":
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
    elif choice == "5":
      confirmation = input("Are you sure you want to clear all student data? (y/n): ")
      if confirmation.lower() == "y":
        students.clear()
        print("All student data cleared!")
      else:
        print("Data clearing canceled.")
    elif choice == "6":
      print("Exiting admin menu!")
      return
    else:
      print("Invalid choice!")

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
    print("1. Login as Student")
    print("2. Login as Admin")
    print("3. Register as Student")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
      student = student_login(students)
      if student:
        student_menu(student)
        save_students(students)
    elif choice == "2":
      admin_menu(students)
      save_students(students)
    elif choice == "3":
      new_student = register_student()
      if new_student:
        students.append(new_student)
        save_students(students)
        print("Registration successful! Please login to proceed.")
    elif choice == "4":
      print("Exiting CLIUniApp!")
      break
    else:
      print("Invalid choice!")

if __name__ == "__main__":
  main()
