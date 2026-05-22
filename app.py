import streamlit as st

# --- 1. GAME CONFIGURATION & MEMORY ---
st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

# Initialize session state to track clues and game completion
if "clues" not in st.session_state:
    st.session_state.clues = []
if "solved" not in st.session_state:
    st.session_state.solved = False

# --- 2. THE STORY & DATABASE ---
# You will replace the video URLs with the actual ones you upload
suspects = {
    "Rahul": {
        "room": "The Kitchen",
        "video_url": "https://www.youtube.com/watch?v=...", # Placeholder
        "clue": "The murderer has a sweet tooth."
    },
    "Aditi": {
        "room": "The Library",
        "video_url": "https://www.youtube.com/watch?v=...", 
        "clue": "I saw someone carrying a heavy candlestick earlier."
    },
    "Karan": {
        "room": "The Garden",
        "video_url": "https://www.youtube.com/watch?v=...", 
        "clue": "The crime definitely happened indoors."
    }
}

# --- 3. SIDEBAR NAVIGATION & INVENTORY ---
with st.sidebar:
    st.header("🗺️ Map")
    # Navigation buttons
    current_room = st.radio("Go to:", ["The Kitchen", "The Library", "The Garden", "The Grand Hall (Make Accusation)"])
    
    st.divider()
    
    st.header("🎒 Your Clues")
    if not st.session_state.clues:
        st.write("Explore the house to find clues!")
    else:
        for clue in set(st.session_state.clues):
            st.warning(clue)

# --- 4. MAIN GAME SCREENS ---
st.title("🕵️‍♀️ Shanaya's Birthday Mystery")

if current_room != "The Grand Hall (Make Accusation)":
    st.subheader(f"📍 You are in: {current_room}")
    st.write("Look around... who do you want to talk to?")
    
    # Filter suspects based on the current room
    people_here = [name for name, details in suspects.items() if details["room"] == current_room]
    
    if people_here:
        # Create a layout column for each person
        cols = st.columns(len(people_here))
        for i, person in enumerate(people_here):
            with cols[i]:
                # Later, you can add st.image() here to show their picture!
                if st.button(f"Talk to {person}"):
                    st.success(f"{person} says Happy Birthday!")
                    # Show their video
                    st.video(suspects[person]["video_url"])
                    # Add clue to inventory
                    if suspects[person]["clue"] not in st.session_state.clues:
                        st.session_state.clues.append(suspects[person]["clue"])
                        st.balloons() # Fun animation when finding a new clue!
    else:
        st.write("It's quiet in here. Nobody is around.")

# --- 5. THE FINAL ACCUSATION ---
elif current_room == "The Grand Hall (Make Accusation)":
    st.subheader("⚖️ Time to solve the mystery!")
    st.write("Review your clues in the sidebar. Who did it? Where? And with what?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        guess_who = st.selectbox("Who is the murderer?", ["Select", "Rahul", "Aditi", "Karan"])
    with col2:
        guess_where = st.selectbox("Where did it happen?", ["Select", "The Kitchen", "The Library", "The Garden"])
    with col3:
        guess_weapon = st.selectbox("What was the weapon?", ["Select", "Candlestick", "Poison", "Rope"])
        
    if st.button("Submit Accusation"):
        # Set the correct answers here
        if guess_who == "Rahul" and guess_where == "The Kitchen" and guess_weapon == "Candlestick":
            st.session_state.solved = True
            st.success("🎉 YOU SOLVED IT! 🎉")
            st.markdown("### 🎁 Your Reward: [Link to Digital Gift Card / Voucher]")
            st.snow()
        else:
            st.error("Not quite right... review your clues and try again!")
