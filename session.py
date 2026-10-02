# session.py
import json
import os

SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "active_session.json")


class AppSession:
    """Global state manager for tracking active teacher and student sessions with file persistence."""

    _active_teacher_id = None
    _active_teacher_name = "Walang Guro"
    _active_student_id = None
    _active_student_name = "Walang Nakapili"

    # --- TEACHER SESSION & PERSISTENCE ---
    @classmethod
    def set_teacher(cls, teacher_id: str, full_name: str, remember: bool = True):
        cls._active_teacher_id = teacher_id
        cls._active_teacher_name = full_name

        if remember:
            cls.save_session_to_file()

    @classmethod
    def get_teacher_id(cls) -> str:
        return cls._active_teacher_id

    @classmethod
    def get_teacher_name(cls) -> str:
        return cls._active_teacher_name

    @classmethod
    def is_teacher_logged_in(cls) -> bool:
        return cls._active_teacher_id is not None

    # --- STUDENT SESSION ---
    @classmethod
    def set_student(cls, student_id: str, full_name: str = ""):
        cls._active_student_id = student_id
        cls._active_student_name = full_name

    @classmethod
    def get_student_id(cls) -> str:
        return cls._active_student_id

    @classmethod
    def get_student_name(cls) -> str:
        return cls._active_student_name

    @classmethod
    def has_active_student(cls) -> bool:
        return cls._active_student_id is not None

    # Aliases to support dashboard dropdown calls safely
    @classmethod
    def set_active_student_id(cls, student_id):
        cls._active_student_id = student_id

    @classmethod
    def get_active_student_id(cls):
        return cls._active_student_id

    # --- FILE PERSISTENCE HELPERS ---
    @classmethod
    def save_session_to_file(cls):
        """Saves current teacher session to JSON file."""
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        data = {
            "teacher_id": cls._active_teacher_id,
            "teacher_name": cls._active_teacher_name,
        }
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @classmethod
    def load_saved_session(cls) -> bool:
        """Loads saved session from JSON on app startup. Returns True if logged in."""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("teacher_id"):
                        cls._active_teacher_id = data["teacher_id"]
                        cls._active_teacher_name = data.get("teacher_name", "Guro")
                        print(f"--> Auto-logged in teacher: {cls._active_teacher_name}")
                        return True
            except Exception as e:
                print(f"--> Failed to load saved session: {e}")
        return False

    # --- CLEAR SESSIONS ---
    @classmethod
    def clear_student(cls):
        cls._active_student_id = None
        cls._active_student_name = "Walang Nakapili"

    @classmethod
    def clear_all(cls):
        cls._active_teacher_id = None
        cls._active_teacher_name = "Walang Guro"
        cls.clear_student()

        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception as e:
                print(f"--> Error removing session file: {e}")