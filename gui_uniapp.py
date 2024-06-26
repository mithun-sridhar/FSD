import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import re
import json


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

    def is_valid_password(self, password):
        return bool(re.match(r"^[A-Z].{5,}[0-9]{3}$", password))

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
                messagebox.showerror("Error", "Email format incorrect. Please ensure it is in the following format: firstname.lastname@university.com")
            if not self.is_valid_password(password):
                messagebox.showerror("Error", "Password does not meet requirements. Please ensure it has: 6 characters; starts with an uppercase letter, and ends with three digits.")
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

    def register_student(self, first_name, last_name, email, password):
        new_student = Student(None, None, None, None)  # Create empty student object
        if new_student.register(first_name, last_name, email, password):
            return new_student
        else:
            return False

    def save_students(self, students):
        data = [{"id": s.id, "first_name": s.first_name, "last_name": s.last_name, "email": s.email, "password": s.password,
                 "enrolled_subjects": [{"subject_id": subj.id, "mark": subj.mark, "grade": subj.grade} for subj in s.enrolled_subjects]} for s in students]
        with open("students.data", "w") as file:
            json.dump(data, file)


class UniAppSystem:
    def __init__(self, root):
        self.root = root
        self.database = Database()
        self.students = self.database.load_students()
        self.logged_in_student = None
        self.main_menu()

    def student_login(self, email, password):
        # Iterate through each student's data in the file
        for student in self.students:
            # Check if the email and password match
            if student.email == email and student.password == password:
                return student  # Credentials match
        return None  # No match found

    def login_case(self):
        email = simpledialog.askstring("Login", "Enter email:")
        password = simpledialog.askstring("Login", "Enter password:", show='*')
        if email and password:
            student = self.student_login(email.lower(), password)
            if student:
                self.logged_in_student = student  # Store the logged-in student
                self.student_course_menu()
                self.database.save_students(self.students)
                return self.logged_in_student
            else:
                messagebox.showerror("Error", "Login unsuccessful, please try again.")

    def register_student_window(self):
        register_student_window = tk.Toplevel(self.root)
        register_student_window.title("Registration Page")

        # Create labels and entry fields for user input
        label_first_name = tk.Label(register_student_window, text="First Name:")
        label_first_name.grid(row=0, column=0, sticky="e")
        entry_first_name = tk.Entry(register_student_window)
        entry_first_name.grid(row=0, column=1)

        label_last_name = tk.Label(register_student_window, text="Last Name:")
        label_last_name.grid(row=1, column=0, sticky="e")
        entry_last_name = tk.Entry(register_student_window)
        entry_last_name.grid(row=1, column=1)

        label_email = tk.Label(register_student_window, text="Email:")
        label_email.grid(row=2, column=0, sticky="e")
        entry_email = tk.Entry(register_student_window)
        entry_email.grid(row=2, column=1)

        label_password = tk.Label(register_student_window, text="Password:")
        label_password.grid(row=3, column=0, sticky="e")
        entry_password = tk.Entry(register_student_window, show="*")
        entry_password.grid(row=3, column=1)

        def register_student():
            # Retrieve values from entry fields
            first_name = entry_first_name.get().capitalize()
            last_name = entry_last_name.get().capitalize()
            email = entry_email.get().lower()
            password = entry_password.get().strip()

            # Check if the student's email is already in the database before adding them in
            students_data = self.database.load_students()
            new_student_email = email
            email_exists = any(student.email == new_student_email for student in students_data)

            if not email_exists:
                # Register the student
                new_student = self.database.register_student(first_name, last_name, email, password)
                if new_student:
                    self.students.append(new_student)
                    self.database.save_students(self.students)
                    messagebox.showinfo("Success", "Registration successful! Please login to proceed.")
                    register_student_window.destroy()
                else:
                    messagebox.showerror("Error", "Registration unsuccessful. Please check your input.")
            else:
                messagebox.showerror("Error", "Student already exists.")

        # Button to trigger registration
        register_button = tk.Button(register_student_window, text="Register", command=register_student)
        register_button.grid(row=4, columnspan=2)

    def exit_menu(self):
        if hasattr(self, 'student_menu_window') and self.student_menu_window.winfo_exists():
            self.student_menu_window.destroy()


    def main_menu(self):
        self.root.title("GUIUniApp - University Enrolment System")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Modern style for buttons
        button_font = ("Arial", 12, "bold")

        tk.Label(self.root, text="Welcome to UniApp", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Student System", command=self.student_menu, font=button_font, bg="#ccd5ae", fg="white").pack(pady=10)
        tk.Button(self.root, text="Admin System", command=self.admin_menu, font=button_font, bg="#ccd5ae", fg="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=button_font, bg="#ccd5ae", fg="white").pack(pady=10)


    def exit_menu(self):
        self.root.destroy()
        self.root = tk.Tk()
        app = UniAppSystem(self.root)
        self.root.mainloop()


    def student_menu(self):
        student_menu_window = tk.Toplevel(self.root)
        student_menu_window.title("Student Menu")
        student_menu_window.geometry("600x400")
        student_menu_window.configure(bg="#f0f0f0")  # Set background color

        # Modern style for labels and buttons
        label_font = ("Arial", 16)
        button_font = ("Arial", 12, "bold")

        tk.Label(student_menu_window, text="Student Menu", font=label_font, bg="#f0f0f0").pack(pady=20)

        # Login button
        login_button = tk.Button(student_menu_window, text="Login as student", command=self.login_case, font=button_font, bg="#4CAF50", fg="white")
        login_button.config(width=20)
        login_button.pack(pady=10)

        # Register button
        register_button = tk.Button(student_menu_window, text="Register as student", command=self.register_student_window, font=button_font, bg="#008CBA", fg="white")
        register_button.config(width=20)
        register_button.pack(pady=10)

        # Exit button
        exit_button = tk.Button(student_menu_window, text="Exit", command=self.exit_menu, font=button_font, bg="#f44336", fg="white")
        exit_button.config(width=20)
        exit_button.pack(pady=10)


    def enroll_subject(self, student):
        if self.logged_in_student and len(self.student.enrolled_subjects) < 4:
            subject_enrolled = Subject()
            student.subject_enrolled.append(subject_enrolled)
            num_enrolled = len(self.student.enrolled_subjects)
            messagebox.showinfo("Enrolled successfully", f"Enrolled successfully into subject {subject_enrolled.id}. You are now enrolled in {num_enrolled} out of 4 subjects.")
            Database.save_students(students=self.students)
        elif not self.logged_in_student:
            messagebox.showerror("Error", "No student logged in.")
        else:
            messagebox.showinfo("Maximum enrolment reached", "Maximum enrolment reached (4 subjects).")


    def remove_subject(self, student):
        if student.enrolled_subjects:
            subject_options = [subject.id for subject in student.enrolled_subjects]
            selected_subject = simpledialog.askstring("Remove Subject", f"Select subject to remove: {subject_options}")
            if selected_subject in subject_options:
                student.enrolled_subjects = [subject for subject in student.enrolled_subjects if subject.id == selected_subject]
                selected_subject = student.enrolled_subjects.pop()
                messagebox.showinfo("Subject Removed", f"Subject {selected_subject} successfully removed.")
            else:
                messagebox.showerror("Error", "Invalid subject selection.")
        else:
            messagebox.showinfo("No subjects enrolled!", "No subjects enrolled!")

    def show_enrolment(self, student):
        if student.enrolled_subjects:
            enrolment_info = "\nEnrolled Subjects:\n"
            for i, subject in enumerate(student.enrolled_subjects):
                enrolment_info += f"{i+1}. Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}\n"
            messagebox.showinfo("Current Enrolment", enrolment_info)
        else:
            messagebox.showinfo("No subjects enrolled!", "No subjects enrolled!")

    def change_password(self, student):
        new_password = simpledialog.askstring("Change Password", "Enter new password:")
        confirm_password = simpledialog.askstring("Change Password", "Confirm password:")
        if new_password != confirm_password:
            messagebox.showinfo("Passwords do not match, please try again.")
            return
        if student.is_valid_password(new_password):
            student.password = new_password
            centered_message = "\n".join(["" * 10 + line for line in "Password changed successfully!".split("\n")])
            messagebox.showinfo("Success", centered_message)
           
        else:
            invalid_message = "Invalid password format! Please try again."
            note_message = "Note: Password must have at least 6 characters total, beginning with an uppercase, and last three characters must be digits."
            centered_invalid_message = "\n".join(["" * 10 + line for line in invalid_message.split("\n")])
            centered_note_message = "\n".join(["" * 10 + line for line in note_message.split("\n")])
            messagebox.showinfo("Error", centered_invalid_message)
            messagebox.showinfo("Note", centered_note_message)

    #def logout(self):
     #   parent_window = self.root.master if self.root.master else self.root
      #  self.root.destroy()  # Hide the current window


    def logout(self):
        self.logged_in_student = None
        self.root.destroy()
        self.root = tk.Tk()
        app = UniAppSystem(self.root)
        self.root.mainloop()

    def student_course_menu(self):
        student_course_menu_window = tk.Toplevel(self.root)
        student_course_menu_window.title("Student Menu")
        student_course_menu_window.geometry("400x400")
        student_course_menu_window.configure(bg="#f0f0f0")

        button_style = {"font": ("Arial", 12,  "bold"), "bg": "#ccd5ae", "fg": "white"}
        label_style = {"font": ("Arial", 16), "bg": "#f0f0f0", "fg": "black"}

        tk.Label(student_course_menu_window, text="Student Course Menu", **label_style).pack(pady=5)
        tk.Button(student_course_menu_window, text="Enrol into a subject", command=lambda: self.enroll_subject(self.logged_in_student), **button_style).pack(pady=5)
        tk.Button(student_course_menu_window, text="Remove a subject from enrolment", command=lambda: self.remove_subject(self.logged_in_student), **button_style).pack(pady=5)
        tk.Button(student_course_menu_window, text="Show current enrolment", command=lambda: self.show_enrolment(self.logged_in_student), **button_style).pack(pady=5)
        tk.Button(student_course_menu_window, text="Change password", command=lambda: self.change_password(self.logged_in_student), **button_style).pack(pady=5)
        tk.Button(student_course_menu_window, text="Logout", command=self.logout, **button_style).pack(pady=5)

    def admin_menu(self):
        admin_menu_window = tk.Toplevel(self.root)
        admin_menu_window.title("Admin Menu")
        admin_menu_window.geometry("400x400")
        admin_menu_window.configure(bg="#f0f0f0")


        button_style = {"font": ("Arial", 12,  "bold"), "bg": "#ccd5ae", "fg": "white"}
        

        tk.Button(admin_menu_window, text="Show all students", command=self.show_all_students, **button_style).pack(pady=5)
        tk.Button(admin_menu_window, text="Group students by grade", command=self.group_students_by_grade, **button_style).pack(pady=5)
        tk.Button(admin_menu_window, text="Partition students by PASS/FAIL category", command=self.partition_students, **button_style).pack(pady=5)
        tk.Button(admin_menu_window, text="Remove a student", command=self.remove_student, **button_style).pack(pady=5)
        tk.Button(admin_menu_window, text="Clear all student data", command=self.clear_students_window, **button_style).pack(pady=5)
        tk.Button(admin_menu_window, text="Exit", command=admin_menu_window.destroy, **button_style).pack(pady=5)

    def show_all_students(self):
        all_students_window = tk.Toplevel(self.root)
        all_students_window.title("All Students")

        tk.Label(all_students_window, text="All Students", font=("Arial", 16)).pack(pady=10)

        for student in self.students:
            student_info = f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Email: {student.email}"
            tk.Label(all_students_window, text=student_info).pack(pady=5)

    def group_students_by_grade(self):
        group_by_grade_window = tk.Toplevel(self.root)
        group_by_grade_window.title("Group Students by Grade")

        subjects_by_grade = {"HD": [], "D": [], "C": [], "P": [], "Z": []}

        # Group subjects by grade
        for student in self.students:
            for subject in student.enrolled_subjects:
                grade = subject.grade
                subjects_by_grade[grade].append((student, subject))

        # Display subjects grouped by grade
        for grade, subjects in subjects_by_grade.items():
            if subjects:
                tk.Label(group_by_grade_window, text=f"Subjects with grade {grade}:", font=("Arial", 12, "bold")).pack(pady=5)
                for student, subject in subjects:
                    student_info = f"Student: {student.first_name} {student.last_name}, Email: {student.email}, Subject: {subject.id}, Subject Mark: {subject.mark}"
                    tk.Label(group_by_grade_window, text=student_info).pack(pady=2)

    def partition_students(self):
        partition_window = tk.Toplevel(self.root)
        partition_window.title("Partition Students by PASS/FAIL Category")

        passed_students = []
        failed_students = []

        for student in self.students:
            total_marks = sum(subject.mark for subject in student.enrolled_subjects)
            average_score = total_marks / len(student.enrolled_subjects) if student.enrolled_subjects else 0

            if average_score >= 50:
                passed_students.append(student)
            else:
                failed_students.append(student)

        tk.Label(partition_window, text="Passed Students:", font=("Arial", 12, "bold")).pack(pady=5)
        for student in passed_students:
            total_marks = sum(subject.mark for subject in student.enrolled_subjects)
            average_score = total_marks / len(student.enrolled_subjects) if student.enrolled_subjects else 0
            student_info = f"ID: {student.id} {student.first_name} {student.last_name}, GPA: {average_score}"
            tk.Label(partition_window, text=student_info).pack(pady=2)

        tk.Label(partition_window, text="Failed Students:", font=("Arial", 12, "bold")).pack(pady=5)
        for student in failed_students:
            total_marks = sum(subject.mark for subject in student.enrolled_subjects)
            average_score = total_marks / len(student.enrolled_subjects) if student.enrolled_subjects else 0
            student_info = f"ID: {student.id} {student.first_name} {student.last_name}, GPA: {average_score}"
            tk.Label(partition_window, text=student_info).pack(pady=2)

    def remove_student(self):
        remove_student_window = tk.Toplevel(self.root)
        remove_student_window.title("Remove Student")

        tk.Label(remove_student_window, text="Enter student email to remove:", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(remove_student_window)
        email_entry.pack(pady=5)

        def remove():
            email = email_entry.get().strip()
            found = False
            for i, student in enumerate(self.students):
                if student.email == email:
                    self.students.pop(i)
                    found = True
                    

            if not found:
                messagebox.showinfo("Error", "Student not found!")

        tk.Button(remove_student_window, text="Remove", command=remove).pack(pady=5)

    def clear_students_window(self):

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to clear all student data?")
        if confirmation:
            try:
                with open("students.data", "w") as file:
                    json.dump([], file)
                messagebox.showinfo("Success", "All student data cleared!")
            except FileNotFoundError:
                messagebox.showerror("Error", "Unable to clear student data.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


root = tk.Tk()
app = UniAppSystem(root)
root.mainloop()

