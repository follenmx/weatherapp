import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

api_key = st.secrets['key']

st.set_page_config(page_title='Weather App',
                   page_icon='👻')
st.title('Weather App 👻')
st.markdown('---')

def get_humidity_description(humidity):
    if humidity < 0 or humidity > 100:
        return "Invalid humidity value"

    if humidity <= 30:
        return "😓 Low Humidity Very dry air, may lead to dry skin and dehydration."
    elif humidity <= 50:
        return "😊 Comfortable Humidity Ideal for indoor environments, prevents moisture or dryness."
    elif humidity <= 70:
        return "😅 Moderate Humidity Slightly muggy but suitable for indoor activities."
    elif humidity < 100:
        return "😫 High Humidity Air feels heavy, may lead to mold and respiratory issues."
    else:
        return "💧 Dew Point Air is saturated, condensation forms on surfaces."

def get_pressure_description(pressure):
    if pressure < 1000:
        return "⛈️ Low Pressure. Brings stormy weather, precipitation, and strong winds."
    elif pressure <= 1013:
        return "☁️ Normal Pressure. Typical for most weather, fair conditions."
    elif pressure <= 1030:
        return "☀️ High Pressure. Brings stable, clear weather with little precipitation."
    elif pressure <= 1100:
        return "🌞 Very High Pressure. Brings prolonged clear, dry weather and temperature extremes."
    else:
        return "🌡️ Extreme Pressure. Rare, brings stable conditions and potential temperature extremes."

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
    
def categorize_weather(weather_description):
    clear_conditions = ["clear sky"]
    cloudy_conditions = ["few clouds", "scattered clouds", "broken clouds", "overcast clouds"]
    rain_conditions = ["light rain", "moderate rain", "heavy intensity rain", "light shower rain", "heavy shower rain"]
    snow_conditions = ["light snow", "moderate snow", "heavy snow"]
    thunderstorm_conditions = ["thunderstorm"]
    bad_conditions = ["mist", "fog", "haze", "dust", "sand"]
    tornado = ["tornado"]
    if weather_description in clear_conditions:
        weather_anim = load_lottiefile("lottiefiles/clearsky.json")
        st_lottie(weather_anim,
                  speed=0.6)
    elif weather_description in cloudy_conditions:
        weather_anim = load_lottiefile("lottiefiles/cloudysky.json")
        st_lottie(weather_anim,
                  speed=0.85)
    elif weather_description in rain_conditions:
        weather_anim = load_lottiefile("lottiefiles/rain.json")
        st_lottie(weather_anim,
                  speed=0.85)
    elif weather_description in thunderstorm_conditions:
        weather_anim = load_lottiefile("lottiefiles/thunder.json")
        st_lottie(weather_anim,
                  speed=0.85)
    elif weather_description in snow_conditions:
        weather_anim = load_lottiefile("lottiefiles/snow.json")
        st_lottie(weather_anim,
                  speed=0.85)
    elif weather_description in bad_conditions:
        weather_anim = load_lottiefile("lottiefiles/mist.json")
        st_lottie(weather_anim,
                  speed=0.85)
    elif weather_description in tornado:
        weather_anim = load_lottiefile("lottiefiles/tornado.json")
        st_lottie(weather_anim,
                  speed=0.85)

with st.form('Weather'):
    user_input = st.text_input('Please introduce your city')
    button = st.form_submit_button('Check')
    weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
    if button:
        if weather_data.json()['cod'] == '404':
            st.warning("No City Found")
        else:
            weather = weather_data.json()['weather'][0]['main']
            description = weather_data.json()['weather'][0]['description']
            pressure = weather_data.json()['main']['pressure']
            humidity = weather_data.json()['main']['humidity']
            temp = weather_data.json()['main']['temp']
            temp = (temp-32)*5/9
            humidity_description = get_humidity_description(humidity)
            pressure_description = get_pressure_description(pressure)
            col1,col2 = st.columns(2)
            with col1:
                categorize_weather(description)
            with col2:
                st.header(f"The temperature in {user_input} is: {int(temp)}ºC")
                st.subheader(f"The weather in {user_input} is: {weather}, with {description}")
                st.subheader(f'The humidity is {humidity}%')
                st.subheader(humidity_description)
                st.subheader(f'The pressure is {pressure} mb')
                st.subheader(pressure_description)
