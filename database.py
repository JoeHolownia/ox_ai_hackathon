import sqlite3

# Initialize the database and create the meals table
def init_db():
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    
    # Table for meal logs with chatbot_output column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal_image BLOB,
        meal_description TEXT,
        nutrient_info TEXT,
        chatbot_output TEXT,
        symptoms TEXT
    )
    """)
    
    conn.commit()
    conn.close()

# Function to insert a meal into the database
def insert_meal(date, meal_image, meal_description, nutrient_info, chatbot_output, symptoms):
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO meals (date, meal_image, meal_description, nutrient_info, chatbot_output, symptoms) 
    VALUES (?, ?, ?, ?, ?, ?)""", 
                   (date, meal_image, meal_description, nutrient_info, chatbot_output, symptoms))
    conn.commit()
    conn.close()

# Function to fetch all meals from the database
def get_meals():
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    meals = cursor.fetchall()
    conn.close()
    return meals

# Function to fetch meals by a specific date (optional)
def get_meals_by_date(date):
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals WHERE date = ?", (date,))
    meals = cursor.fetchall()
    conn.close()
    return meals

# Function to fetch meals for a specific month (optional)
def get_meals_by_month(year, month):
    conn = sqlite3.connect("health_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM meals WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
    """, (str(year), str(month).zfill(2)))  # Ensures the month is two digits
    meals = cursor.fetchall()
    conn.close()
    return meals

def get_symptoms():
    conn = sqlite3.connect('health_tracker.db')
    cursor = conn.cursor()
    
    # Select only the symptoms column from the meals table
    cursor.execute('SELECT symptoms FROM meals')
    symptoms_data = cursor.fetchall()
    
    conn.close()

    # If symptoms are stored as comma-separated values, split them into individual symptoms
    symptoms_list = []
    for symptoms in symptoms_data:
        # Assuming symptoms are stored as a comma-separated string (e.g. "Headache, Nausea, Fatigue")
        symptoms_list.extend(symptoms[0].split(","))
    
    # Clean up any leading or trailing spaces from symptoms
    symptoms_list = [symptom.strip() for symptom in symptoms_list]
    
    return symptoms_list