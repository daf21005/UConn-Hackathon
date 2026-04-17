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

    # 4. Course Weights Table (Added for the Gemini Syllabus Feature)
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