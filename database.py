# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    # Table for meal logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal_image BLOB,
        meal_description TEXT,
        nutrient_info TEXT
    )
    """)
    # Table for symptoms and user updates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptoms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        symptom_description TEXT,
        symptom_level INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert_meal(date, meal_image, meal_description, nutrient_info):
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals (date, meal_image, meal_description, nutrient_info) VALUES (?, ?, ?, ?)",
                   (date, meal_image, meal_description, nutrient_info))
    conn.commit()
    conn.close()

def insert_symptom(date, symptom_description, symptom_level):
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO symptoms (date, symptom_description, symptom_level) VALUES (?, ?, ?)",
                   (date, symptom_description, symptom_level))
    conn.commit()
    conn.close()

def get_meals():
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    meals = cursor.fetchall()
    conn.close()
    return meals

def get_symptoms():
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM symptoms")
    symptoms = cursor.fetchall()
    conn.close()
    return symptoms
