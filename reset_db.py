# reset_db.py

from Database.queries import clear_local_teachers

if __name__ == "__main__":
    print("--> Initializing local database reset...")
    clear_local_teachers()
    print("--> Local database reset complete! You can now run your app for fresh testing.")