import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import tempfile
import os
import pandas as pd
from datetime import datetime
from database import init_db, insert_meal, get_meals, get_symptoms

init_db()

# Set up the Streamlit page
st.set_page_config(page_title="Nutrify", page_icon="🍎")

st.image("logo.png", width=500)  # Adjust width as needed

# --- Meal Date Input as a Header ---
st.markdown(
    "<h4 style='text-align: center;'>Select the date:</h4>", 
    unsafe_allow_html=True
)

# Title and instructions
# st.write("Upload a food image and ask questions about its nutritional information!")

# Sidebar for meal history
st.sidebar.markdown("## Meal History")
st.sidebar.write("View your meal log and nutritional insights here.")

# --- Setup chatpot api with ondemand ---

# Replace with your actual API key and external user ID
api_key = 'OZsN1bdvFouFV1dd3fBrZ5fBmHn2hbf3'
external_user_id = 'joeyjoejoe'

# Create Chat Session
create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
create_session_headers = {
    'apikey': api_key
}

create_session_body = {
    "pluginIds": [],
    "externalUserId": external_user_id
}
 
# Make the request to create a chat session
response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
response_data = response.json()

# Extract session ID from the response
session_id = response_data['data']['id']

# Meal date input (user selects the day of the meal) with max_date set to today
meal_date = st.date_input("", datetime.today(), max_value=datetime.today())

tab1, tab2 = st.tabs(["Log Meal", "Log Symptoms"])

# Submit Query details
submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
submit_query_headers = {
    'apikey': api_key
}

submit_img_url = f"https://api.on-demand.io/media/v1/public/file/raw"
submit_img_header = {
                 "content-type": "multipart/form-data",
                 "apikey": f"{api_key}"
}

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

        # HARDCODE IMAGE AT START
        uploaded_image = Image.open("eg_img.jpg")

        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Food Image", use_container_width=True)  # Updated to use_container_width


    if uploaded_image:

        # Define where to save the image
        # save_path = f"./food_image.jpg"
        
        # Save the file
        # with open(save_path, "wb") as file:
        #     file.write(uploaded_image.getbuffer())
        
        # # Convert the uploaded image to binary
        # image_data = uploaded_image.read()

        files = {
            "file": '' # TODO: left blank for now due to api errors
        }

        # st.write(f"{os.path.getsize(save_path)}")

        # img body data
        submit_img_body = {
            "createdBy": "Joe Holownia",
            "updatedBy": "Joe Holownia",
            "sessionId": f"{session_id}",
            "name": "image_of_food",
            "plugins": ["plugin-1712327325", "plugin-1713962163"],
            "sizeBytes":  7834093,
            "responseMode": "sync"
        }             

        # submit image to image api
        try:

            response = requests.post(submit_img_url, 
                                    headers=submit_img_header, 
                                    files=files, 
                                    data=submit_img_body)

            # To print the response
            # st.write(response.status_code)
            # st.write(response.json())
        except Exception as e:
            st.write("Error:", e)

        st.write("""
                 Chatbot response (using example image): \n\n

                 Here are the food items I detected!

                 \nBread (Ciabatta) - Two halves
                 \nVeggie Patty - One patty
                 \nTomato Slices - Few slices
                 \nPickles - Few slices
                 """)

    st.markdown(
        "<h4 style='text-align: center;'>Ask Nutrify about your food:</h4>", 
        unsafe_allow_html=True
    )

    # Chatbot-like input box with placeholder text
    user_input = st.text_input("", placeholder="Anything you'd like to correct about my food detection? Or any questions about its nutritional value?")

    # Simulate chatbot output (you can connect to an actual chatbot API later)
    chatbot_output = ""
    if user_input and uploaded_image:
        
        # Display the user query
        st.write(f"User asked: {user_input}")

        # chat query body data
        submit_query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": f"{user_input}",
            "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
            "responseMode": "sync"
        }

        try:
            response = requests.post(submit_query_url,
                                    headers=submit_query_headers,
                                    json=submit_query_body
                                    )
            if response.status_code == 200:
                result = response.json()
                print(result)
                # Display the chatbot's response
                st.write("Chatbot response:")
                st.write(result['data']['answer'])
        
        except Exception as e:
            st.write("Error:", e)


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

# # Display symptoms
st.sidebar.subheader("Symptom History")
# symptoms = get_symptoms()
# symptom_df = pd.DataFrame(symptoms, columns=["ID", "Date", "Description", "Level"])
# st.sidebar.write(symptom_df[["Date", "Description", "Level"]])
# # Placeholder for Nutritional Analysis
# st.sidebar.subheader("Nutritional Analysis & Suggestions")
# st.sidebar.write("Your nutrient intake trends and suggestions will appear here.")
