import streamlit as st
import google.generativeai as genai
import random

# Replace with your actual Gemini API key
genai.configure(api_key=st.secrets["AIzaSyByWTC_pAlxt1IcyfPtMU-cieWQPWkjT9o"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

st.set_page_config(page_title="🕵️ Dark Secrets RPG", layout="centered")
st.title("🕵️ Dark Secrets RPG")
st.markdown("Step into the shoes of a young and motivated journalist in a rain-soaked city full of secrets and corruption.")

# Initialize game state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "name": "Amanda Lee",
        "location": "Rainy alleyway",
        "occupation": "Journalist",
        "inventory": ["notebook", "camera"],
        "hp": 20,
        "log": [],
        "started": False
    }

game_state = st.session_state.game_state

# 🎯 Dice roll
def roll_d20():
    return random.randint(1, 20)

def skill_check(threshold=12):
    roll = roll_d20()
    return roll, roll >= threshold

# 🤖 AI response
def generate_dm_response(player_input, state):
    system_prompt = f"""You are a noir narrator and dungeon master guiding the player through a gritty 1950s detective mystery. The player is a young female journalist who believes in justice.
Use stylized noir language: moody, cynical, dramatic. Respond to the player's actions with consequences, discoveries, or twists. Be brief but flavorful. Maximum 5 sentences.
If the die roll is under 12, reflect failure in the narrative.
Detective: {state['name']}, Occupation: {state['occupation']}, HP: {state['hp']}, Location: {state['location']}, Inventory: {state['inventory']}"""

    user_prompt = f"The player says: '{player_input}'\nWhat happens next?"

    response = model.generate_content([
        {"role": "user", "parts": [system_prompt + "\n\n" + user_prompt]}
    ])
    return response.text

# 🕵️ Intro scene
def generate_intro(state):
    prompt = f"""You are a noir narrator. Begin a detective RPG with a moody intro set in a rainy city. 
Introduce the player as {state['name']}, a young naive journalist who believes in justice, in {state['location']}. 
Set the stage with atmosphere and hint at a mysterious case without requiring input yet. It should be 4 sentences."""
    response = model.generate_content(prompt)
    return response.text

# Start with a moody intro if not started yet
if not game_state["started"]:
    intro = generate_intro(game_state)
    game_state["log"].append(f"📜 DM: {intro}")
    game_state["started"] = True
    st.rerun()

# 🧭 Sidebar: Player Status
with st.sidebar:
    st.header("🧍‍♂️ Character Info")
    st.markdown(f"**Name:** {game_state['name']}")
    st.markdown(f"**Occupation:** {game_state['occupation']}")
    st.markdown(f"**Location:** {game_state['location']}")
    st.markdown("---")
    st.subheader("❤️ HP")
    st.markdown(f"{game_state['hp']} / 20")
    st.markdown("---")
    st.subheader("🎒 Inventory")
    if game_state["inventory"]:
        for item in game_state["inventory"]:
            st.markdown(f"- {item}")
    else:
        st.markdown("*(Empty)*")

# 💬 Chat log
for msg in game_state["log"]:
    if msg.startswith("🧍‍♂️ You:"):
        with st.chat_message("user"):
            st.markdown(msg.replace("🧍‍♂️ You: ", ""))
    elif msg.startswith("📜 DM:"):
        with st.chat_message("assistant"):
            st.markdown(msg.replace("📜 DM: ", ""))
    else:
        st.markdown(msg)

# 🎙️ Chat input
user_input = st.chat_input("What do you do?")

if user_input:
    roll, success = skill_check()
    outcome_text = f"🎲 You rolled a {roll} — {'Success!' if success else 'Failure.'}"
    game_state["log"].append(f"🧍‍♂️ You: {user_input}")
    game_state["log"].append(outcome_text)

    dm_response = generate_dm_response(user_input, game_state)
    game_state["log"].append(f"📜 DM: {dm_response}")
    st.rerun()
