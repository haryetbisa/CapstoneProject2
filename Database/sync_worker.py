import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtCore import QThread, Signal

try:
    from config import SUPABASE_URL, SUPABASE_KEY  # type: ignore
except ImportError:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

try:
    from supabase import create_client
except ImportError:
    create_client = None

from Database.connection import get_db_connection


class CloudSyncWorker(QThread):
    sync_status = Signal(str)

    def __init__(self, check_interval_seconds=15, parent=None):
        super().__init__(parent)
        self.check_interval = check_interval_seconds
        self._is_running = True

        if SUPABASE_URL and SUPABASE_KEY and create_client:
            try:
                self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                print(f"--> Failed to initialize Supabase client: {e}")
                self.supabase = None
        else:
            self.supabase = None

    def run(self):
        print("--> Cloud Sync Worker started...")
        while self._is_running:
            if self.supabase:
                self.process_sync_queue()
            time.sleep(self.check_interval)

    def stop(self):
        self._is_running = False
        self.wait()

    def process_sync_queue(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sync_queue ORDER BY queue_id ASC LIMIT 10")
                queue_items = [dict(row) for row in cursor.fetchall()]

                if not queue_items:
                    return

                print(f"--> Found {len(queue_items)} pending items in sync queue.")

                for item in queue_items:
                    success = self.upload_item_to_supabase(conn, item)
                    if not success:
                        break

        except Exception as e:
            print(f"--> Sync worker error: {e}")

    def upload_item_to_supabase(self, conn, item: dict) -> bool:
        table_name = item['table_name']
        record_id = item['record_id']
        queue_id = item['queue_id']

        id_col_map = {
            'teachers': 'teacher_id',
            'students': 'student_id',
            'activity_logs': 'log_id'
        }
        pk_col = id_col_map.get(table_name)
        if not pk_col:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE {pk_col} = ?", (record_id,))
            record = cursor.fetchone()

            if not record:
                cursor.execute("DELETE FROM sync_queue WHERE queue_id = ?", (queue_id,))
                conn.commit()
                return True

            record_dict = dict(record)
            record_dict.pop('is_synced', None)

            self.supabase.table(table_name).upsert(record_dict).execute()

            cursor.execute(f"UPDATE {table_name} SET is_synced = 1 WHERE {pk_col} = ?", (record_id,))
            cursor.execute("DELETE FROM sync_queue WHERE queue_id = ?", (queue_id,))
            conn.commit()

            print(f"--> Successfully synced {table_name} ({record_id}) to cloud!")
            self.sync_status.emit(f"Synced {table_name} record to cloud.")
            return True

        except Exception as e:
            print(f"--> Failed to sync {table_name} ({record_id}): {e}")
            return False