import streamlit as st
import speech_recognition as sr
import requests

# ---------------- PAGE ---------------- #

st.set_page_config(page_title="Voice Weather Agent", page_icon="🌤")

st.title("🌤 Voice Weather Agent")
st.write("Click the button below and speak the name of a city.")

st.markdown("---")

# ---------------- SPEECH ---------------- #

recognizer = sr.Recognizer()


def voice_input():

    with sr.Microphone() as source:

        st.info("🎙 Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        city = recognizer.recognize_google(audio)

        return city.title()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        st.error("Speech service unavailable.")
        return ""


# ---------------- WEATHER ---------------- #

def fetch_weather(city):

    api = f"https://wttr.in/{city}?format=j1"

    response = requests.get(api)

    if response.status_code != 200:
        return None

    weather_data = response.json()

    current = weather_data["current_condition"][0]

    details = {
        "temperature": current["temp_C"],
        "humidity": current["humidity"],
        "weather": current["weatherDesc"][0]["value"],
        "wind": current["windspeedKmph"]
    }

    return details


# ---------------- SUPPORTED CITIES ---------------- #

st.markdown("### Cities")

col1, col2 = st.columns(2)

with col1:
    st.write("• Chennai")
    st.write("• Coimbatore")
    st.write("• Bangalore")
    st.write("• Mumbai")
    st.write("• Delhi")

with col2:
    st.write("• Hyderabad")
    st.write("• London")
    st.write("• Dubai")
    st.write("• Tokyo")
    st.write("• New York")

st.markdown("---")

# ---------------- BUTTON ---------------- #

if st.button("🎤 Get Weather Report"):

    spoken_city = voice_input()

    if spoken_city == "":

        st.warning("Please speak a valid city name.")

    else:

        st.success(f"City Detected: {spoken_city}")

        result = fetch_weather(spoken_city)

        if result:

            st.markdown("## 📋 Weather Report")

            st.write(f"**📍 City :** {spoken_city}")
            st.write(f"**🌡 Temperature :** {result['temperature']} °C")
            st.write(f"**💧 Humidity :** {result['humidity']} %")
            st.write(f"**☁ Condition :** {result['weather']}")
            st.write(f"**🌬 Wind Speed :** {result['wind']} km/h")

        else:

            st.error("Unable to retrieve weather details.")