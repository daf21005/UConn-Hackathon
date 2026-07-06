import sqlite3
# will be communicating with SQLite to create a database file

# creating a connection to SQLite database
def get_connection():
    conn = sqlite3.connect("hackathon.db", check_same_thread=False)

    conn.row_factory = sqlite3.Row
    return conn

# initializes the tables if they dont exist already
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # students table
    # (id, name and blackboard id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blackboard_id TEXT UNIQUE NOT NULL
        )
    """)

    # course table
    # (course id, student id, course name, course credits, grade, connection to student)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            current_grade REAL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    # gpa history table
    # (gpa id, student id, semester, gpa, connection to student)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gpa_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            semester TEXT NOT NULL,
            gpa REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    # course Weights Table (Added for the Gemini Syllabus Feature)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            weight_percentage REAL NOT NULL,
            current_score REAL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    # save changes and close connection
    conn.commit()
    conn.close()

# WRITE into the db
def save_student(name, blackboard_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # INSERT INTO students table
    # use INSERT OR IGNORE so it doesn't crash if student already exists
    cursor.execute("""
        INSERT OR IGNORE INTO students (name, blackboard_id)
        VALUES (?, ?)
    """, (name, blackboard_id))
    
    conn.commit()
    conn.close()
    

def save_course(student_id, course_name, credits, current_grade):
    conn = get_connection()
    cursor = conn.cursor()
    
    # INSERT INTO courses table
    cursor.execute("""
        INSERT INTO courses (student_id, course_name, credits, current_grade)
        VALUES (?, ?, ?, ?)
        
    """, (student_id, course_name, credits, current_grade))
    
    conn.commit()
    conn.close()

def save_gpa_history(student_id, semester, gpa):
    conn = get_connection()
    cursor = conn.cursor()
    
    # INSERT INTO gpa_history table
    cursor.execute("""
        INSERT INTO gpa_history (student_id, semester, gpa)
        VALUES (?, ?, ?)
    """, (student_id, semester, gpa))
    
    conn.commit()
    conn.close()

def save_course_weights(course_id, category, weight_percentage, current_score):
    conn = get_connection()
    cursor = conn.cursor()
    
    # INSERT INTO course_weights table
    cursor.execute("""
        INSERT INTO course_weights (course_id, category, weight_percentage, current_score)
        VALUES (?, ?, ?, ?)
    """, (course_id, category, weight_percentage, current_score))
    
    conn.commit()
    conn.close()

# WIP
# READ from the db
def get_student(blackboard_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # SELECT from students WHERE blackboard_id matches
    cursor.execute("""
        SELECT * FROM students
        WHERE blackboard_id = ?
    """, (blackboard_id,))
    
    # fetchone() returns a single row
    row = cursor.fetchone()
    conn.close()
    return row


def get_courses(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # SELECT all courses WHERE student_id matches
    cursor.execute("""
        SELECT * FROM courses
        WHERE student_id = ?
    """, (student_id,))
    
    # fetchall() returns all matching rows as a list
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_gpa_history(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # SELECT all gpa records WHERE student_id matches
    cursor.execute("""
        SELECT * FROM gpa_history
        WHERE student_id = ?
        
    """, (student_id,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_course_weights(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # SELECT all weights WHERE course_id matches
    cursor.execute("""
        SELECT * FROM course_weights
        WHERE course_id = ?
    """, (course_id,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

''' Hint:
Inserting:
INSERT INTO table_name (column1, column2, column3)
VALUES (?, ?, ?)

Selecting:
SELECT * FROM table_name
WHERE column_name = ?
''' 