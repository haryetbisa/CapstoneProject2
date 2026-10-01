# database/queries.py

import uuid
import bcrypt
from Database.connection import get_db_connection

def create_teacher_account(full_name: str, email: str, raw_password: str, school_name="Paharang Elementary School", section_name="Kindergarten - Paharang"):
    """Hashes password and saves a new teacher record locally and in the sync queue."""
    teacher_id = str(uuid.uuid4())
    hashed_pw = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (teacher_id, full_name, email, password_hash, school_name, section_name, is_synced)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (teacher_id, full_name, email.lower().strip(), hashed_pw, school_name, section_name))
        
        cursor.execute("""
            INSERT INTO sync_queue (table_name, record_id, action)
            VALUES ('teachers', ?, 'INSERT')
        """, (teacher_id,))
        
        conn.commit()
    return teacher_id

def verify_teacher_login(email: str, raw_password: str):
    """Checks teacher credentials against local SQLite database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE email = ?", (email.lower().strip(),))
        teacher = cursor.fetchone()
        
        if teacher and bcrypt.checkpw(raw_password.encode('utf-8'), teacher['password_hash'].encode('utf-8')):
            return dict(teacher)
    return None

# --- STUDENT ROSTER MANAGEMENT ---

def add_student(teacher_id: str, first_name: str, last_name: str, section="Kindergarten - Paharang"):
    """Adds a pupil to the active teacher's local roster."""
    student_id = str(uuid.uuid4())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (student_id, teacher_id, first_name, last_name, grade_section, is_synced)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (student_id, teacher_id, first_name.strip(), last_name.strip(), section))
        
        cursor.execute("""
            INSERT INTO sync_queue (table_name, record_id, action)
            VALUES ('students', ?, 'INSERT')
        """, (student_id,))
        
        conn.commit()
    return student_id

def get_students_by_teacher(teacher_id: str):
    """Retrieves all students associated with the logged-in teacher."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students 
            WHERE teacher_id = ? 
            ORDER BY last_name ASC, first_name ASC
        """, (teacher_id,))
        return [dict(row) for row in cursor.fetchall()]

# --- ACTIVITY SCORE LOGGING ---

def log_activity(student_id: str, module_name: str, score: float, target_word=None, speech_accuracy=None, attempts=1):
    """Saves practice module or speech recognition performance locally."""
    log_id = str(uuid.uuid4())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activity_logs (log_id, student_id, module_name, target_word, score, speech_accuracy, attempts, is_synced)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (log_id, student_id, module_name, target_word, score, speech_accuracy, attempts))
        
        cursor.execute("""
            INSERT INTO sync_queue (table_name, record_id, action)
            VALUES ('activity_logs', ?, 'INSERT')
        """, (log_id,))
        
        conn.commit()
    return log_id

# --- LOCAL CLEANUP UTILITY ---

def clear_local_teachers():
    """Deletes all local teacher accounts and clears the sync queue for fresh testing."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers")
        cursor.execute("DELETE FROM sync_queue WHERE table_name = 'teachers'")
        conn.commit()
        print("--> All local teacher accounts and sync queue entries have been cleared.")