# database/connection.py

import os
import sqlite3
from .database_security import encrypt_data, decrypt_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "basamatika.db")


def get_db_connection():
    """Returns a connection object configured for dictionary-style row access."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_local_database():
    """Initializes local SQLite tables for teachers, students, logs, and sync tracking."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Teachers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                school_name TEXT DEFAULT 'Paharang Elementary School',
                section_name TEXT DEFAULT 'Kindergarten - Paharang',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_synced INTEGER DEFAULT 0
            )
        """)

        # 2. Students Table (Names will be encrypted for privacy)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                teacher_id TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                grade_section TEXT DEFAULT 'Kindergarten - Paharang',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_synced INTEGER DEFAULT 0,
                FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
            )
        """)

        # 3. Activity Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                log_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                module_name TEXT NOT NULL,
                target_word TEXT,
                score REAL NOT NULL,
                speech_accuracy REAL,
                attempts INTEGER DEFAULT 1,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_synced INTEGER DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_queue (
                queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id TEXT NOT NULL,
                action TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


# --- SECURE HELPER FUNCTIONS FOR STUDENT RECORDS ---

def insert_secure_student(student_id, teacher_id, first_name, last_name, grade_section="Kindergarten - Paharang"):
    """Encrypts student first and last names before inserting them into the database."""
    encrypted_first = encrypt_data(first_name)
    encrypted_last = encrypt_data(last_name)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO students (student_id, teacher_id, first_name, last_name, grade_section)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, teacher_id, encrypted_first, encrypted_last, grade_section))
        conn.commit()


def fetch_all_secure_students():
    """Retrieves all students and automatically decrypts their names for UI display."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, teacher_id, first_name, last_name, grade_section, created_at FROM students")
        rows = cursor.fetchall()
        
        students_list = []
        for row in rows:
            students_list.append({
                "student_id": row["student_id"],
                "teacher_id": row["teacher_id"],
                "first_name": decrypt_data(row["first_name"]),
                "last_name": decrypt_data(row["last_name"]),
                "grade_section": row["grade_section"],
                "created_at": row["created_at"]
            })
        return students_list