

from Database.connection import get_db_connection

def view_local_teachers():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id, full_name, email, school_name, is_synced FROM teachers")
        teachers = cursor.fetchall()
        
        if not teachers:
            print("--> No local teacher accounts found in the database.")
        else:
            print(f"--> Found {len(teachers)} local teacher account(s):")
            for t in teachers:
                print(dict(t))

if __name__ == "__main__":
    view_local_teachers()