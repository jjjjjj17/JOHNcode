import streamlit as st
import openai
import random
from streamlit_autorefresh import st_autorefresh
from abc import ABC, abstractmethod

openai.api_key = ""


class TemperatureControlStrategy(ABC):
    @abstractmethod
    def adjust_temperature(self, current_temp):
        pass


class NormalTemperatureControl(TemperatureControlStrategy):
    def adjust_temperature(self, current_temp):
        return current_temp


class CoolingTemperatureControl(TemperatureControlStrategy):
    def adjust_temperature(self, current_temp):
        return max(current_temp - 0.5, 20)


class HeatingTemperatureControl(TemperatureControlStrategy):
    def adjust_temperature(self, current_temp):
        return min(current_temp + 0.5, 30)


class Room:
    def __init__(
        self,
        name,
        temperature,
        humidity,
        light,
        temp_control_strategy: TemperatureControlStrategy,
    ):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.temp_control_strategy = temp_control_strategy
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def update_data(self):
        self.temperature = self.temp_control_strategy.adjust_temperature(
            self.temperature
        )
        humidity_change = random.uniform(-2, 2)
        self.humidity = round(self.humidity + humidity_change, 1)
        self.humidity = max(min(self.humidity, 70.0), 30.0)
        self.notify_observers()

    def toggle_light(self):
        self.light = not self.light

    def get_status(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "light": self.light,
        }


class RoomStatusDisplay:
    def update(self, room):
        self.show_room_status(room.name, room.get_status())

    def show_room_status(self, name, data):
        bg_color = self.get_temp_color(data["temperature"])
        st.markdown(
            f"""
            <div style="background-color: {bg_color}; padding: 15px; border-radius: 15px; text-align: center;">
                <h3>{name}</h3>
                <p>🌡️ <b>Temperature:</b> {data['temperature']} °C</p>
                <p>💧 <b>Humidity:</b> {data['humidity']} %</p>
                <p>💡 <b>Light:</b> {"ON" if data['light'] else "OFF"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def get_temp_color(self, temp):
        if temp < 22:
            return "#add8e6"
        elif temp < 26:
            return "#90ee90"
        else:
            return "#ff7f7f"


class RoomFactory:
    @staticmethod
    def create_room(name, temperature, humidity, light, temp_control_strategy):
        return Room(name, temperature, humidity, light, temp_control_strategy)


def ask_llm_about_rooms(question):
    prompt = f"""
    Here are the real-time statuses of different rooms in the smart house:
    {st.session_state.rooms}

    Based on the above information, please answer the user's question:
    {question}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.error.APIConnectionError as e:
        st.error(f"API connection error: {e}")
        return None
    except openai.error.Timeout as e:
        st.error(f"Request timed out: {e}")
        return None
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


st.set_page_config(page_title="Smart House", layout="wide")
st.title("🏠 Smart House")

st_autorefresh(interval=15000, limit=None, key="datarefresh")

if "rooms" not in st.session_state:

    living_room = RoomFactory.create_room(
        "Living Room", 25.0, 50.0, False, NormalTemperatureControl()
    )
    dining_room = RoomFactory.create_room(
        "Dining Room", 24.0, 55.0, True, CoolingTemperatureControl()
    )
    kitchen = RoomFactory.create_room(
        "Kitchen", 26.0, 45.0, False, HeatingTemperatureControl()
    )

    room_display = RoomStatusDisplay()

    living_room.add_observer(room_display)
    dining_room.add_observer(room_display)
    kitchen.add_observer(room_display)

    st.session_state.rooms = {
        "Living Room": living_room,
        "Dining Room": dining_room,
        "Kitchen": kitchen,
    }

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.rooms["Living Room"].update_data()
with col2:
    st.session_state.rooms["Dining Room"].update_data()
with col3:
    st.session_state.rooms["Kitchen"].update_data()

st.divider()

st.header("🤖 AI Assistant")

user_question = st.text_input(
    "Enter your question to the smart assistant (e.g., Do I need to turn on the AC?)"
)
if st.button("Ask AI") and user_question:
    with st.spinner("AI is thinking..."):
        llm_answer = ask_llm_about_rooms(user_question)
        st.success(llm_answer)

if st.button("🧠 Ask AI for overall suggestions"):
    with st.spinner("AI is analyzing..."):
        summary = ask_llm_about_rooms(
            "Based on the current status, provide a comprehensive suggestion including temperature, humidity, and lighting."
        )
        st.info(summary)
