# app.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set up the Streamlit page
st.set_page_config(page_title="Nutrition Assistant", page_icon="🍎")

# Title and instructions
st.title("NUTRIFY")
st.write("Upload a food image and ask questions about its nutritional information!")

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
print(response_data)

# Extract session ID from the response
session_id = response_data['data']['id']

# Submit Query details
submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
submit_query_headers = {
    'apikey': api_key
}

# --- Main UI Components ---

# Camera button for file upload
st.subheader("Tap the camera icon below to upload an image of your food:")

# Custom camera icon button for file upload
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Display the camera icon as a button
    if st.button("📷 Upload Food Image", key="upload_button"):
        uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"], key="image_uploader")
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Food Image", use_column_width=True)

# Chatbot-like input box with placeholder text
user_input = st.text_input("", placeholder="Ask me a question")

# --- Processing Input ---

if user_input and uploaded_image:

    # Display the user query
    st.write(f"User asked: {user_input}")

    # Convert the uploaded image to binary
    image_data = uploaded_image.read()

    # TODO: we may need to include the files and data in this query body somehow for ondemand?
    submit_query_body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": f"{user_input}",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    # Send the image and prompt to your chatbot API
    # api_url = "https://api.on-demand.io/chat/v1/sessions"  # Replace with your actual API URL
    files = {'image': image_data}
    data = {'question': user_input}

    try:
        response = requests.post(submit_query_url,
                                 headers=submit_query_headers,
                                 json=submit_query_body,
                                 files=files, 
                                 data=data)
        if response.status_code == 200:
            result = response.json()
            # Display the chatbot's response
            st.write("Chatbot response:")
            st.write(result["answer"])
        else:
            st.write("Error: Unable to get a response from the chatbot API.")
    except Exception as e:
        st.write("Error:", e)

else:
    x = True