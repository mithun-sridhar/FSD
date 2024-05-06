def show_all_students(self):
        all_students_window = tk.Toplevel(self.root)
        all_students_window.title("All Students")

        tk.Label(all_students_window, text="All Students", font=("Arial", 16)).pack(pady=10)

        for student in self.students:
            student_info = f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Email: {student.email}"
            tk.Label(all_students_window, text=student_info).pack(pady=5)

