import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
from datetime import datetime
from database import init_db, insert_meal, get_meals, get_symptoms

init_db()

# Set up the Streamlit page
st.set_page_config(page_title="Nutrify", page_icon="🍎")

st.image("logo.png", width=500)  # Adjust width as needed
# --- Meal Date Input as a Header ---
st.markdown(
    "<h4 style='text-align: center;'>Select the meal date:</h4>", 
    unsafe_allow_html=True
)

# Meal date input (user selects the day of the meal) with max_date set to today
meal_date = st.date_input("", datetime.today(), max_value=datetime.today())

tab1, tab2 = st.tabs(["Log Meal", "Log Symptoms"])

# Title and instructions


with tab1:
    st.markdown(
        "<h4 style='text-align: center;'>Upload a food image and enter meal details below:</h4>", 
        unsafe_allow_html=True
    )

    # --- Main UI Components ---

    # Camera button for file upload
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Display the camera icon as a button
        uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"], key="image_uploader")

        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Food Image", use_container_width=True)  # Updated to use_container_width


    st.markdown(
        "<h4 style='text-align: center;'>Ask Nutrify about your food:</h4>", 
        unsafe_allow_html=True
    )
    # Chatbot-like input box with placeholder text
    user_input = st.text_input("", placeholder="Ask me a question about the food")

    # Simulate chatbot output (you can connect to an actual chatbot API later)
    chatbot_output = ""
    if user_input and uploaded_image:
        # Display the user query
        st.write(f"User asked: {user_input}")
        
        # Mock API call for chatbot response
        # (In a real implementation, send the image and user input to a chatbot API)
        chatbot_output = f"Chatbot response: Here is the nutritional information for your meal. {user_input}"
        st.write(chatbot_output)

with tab2:
    # --- Health Symptoms Text Box ---
    st.markdown(
        "<h4 style='text-align: center;'>Please describe any health symptoms you are experiencing:</h4>", 
        unsafe_allow_html=True
    )

    health_symptoms = st.text_input("", placeholder="Describe your symptoms here")


# Submit button
if st.button("Submit"):
    if uploaded_image and health_symptoms:
        # Save image as a binary blob
        meal_image_binary = uploaded_image.read()
        date = meal_date.strftime("%Y-%m-%d")  # Use the selected date for the meal
        
        # Insert all the data into the database
        insert_meal(date, meal_image_binary, "Meal Description", "Nutrient Info", chatbot_output, health_symptoms)
        st.success("Meal and health symptoms submitted successfully!")
    else:
        st.error("Please make sure to fill in all the fields (image, symptoms, and questions).")


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#SIDE BAR
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
st.sidebar.markdown("## Meal History Calendar")
st.sidebar.write("View your meal log and nutritional insights here.")

# Function to generate list of months from Jan 2024 to current month
def get_months():
    current_date = datetime.now()
    start_year = 2024
    months = []
    
    for year in range(start_year, current_date.year + 1):
        start_month = 1 if year > start_year else 1
        end_month = current_date.month if year == current_date.year else 12
        for month in range(start_month, end_month + 1):
            month_name = datetime(year, month, 1).strftime('%B %Y')
            months.append(month_name)
    
    return months

# Generate a list of months (from January 2024 to the current month)
months = get_months()

# Set the default month to the current month by using the index of the current month
selected_month = st.sidebar.selectbox("Select a month", months, index=len(months) - 1)

# Extract the selected month and year
selected_month_date = datetime.strptime(selected_month, "%B %Y")
month_name = selected_month_date.strftime("%B %Y")
days_in_month = (pd.to_datetime(f'{selected_month_date.year}-{selected_month_date.month}-01') + pd.DateOffset(months=1) - pd.DateOffset(days=1)).day

# Fetch meals from the database and filter by selected month
def get_meals_by_month(selected_month_date):
    meals = get_meals()
    filtered_meals = []
    for meal in meals:
        meal_date = pd.to_datetime(meal[1])  # Convert stored string to datetime
        if meal_date.month == selected_month_date.month and meal_date.year == selected_month_date.year:
            filtered_meals.append(meal)
    return filtered_meals

# Fetch meals for the selected month
filtered_meals = get_meals_by_month(selected_month_date)

# Initialize lists for nutrient values and symptoms
meal_nutrients = []
meal_symptoms = []

for meal in filtered_meals:
    meal_date = pd.to_datetime(meal[1])
    nutrient_value = meal[5]  # Assuming this is the nutritional value
    symptoms = meal[6]  # Assuming this stores the symptoms
    
    if nutrient_value:
        meal_nutrients.append(nutrient_value)
    if symptoms:
        meal_symptoms.append(symptoms)

# Now, create a DataFrame for correlation
# df = pd.DataFrame({
#     'Nutrient Value': meal_nutrients,
#     'Symptoms': meal_symptoms
# })

# # Generate the plot in the sidebar
# if len(df) > 0:
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(x='Nutrient Value', y='Symptoms', data=df)
#     plt.title(f'Nutrient Correlation with Symptoms for {month_name}')
#     plt.xlabel('Nutrient Value')
#     plt.ylabel('Symptoms')
#     st.sidebar.pyplot(plt)
# else:
#     st.sidebar.write("No data available for this month to show the correlation.")


# Initialize the calendar layout
meal_by_day = {day: [] for day in range(1, days_in_month + 1)}

# Map meals to days of the selected month
for meal in filtered_meals:
    meal_date = pd.to_datetime(meal[1])
    if meal_date.month == selected_month_date.month and meal_date.year == selected_month_date.year:
        meal_by_day[meal_date.day].append(meal)

# Function to fetch chatbot information for a day
def get_chatbot_info(day):
    if day in meal_by_day:
        return f"Information for day {day}: Here are the meals and nutrients for this day."
    return "No meal information logged for this day."

# Render the calendar in the sidebar
st.sidebar.markdown(f"<h2 style='text-align: center;'>{month_name}</h2>", unsafe_allow_html=True)

# Create a 7x5 grid for the calendar (7 columns for the weekdays, 5 rows for the month)
cols = st.sidebar.columns(7)

row_count = 5  # 5 rows for the calendar grid (to cover all 31 days of the month)
days_in_week = 7  # 7 columns to represent Sunday to Saturday

# Add some empty padding for the calendar days to start on the correct day of the week
start_day = pd.to_datetime(f'{selected_month_date.year}-{selected_month_date.month}-01').weekday()
empty_cells = [None] * start_day  # Empty cells before the first day of the month

# Create a list of all days that should appear in the calendar (with empty cells before the start day)
calendar_days = [None] * start_day + list(range(1, days_in_month + 1))

# Render the calendar
for row in range(row_count):
    cols_in_row = st.sidebar.columns(7)  # Create a new row of 7 columns (Sunday-Saturday)
    for col, day in enumerate(calendar_days[row * 7: (row + 1) * 7]):
        if day is not None:
            with cols_in_row[col]:
                day_button = st.button(f"{day}", key=f"day_{day}")
                if day_button:
                    chatbot_info = get_chatbot_info(day)
                    st.sidebar.write(chatbot_info)
        else:
            with cols_in_row[col]:
                st.write("")  # Empty cell if there's no day to display

# Display symptoms
st.sidebar.subheader("Symptom History")
symptoms = get_symptoms()
symptom_df = pd.DataFrame(symptoms, columns=["ID", "Date", "Description", "Level"])
st.sidebar.write(symptom_df[["Date", "Description", "Level"]])
# Placeholder for Nutritional Analysis
st.sidebar.subheader("Nutritional Analysis & Suggestions")
st.sidebar.write("Your nutrient intake trends and suggestions will appear here.")
