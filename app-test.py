# app.py
import streamlit as st
import datetime
import requests
from PIL import Image
from io import BytesIO
from database import init_db, insert_meal, get_meals
from helpers import analyze_nutrient_intake
import pandas as pd

# Initialize Database
init_db()

# Title and layout
st.set_page_config(page_title="Personal Health & Nutrition Tracker", page_icon="🍎")
st.title("Personal Health & Nutrition Tracker")
st.write("Upload a food image and ask for its nutritional information!")

# Homepage: Food Image Upload + Chatbot
st.subheader("Upload Food Image")
uploaded_image = st.file_uploader("Choose an image of your food", type=["jpg", "png", "jpeg"])

# Chatbot-like prompt for user interaction
user_input = st.text_input("Ask me something!", "Give me the nutritional information for this food")

# Process the image and request nutritional info
if uploaded_image and user_input:
    st.image(uploaded_image, caption="Uploaded Food Image", use_column_width=True)
    st.write(f"User asked: {user_input}")

    # Call a function to process the image and get nutritional information
    # (replace this with your own API plugin for nutrition data)
    if "nutritional" in user_input.lower():
        # For now, we'll use a placeholder function to simulate this behavior
        # Replace this with actual API calls to your nutrition plugin
        img = Image.open(uploaded_image)
        nutrients = analyze_nutrient_intake(img)  # Placeholder for nutrient analysis
        st.write(f"Nutritional Information: {nutrients}")
        
        # Optionally, store this meal in the database
        date = datetime.date.today()
        meal_description = "Food image uploaded for nutritional analysis."
        nutrient_info = nutrients
        insert_meal(date, uploaded_image.read(), meal_description, nutrient_info)

else:
    st.write("Please upload an image and ask for nutritional information!")

# Meal History Tab
st.sidebar.header("Meal History")
meals = get_meals()
meal_df = pd.DataFrame(meals, columns=["ID", "Date", "Image", "Description", "Nutrient Info"])
st.sidebar.write(meal_df[["Date", "Description", "Nutrient Info"]])
