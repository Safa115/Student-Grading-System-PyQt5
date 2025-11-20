from models.database_manager import DatabaseManager

def fix_all_gpas():
    print("Starting GPA recalculation for all students...")
    
    db = DatabaseManager()
    conn = db.connect()
    cursor = conn.cursor()
    
    # 1. Get all students
    cursor.execute("SELECT student_id, name FROM Student")
    students = cursor.fetchall()
    
    count = 0
    for student in students:
        s_id = student[0]
        s_name = student[1]
        
        # 2. Recalculate GPA for each student
        # Passing 0 as dummy course_id since it's not needed for total calculation
        new_gpa = db.calculate_gpa(s_id, 0)
        
        print(f" {s_name}: GPA Updated to -> {new_gpa}")
        count += 1
        
    print(f"\n Successfully updated {count} students! You can now open the application.")

if __name__ == "__main__":
    fix_all_gpas()