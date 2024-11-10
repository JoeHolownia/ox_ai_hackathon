import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import tempfile
import os

# Set up the Streamlit page
st.set_page_config(page_title="Nutrition Assistant", page_icon="🍎")

st.image("logo.png", width=500)  # Adjust width as needed

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

# --- Main UI Components ---

# Camera button for file upload
st.markdown(
    "<h3 style='text-align: center;'>Tap the camera icon below to upload an image of your food:</h3>", 
    unsafe_allow_html=True
)

# st.subheader("Tap the camera icon below to upload an image of your food:")

# Custom camera icon button for file upload
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Display the camera icon as a button
    uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"], key="image_uploader")

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Food Image", use_container_width=True)  # Updated to use_container_width

if uploaded_image:

    # Define where to save the image
    save_path = f"./food_image.jpg"
    
    # Save the file
    with open(save_path, "wb") as file:
        file.write(uploaded_image.getbuffer())
    
    st.success(f"Image saved at: {save_path}")

    # # Convert the uploaded image to binary
    image_data = uploaded_image.read()

    files = {
        "file": image_data
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

# Chatbot-like input box with placeholder text
user_input = st.text_input("", placeholder="")

# --- Processing Input ---

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
        else:
            st.write("Error: Unable to get a response from the chatbot API.")
    except Exception as e:
        st.write("Error:", e)
