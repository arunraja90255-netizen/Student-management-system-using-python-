import json
import os 
from datetime import datetime

class Student:
    """Student class to store student information"""
    def __init__(self, student_id, name, dob, gender, email, phone, address, course, year, gpa):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.course = course
        self.year = year
        self.gpa = gpa
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "course": self.course,
            "year": self.year,
            "gpa": self.gpa,
            "created_date": self.created_date
        }
    
    def display(self):
        """Display student information"""
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Date of Birth: {self.dob}")
        print(f"Gender: {self.gender}") 
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Address: {self.address}")
        print(f"Course: {self.course}")
        print(f"Year: {self.year}")
        print(f"GPA: {self.gpa}")


class StudentManager:
    """Main class to manage student records"""
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()
    
    def load_students(self):
        """Load students from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    for item in data:
                        student_obj = Student(
                            item["student_id"],
                            item["name"],
                            item["dob"],
                            item["gender"],
                            item["email"],
                            item["phone"],
                            item["address"],
                            item["course"],
                            item["year"],
                            item["gpa"]
                        )
                        self.students.append(student_obj)
                print(f"✓ Loaded {len(self.students)} students")
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_students(self):
        """Save students to JSON file"""
        try:
            data = [student.to_dict() for student in self.students]
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def generate_student_id(self):
        """Generate unique student ID"""
        if not self.students:
            return "S001"
        numbers = []
        for student in self.students:
            try:
                numbers.append(int(student.student_id[1:]))
            except (ValueError, IndexError):
                continue
        if numbers:
            new_num = max(numbers) + 1
        else:
            new_num = 1
        return f"S{new_num:03d}"
    
    def add_student(self, name, dob, gender, email, phone, address, course, year, gpa):
        """Add a new student""" 
        if not name or not name.strip():
            print("Error: Name cannot be empty.")
            return False
        if not dob or not dob.strip():
            print("Error: Date of Birth cannot be empty.")
            return False
        if not gender or not gender.strip():
            print("Error: Gender cannot be empty.")
            return False    
        if not email or not email.strip():
            print("Error: Email cannot be empty.")
            return False            
        if not phone or not phone.strip():
            print("Error: Phone cannot be empty.")
            return False    
        if not address or not address.strip():
            print("Error: Address cannot be empty.")
            return False
        if not course or not course.strip():
            print("Error: Course cannot be empty.")
            return False
        if not year:
            print("Error: Year cannot be empty.")
            return False
        if not gpa:
            print("Error: GPA cannot be empty.")
            return False
        
        
        for student in self.students:
            if student.email == email:
                print("Error: Email already exists!")
                return False
        
        student_id = self.generate_student_id()
        new_student = Student(
            student_id, 
            name.strip(), 
            dob.strip(), 
            gender.strip(), 
            email.strip(), 
            phone.strip(), 
            address.strip(), 
            course.strip(), 
            year, 
            gpa
        )
        self.students.append(new_student)
        if self.save_students():
            print(f"✓ Student added successfully with ID: {student_id}")
            return True
        else:
            print("Error adding student.")
            return False
    
    def get_all_students(self):
        """Return list of all students"""
        return self.students
    
    def find_student_by_id(self, student_id):
        """Find student by ID"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def search_students_by_name(self, name):
        """Search students by name"""
        results = []
        for student in self.students:
            if name.lower() in student.name.lower():
                results.append(student)
        return results
    
    def update_student(self, student_id, name=None, dob=None, gender=None, email=None, 
                       phone=None, address=None, course=None, year=None, gpa=None):
        """Update student information"""
        student = self.find_student_by_id(student_id)
        if not student:
            print("Student not found.")
            return False
        
        
        if name and name.strip():
            student.name = name.strip()
        if dob and dob.strip():
            student.dob = dob.strip()
        if gender and gender.strip():
            student.gender = gender.strip()
        if email and email.strip():
            # Check if email already exists for another student
            for s in self.students:
                if s.email == email and s.student_id != student_id:
                    print("Error: Email already exists!")
                    return False
            student.email = email.strip()
        if phone and phone.strip():
            student.phone = phone.strip()
        if address and address.strip():
            student.address = address.strip()
        if course and course.strip():
            student.course = course.strip()
        if year:
            student.year = year
        if gpa:
            student.gpa = gpa
        
        if self.save_students():
            print("✓ Student updated successfully.")
            return True
        else:
            print("Error updating student.")
            return False
    
    def delete_student(self, student_id):
        """Delete student by ID"""
        student = self.find_student_by_id(student_id)
        if not student:
            print("Student not found.")
            return False
        
        self.students.remove(student)
        if self.save_students():
            print("✓ Student deleted successfully.")
            return True
        else:
            print("Error deleting student.")
            return False
    
    def view_all_students(self):
        """Display all students"""
        if not self.students:
            print("\nNo students found in the database!")
            return
        
        print("\n" + "="*60)
        print(f"ALL STUDENTS ({len(self.students)} records)")
        print("="*60)
        for i, student in enumerate(self.students, 1):
            print(f"\n{i}. {student.name} (ID: {student.student_id})")
            print(f"   DOB: {student.dob} \n   Gender: {student.gender}")
            print(f"   Course: {student.course} \n   Year: {student.year} \n   GPA: {student.gpa}")
            print(f"   Email: {student.email} \n   Phone: {student.phone}")
            print(f"   Address: {student.address}")
    
    def view_statistics(self):
        """Get and display statistics about students"""
        stats = self.get_statistics()
        if stats:
            print(f"\nTotal Students: {stats['total_students']}")
            print(f"Average GPA: {stats['average_gpa']:.2f}")
            print("\nCourse Distribution:")
            for course, count in stats['course_distribution'].items():
                print(f"  {course}: {count} student(s)")
    
    def get_statistics(self):
        """Get statistics about students"""
        total_students = len(self.students)
        if total_students == 0:
            print("No students found.")
            return None
        
        average_gpa = sum(float(student.gpa) for student in self.students) / total_students
        
        courses = {}
        for student in self.students:
            courses[student.course] = courses.get(student.course, 0) + 1
        
        return {
            "total_students": total_students,
            "average_gpa": average_gpa,
            "course_distribution": courses
        }
    
    
    
    
    def interactive_menu(self):
        """Interactive menu for user input"""
        while True:
            print("\n" + "="*60)
            print("STUDENT MANAGEMENT SYSTEM")
            print("="*60)
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Students by Name")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. View Statistics")
           # print("7. Export to CSV")
            #print("8. Import from CSV")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                print("\n--- Add New Student ---")
                name = input("Name: ").strip()
                dob = input("Date of Birth (YYYY-MM-DD): ").strip()
                # Validate date format
                try:
                    datetime.strptime(dob, "%Y-%m-%d")
                except ValueError:
                    print("Error: Invalid date format. Please use YYYY-MM-DD.")
                    continue
                gender = input("Gender (Male/Female/Other): ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                address = input("Address: ").strip()
                course = input("Course: ").strip()
                try:
                    year = int(input("Year (1-4): ").strip())
                except ValueError:
                    print("Error: Year must be a number.")
                    continue
                try:
                    gpa = float(input("GPA (0-4.0): ").strip())
                except ValueError:
                    print("Error: GPA must be a number.")
                    continue
                
                self.add_student(name, dob, gender, email, phone, address, course, year, gpa)
            
            elif choice == "2":
                self.view_all_students()
            
            elif choice == "3":
                print("\n--- Search Students ---")
                name = input("Enter student name to search: ").strip()
                results = self.search_students_by_name(name)
                if results:
                    print(f"\nFound {len(results)} student(s):")
                    for student in results:
                        student.display()
                else:
                    print("No students found.")
            
            elif choice == "4":
                print("\n--- Update Student ---")
                student_id = input("Enter student ID to update: ").strip()
                student = self.find_student_by_id(student_id)
                if not student:
                    print("Student not found!")
                    continue
                
                print("\nEnter new details (press Enter to keep current value):")
                name = input(f"Name ({student.name}): ").strip()
                dob = input(f"Date of Birth ({student.dob}): ").strip()
                gender = input(f"Gender ({student.gender}): ").strip()
                email = input(f"Email ({student.email}): ").strip()
                phone = input(f"Phone ({student.phone}): ").strip()
                address = input(f"Address ({student.address}): ").strip()
                course = input(f"Course ({student.course}): ").strip()
                year_input = input(f"Year ({student.year}): ").strip()
                gpa_input = input(f"GPA ({student.gpa}): ").strip()
                
                # Prepare updates
                updates = {}
                if name: updates['name'] = name
                if dob: updates['dob'] = dob
                if gender: updates['gender'] = gender
                if email: updates['email'] = email
                if phone: updates['phone'] = phone
                if address: updates['address'] = address
                if course: updates['course'] = course
                if year_input: updates['year'] = int(year_input)
                if gpa_input: updates['gpa'] = float(gpa_input)
                
                if updates:
                    self.update_student(student_id, **updates)
                else:
                    print("No updates provided.")
            
            elif choice == "5":
                print("\n--- Delete Student ---")
                student_id = input("Enter student ID to delete: ").strip()
                confirm = input(f"Are you sure you want to delete student {student_id}? (y/n): ")
                if confirm.lower() == 'y':
                    self.delete_student(student_id)
            
            elif choice == "6":
                print("\n--- Statistics ---")
                self.view_statistics()
            
            #elif choice == "7":
             #   print("\n--- Export to CSV ---")
              #  filename = input("Enter filename (default: students.csv): ").strip()
               # if not filename:
                #    filename = "students.csv"
                #if not filename.endswith('.csv'):
                 #   filename += '.csv'
                #self.export_students_to_csv(filename)
            
#            elif choice == "8":
 #               print("\n--- Import from CSV ---")
  #              filename = input("Enter filename (default: students.csv): ").strip()
   #             if not filename:
    #                filename = "students.csv"
     #           self.import_students_from_csv(filename)
            
            elif choice == "7":
                print("\nThank you for using Student Management System!")
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("="*60)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    print("Select mode:")
    print("1. Interactive Menu")
    
    
    mode = input("\nEnter your choice : ").strip()
    
    if mode == '1':
        manager = StudentManager()
        manager.interactive_menu()
    #elif mode == '2':
     
     #   manager = StudentManager("test_students.json")
      #  manager.test_operations()
    else:
        print("Invalid choice. Exiting.")