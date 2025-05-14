import streamlit as st
import openai
import random
from streamlit_autorefresh import st_autorefresh

# ====== OpenAI API 設定 ======
openai.api_key = "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"

# ====== 房間數據初始化 ======
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Living Room": {"temperature": 25.0, "humidity": 50.0, "light": False},
        "Dining Room": {"temperature": 24.0, "humidity": 55.0, "light": True},
        "Kitchen": {"temperature": 26.0, "humidity": 45.0, "light": False},
    }


# 模擬數據更新
def simulate_data():
    for room in st.session_state.rooms:
        room_data = st.session_state.rooms[room]
        temp_change = random.uniform(-0.3, 0.3)
        room_data["temperature"] = round(room_data["temperature"] + temp_change, 1)
        room_data["temperature"] = max(min(room_data["temperature"], 30.0), 20.0)

        humidity_change = random.uniform(-2, 2)
        room_data["humidity"] = round(room_data["humidity"] + humidity_change, 1)
        room_data["humidity"] = max(min(room_data["humidity"], 70.0), 30.0)


# 根據溫度設置顏色
def get_temp_color(temp):
    if temp < 22:
        return "#add8e6"
    elif temp < 26:
        return "#90ee90"
    else:
        return "#ff7f7f"


# 顯示房間狀態
def show_room_status(name, data):
    bg_color = get_temp_color(data["temperature"])
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
    if st.button(f"Toggle {name} Light", key=f"light_{name}"):
        data["light"] = not data["light"]


# 向 LLM 提問並獲得回應
def ask_llm_about_rooms(question):
    prompt = f"""
    Here are the real-time statuses of different rooms in the smart house:
    {st.session_state.rooms}

    Based on the above information, please answer the user's question:
    {question}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用 gpt-3.5-turbo 模型
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


# ====== Streamlit Page 設定 ======
st.set_page_config(page_title="Smart House", layout="wide")
st.title("🏠 Smart House")

# ====== Auto Refresh 每 15 秒 ======
st_autorefresh(interval=15000, limit=None, key="datarefresh")

# 模擬數據更新
simulate_data()

# 顯示房間狀態
col1, col2, col3 = st.columns(3)
with col1:
    show_room_status("Living Room", st.session_state.rooms["Living Room"])
with col2:
    show_room_status("Dining Room", st.session_state.rooms["Dining Room"])
with col3:
    show_room_status("Kitchen", st.session_state.rooms["Kitchen"])

st.divider()

# ====== LLM 問答區 ======
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
