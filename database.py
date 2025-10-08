import sqlite3
from datetime import datetime, date

class PlantDatabase:
    def __init__(self, db_name="plant_tracker.db"):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date_planted DATE,
                    care_plan TEXT,
                    last_watered DATE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plant_id INTEGER,
                    entry_date DATE,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE
                )
            ''')
            print("Database tables created successfully!")

    def execute_query(self, query, params=(), fetch=False, fetchall=False):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid if "INSERT" in query.upper() else True

    def add_plant(self, name, date_planted, care_plan):
        return self.execute_query(
            "INSERT INTO plants (name, date_planted, care_plan, last_watered) VALUES (?, ?, ?, ?)",
            (name, date_planted, care_plan, None)
        )

    def get_all_plants(self):
        return self.execute_query(
            "SELECT id, name, date_planted, care_plan, last_watered, created_at FROM plants ORDER BY created_at DESC",
            fetchall=True
        )

    def add_journal_entry(self, plant_id, entry_date, notes):
        return self.execute_query(
            "INSERT INTO journal_entries (plant_id, entry_date, notes) VALUES (?, ?, ?)",
            (plant_id, entry_date, notes)
        )

    def get_journal_entries(self, plant_id):
        return self.execute_query(
            "SELECT id, plant_id, entry_date, notes, created_at FROM journal_entries WHERE plant_id = ? ORDER BY entry_date DESC",
            (plant_id,), fetchall=True
        )

    def get_plant_by_id(self, plant_id):
        return self.execute_query(
            "SELECT id, name, date_planted, care_plan, last_watered, created_at FROM plants WHERE id = ?",
            (plant_id,), fetch=True
        )

    def delete_plant(self, plant_id):
        try:
            self.execute_query("DELETE FROM journal_entries WHERE plant_id = ?", (plant_id,))
            self.execute_query("DELETE FROM plants WHERE id = ?", (plant_id,))
            return True
        except Exception as e:
            print(f"Error deleting plant: {e}")
            return False

    def delete_journal_entry(self, entry_id):
        try:
            self.execute_query("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
            return True
        except Exception as e:
            print(f"Error deleting journal entry: {e}")
            return False

    def update_plant(self, plant_id, name, date_planted, care_plan):
        try:
            self.execute_query(
                "UPDATE plants SET name = ?, date_planted = ?, care_plan = ? WHERE id = ?",
                (name, date_planted, care_plan, plant_id)
            )
            return True
        except Exception as e:
            print(f"Error updating plant: {e}")
            return False

    def update_journal_entry(self, entry_id, entry_date, notes):
        try:
            self.execute_query(
                "UPDATE journal_entries SET entry_date = ?, notes = ? WHERE id = ?",
                (entry_date, notes, entry_id)
            )
            return True
        except Exception as e:
            print(f"Error updating journal entry: {e}")
            return False

    def water_plant(self, plant_id):
        """Mark plant as watered today"""
        today = date.today().isoformat()
        try:
            self.execute_query(
                "UPDATE plants SET last_watered = ? WHERE id = ?",
                (today, plant_id)
            )
            return True
        except Exception as e:
            print(f"Error watering plant: {e}")
            return False

    def needs_watering(self, plant):
        """Check if plant needs watering (not watered today)"""
        plant_id, name, date_planted, care_plan, last_watered, created_at = plant
        if last_watered is None:
            return True
        try:
            last_watered_date = date.fromisoformat(last_watered)
            return last_watered_date < date.today()
        except:
            return True
