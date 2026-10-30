# reset_db.py

import os
from Database.connection import get_db_connection
from Database.queries import (
    clear_local_teachers, 
    clear_local_students, 
    clear_local_activity_logs
)

SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "active_session.json")

def clear_sync_queue():
    """Wipes all remaining entries from the sync queue."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sync_queue")
        conn.commit()
        print("--> Sync queue completely cleared.")

if __name__ == "__main__":
    print("--> Initializing local database reset...")
    clear_local_teachers()
    clear_local_students()
    clear_local_activity_logs()
    clear_sync_queue()  

    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
            print("--> Active session file cleared.")
        except Exception as e:
            print(f"--> Error removing session file: {e}")

    print("--> Local database reset complete! You can now run your app for fresh testing.")