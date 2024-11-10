# app.py
import streamlit as st
import pandas as pd
import datetime
from database import init_db, insert_meal, insert_symptom, get_meals, get_symptoms

# Initialize Database
init_db()

# Title and tabs
st.title("Personal Health & Nutrition Tracker")
tab1, tab2, tab3 = st.tabs(["Log Meal", "Log Symptoms", "History & Analysis"])

# Log Meal Tab
with tab1:
    st.header("Log Your Meal")
    date = st.date_input("Meal Date", datetime.date.today())
    meal_description = st.text_input("Meal Description")
    meal_image = st.file_uploader("Upload Meal Image (optional)", type=["jpg", "png"])

    if st.button("Save Meal"):
        if meal_description:
            nutrient_info = "Sample nutrient data"  # Placeholder for AI-based nutrient analysis
            insert_meal(date, meal_image.read() if meal_image else None, meal_description, nutrient_info)
            st.success("Meal logged successfully!")
        else:
            st.warning("Please enter a meal description.")

# Log Symptoms Tab
with tab2:
    st.header("Log Your Symptoms")
    date = st.date_input("Symptom Date", datetime.date.today())
    symptom_description = st.text_input("Symptom Description")
    symptom_level = st.slider("Symptom Severity Level (1-10)", 1, 10, 5)

    if st.button("Save Symptom"):
        if symptom_description:
            insert_symptom(date, symptom_description, symptom_level)
            st.success("Symptom logged successfully!")
        else:
            st.warning("Please enter a symptom description.")

# History & Analysis Tab
with tab3:
    st.header("View Meal & Symptom History")

    # Display meals
    st.subheader("Meal History")
    meals = get_meals()
    meal_df = pd.DataFrame(meals, columns=["ID", "Date", "Image", "Description", "Nutrient Info"])
    st.write(meal_df[["Date", "Description", "Nutrient Info"]])

    # Display symptoms
    st.subheader("Symptom History")
    symptoms = get_symptoms()
    symptom_df = pd.DataFrame(symptoms, columns=["ID", "Date", "Description", "Level"])
    st.write(symptom_df[["Date", "Description", "Level"]])

    # Placeholder for Nutritional Analysis
    st.subheader("Nutritional Analysis & Suggestions")
    st.write("Your nutrient intake trends and suggestions will appear here.")

    # Placeholder for calendar view
    st.subheader("Calendar View (Placeholder)")
    st.write("Future implementation could include a calendar for detailed history view.")
