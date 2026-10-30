# helpers/activity_helper.py

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Database.queries import log_activity
from session import AppSession


def save_student_performance(module_name: str, score: float, target_word: str = None, speech_accuracy: float = None, attempts: int = 1):
    # Fixed to use get_active_student_id() so it matches grade1_dashboard and kinder_dashboard session state
    student_id = AppSession.get_active_student_id()

    if not student_id:
        print("--> Warning: No active student selected in session. Score not saved.")
        return None

    try:
        log_id = log_activity(
            student_id=student_id,
            module_name=module_name,
            score=score,
            target_word=target_word,
            speech_accuracy=speech_accuracy,
            attempts=attempts
        )
        print(f"--> Saved score for student {student_id} | Module: {module_name} | Score: {score}")
        return log_id
    except Exception as e:
        print(f"--> Failed to log activity: {e}")
        return None