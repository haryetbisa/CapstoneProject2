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

def get_students_by_teacher_and_section(teacher_id: str, section: str):
    """Retrieves all students associated with the logged-in teacher filtered by grade/section."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students 
            WHERE teacher_id = ? AND grade_section = ?
            ORDER BY last_name ASC, first_name ASC
        """, (teacher_id, section))
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

def get_student_activity_logs(student_id: str):
    """Retrieves all activity and score logs for a specific student."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # FIXED: Changed 'timestamp' to 'completed_at' to match connection.py schema
        cursor.execute("""
            SELECT module_name, target_word, score, speech_accuracy, attempts, completed_at 
            FROM activity_logs 
            WHERE student_id = ? 
            ORDER BY completed_at DESC
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_module_progress_percentage(student_id: str, module_name: str, total_module_items: int = 10):
    """Calculates the completion percentage for a specific module based on unique completed targets."""
    if not student_id:
        return 0
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT target_word) as completed_count
            FROM activity_logs 
            WHERE student_id = ? AND module_name = ? AND target_word IS NOT NULL
        """, (student_id, module_name))
        result = cursor.fetchone()
        
        completed = result['completed_count'] if result else 0
        
        if total_module_items <= 0:
            return 0
            
        percentage = int(min(100, (completed / total_module_items) * 100))
        return percentage

def clear_local_teachers():
    """Deletes all local teacher accounts and clears the sync queue for fresh testing."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers")
        cursor.execute("DELETE FROM sync_queue WHERE table_name = 'teachers'")
        conn.commit()
        print("--> All local teacher accounts and sync queue entries have been cleared.")

def clear_local_students():
    """Deletes all local students and clears their sync queue entries."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM sync_queue WHERE table_name = 'students'")
        conn.commit()
        print("--> All local students and sync queue entries have been cleared.")

def clear_local_activity_logs():
    """Deletes all activity logs and clears their sync queue entries."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activity_logs")
        cursor.execute("DELETE FROM sync_queue WHERE table_name = 'activity_logs'")
        conn.commit()
        print("--> All local activity logs and sync queue entries have been cleared.")