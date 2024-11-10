# Nutrify - README

## Overview
Nutrify is an innovative app designed to help users track their nutritional intake, correlate diet to health symptoms, and provide personalized food recommendations based on their specific health needs. By combining AI-driven food recognition and health tracking, Nutrify empowers users to make informed decisions about their diet and optimize their wellness.

## Key Features
- **Food Recognition**: Take a picture of your meal or input the meal via text or audio. The app analyzes the food, identifies ingredients, and estimates their nutritional content.
- **Nutritional Insights**: Get detailed information about your meal’s nutritional profile, including fats, proteins, carbohydrates, vitamins, and minerals. The app compares your intake with the recommended daily values to guide healthier choices.
- **Symptom Tracking**: Log your symptoms and connect them to the foods you've eaten. The app uses historical data to identify food triggers for symptoms like headaches, low energy, or digestive discomfort.
- **Personalized Recommendations**: Based on the nutritional content of your meals and your health symptoms, Nutrify suggests foods to increase or avoid, helping you meet your health goals.
- **Meal History & Calendar**: View your meal history and track your nutrient intake on a visual calendar. Each day shows a photo of the meal, followed by its nutritional breakdown, enabling easy access to past meals and their correlation with symptoms.
  
## Workflow

### 1. **App Opening**
   - The app opens with a simple chatbot interface resembling GPT. There’s a button to open the camera, accompanied by a header explaining what the app does.

### 2. **Meal Input**
   - The user can either upload a picture of their meal, record an audio clip, or enter a text description (e.g., “I had sausage and banana for lunch”).
   - The bot will confirm the meal time, such as "Can I confirm you had lunch with sausage and banana?"
   - If a picture is provided, the bot estimates the meal time based on the user's local time.

### 3. **AI Analysis**
   - The picture or text input is sent to the backend, which calls the image recognition API.
   - The AI identifies the food items in the image and estimates portion sizes, then calculates the nutritional content (e.g., total fat, protein, carbs, etc.).
   - The app provides a summary of the total meal’s nutrient information and compares it to the recommended daily intake. The results are available as a downloadable CSV file.

### 4. **Symptom Tracking**
   - If the user logs symptoms (e.g., “I have a headache”), the app analyzes whether the symptoms could be related to foods eaten earlier. It uses historical data to determine if similar meals are correlated with these symptoms.

### 5. **Meal History**
   - The user can view their meal history, with images and nutritional information displayed for each day. This is useful for tracking diet over time and for consultations with healthcare providers.

### 6. **Nutritional Recommendations**
   - Based on the nutritional analysis, the app will suggest which nutrients the user may need more of to meet their daily goals and identify any foods that may be contributing to health symptoms.

## The Challenge
- **Difficult to Track Nutrient Intake**: Many people struggle to accurately track their daily nutrition, which can lead to poor diet choices and health issues.
- **Correlating Diet with Symptoms**: It’s hard to determine how certain foods affect your mood, energy levels, or sleep.
- **Manual Tracking is Time-Consuming**: Keeping a food diary is tedious and often incomplete, leading to inaccurate or missing data.
  
## The Solution
Nutrify addresses these challenges by automating food tracking through AI-powered analysis. The app makes it easy to:
- **Log meals** through images, audio, or text.
- **Get instant nutritional insights**, with a focus on the nutrients that matter most.
- **Track symptoms** and correlate them with foods to identify potential triggers.
- **Make personalized recommendations** to improve both physical and mental health.

## Product Benefits
- **Food Triggers Identification**: Identify foods that trigger symptoms (e.g., headaches, digestive issues) based on your dietary history.
- **Boost Mental & Physical Performance**: Track your nutrient intake and understand its effect on your mood, energy levels, and overall wellness.
- **Reinforce Positive Wellness Behaviors**: Stay motivated by seeing how your food choices impact your well-being.
- **Informed Food Choices**: Make smarter, data-driven decisions about what to eat based on your personal health data.

## Target Audience
- **Chronic Disease Sufferers**: People with conditions like obesity, diabetes, and cardiovascular disease, where diet plays a key role.
- **Individuals with IBS**: People who need to identify which foods trigger flare-ups and track their impact on symptoms.
- **Vegan/Vegetarian Dieters**: Individuals who follow a plant-based diet and need to monitor nutrient intake to prevent deficiencies (e.g., B12 deficiency).
- **Health-Conscious Individuals**: Anyone who wants to improve their nutrition and mental well-being.

## Market Opportunity
- The **global health and wellness market** is projected to reach USD $7 trillion by 2025.
- Increasing demand for **personalized health tracking tools** with AI integration.
- The **AI-driven wellness tech market** is rapidly growing, with more than 311 million mobile health app users in 2024 alone.
- Nutrify can scale across various markets, including fitness, mental health, and dietary sectors.

## Business Model
- **Subscription-Based Pricing**: 
  - £2 per month or £20 per year.
  - Low maintenance and scalable, ensuring consistent cash flow for the app.
- **Potential Partnerships**: Collaborations with wellness brands, dietitians, healthcare providers, and food delivery services.


## Conclusion
Nutrify is designed to empower individuals to take control of their health through personalized nutrition tracking. With its intuitive interface, AI-driven insights, and focus on connecting food intake to health symptoms, Nutrify makes it easier to eat healthier, manage chronic conditions, and boost overall well-being.


## Usage:

For the streamlit demo, run:

pip install streamlit
pip install pandas
pip install sqlite3
pip install matplotlib

Then to run the app locally in your web browser, run:

streamlit run app.py
