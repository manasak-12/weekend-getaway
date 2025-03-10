import os
import streamlit as st
import requests
from datetime import datetime, timedelta
from groq import Groq

# Set up API keys (ensure they are securely managed)
os.environ["GROQ_API_KEY"] = "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"
WEATHER_API_KEY = "7f315248aa15f08e5d5e7cc256193ffd"

client = Groq()

# Title for the Streamlit app
st.title("🌍✨ AI Weekend Getaway Planner ✨🚗")
st.write("🔹 Spontaneous weekend trips, personalized just for you! 🎒💨")

with st.sidebar:
    # User inputs
    home_city = st.text_input("Enter your city of departure:")
    budget = st.number_input("Enter your budget (in INR):", min_value=5000, step=5000)
    preferences = st.text_area("Enter your preferences (e.g., adventure, relaxation, food, nightlife):")
    trip_length = st.slider("Trip Duration (days):", 1, 3, 2)
    max_travel_time = st.slider("Max Travel Time (hours):", 1, 6, 3)
    start_date = datetime.today()
    end_date = start_date + timedelta(days=trip_length)

# Function to get real-time weather data
def get_weather(destination):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("weather"):
        return response["weather"][0]["description"], response["main"]["temp"]
    return "Weather data unavailable", "-"

# Button to generate itinerary
if st.button("Plan My Getaway!"):
    if not home_city or not budget or not preferences:
        st.error("Please fill in all fields to generate your itinerary.")
    else:
        with st.spinner("Crafting your perfect weekend escape... ✨"):
            try:
                messages = [
                    {"role": "system", "content": "You are an AI travel planner specializing in last-minute weekend getaways."},
                    {"role": "user", "content": (
                        f"I am in {home_city} with a budget of ₹{budget}. I want a getaway from {start_date.strftime('%Y-%m-%d')} "
                        f"to {end_date.strftime('%Y-%m-%d')}. My preferences: {preferences}. Max travel time: {max_travel_time} hours. "
                        "Recommend a great destination with an itinerary including transport, activities, food, and accommodation."
                    )}
                ]

                response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages)
                trip_plan = response.choices[0].message.content

                # Extract destination for weather lookup
                destination = trip_plan.split("Destination:")[1].split("\n")[0] if "Destination:" in trip_plan else "Unknown"
                weather, temp = get_weather(destination)
                
                st.success("Your spontaneous weekend getaway is ready! 🎉")
                st.subheader(f"🌍 Destination: {destination}")
                st.write(f"🌤 Weather: {weather}, {temp}°C")
                st.write("📌 Your Itinerary:")
                st.markdown(trip_plan, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")

# Footer with Team Info
st.markdown("---")
st.markdown("### 🤝 Developed by Schrodinger's Code")
st.markdown("**Team Members:**  ")
st.markdown("- Anagha V  ")
st.markdown("- Uzayr Iqbal Hamid  ")
st.markdown("- K Manasa")
