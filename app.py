import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set up the Streamlit page
st.set_page_config(page_title="Nutrition Assistant", page_icon="🍎")

st.image("logo.png", width=500)  # Adjust width as needed

# Title and instructions
# st.write("Upload a food image and ask questions about its nutritional information!")

# Sidebar for meal history
st.sidebar.markdown("## Meal History")
st.sidebar.write("View your meal log and nutritional insights here.")

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

# Chatbot-like input box with placeholder text
user_input = st.text_input("", placeholder="Ask me a question")

# --- Processing Input ---

if user_input and uploaded_image:
    # Display the user query
    st.write(f"User asked: {user_input}")

    # Convert the uploaded image to binary
    image_data = uploaded_image.read()

    # Send the image and prompt to your chatbot API
    api_url = "https://your-chatbot-api-url.com/process"  # Replace with your actual API URL
    files = {'image': image_data}
    data = {'question': user_input}

    try:
        response = requests.post(api_url, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            # Display the chatbot's response
            st.write("Chatbot response:")
            st.write(result["answer"])
        else:
            st.write("Error: Unable to get a response from the chatbot API.")
    except Exception as e:
        st.write("Error:", e)
