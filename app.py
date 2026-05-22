import streamlit as st

# --- 1. GAME CONFIGURATION & MEMORY ---
st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="centered")

# Track game progress and navigation
if "clues" not in st.session_state:
    st.session_state.clues = []
if "solved" not in st.session_state:
    st.session_state.solved = False
if "current_room" not in st.session_state:
    st.session_state.current_room = "Map"

# Helper function to change rooms instantly
def change_room(room_name):
    st.session_state.current_room = room_name

# --- 2. THE STORY & DATABASE ---
suspects = {
    "Rahul": {
        "room": "The Kitchen",
        "video_url": "https://www.youtube.com/watch?v=...", 
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

# --- 3. THE MAIN MAP SCREEN ---
if st.session_state.current_room == "Map":
    st.title("🗺️ The Mansion Map")
    st.write("Click on a room to explore it and look for people!")
    
    # Building a visual floor plan using columns
    st.divider()
    
    # Top Row of rooms
    col1, col2 = st.columns(2)
    with col1:
        st.button("🍳 The Kitchen", use_container_width=True, on_click=change_room, args=("The Kitchen",))
    with col2:
        st.button("📚 The Library", use_container_width=True, on_click=change_room, args=("The Library",))
        
    # Bottom Row of rooms
    col3, col4 = st.columns(2)
    with col3:
        st.button("🌳 The Garden", use_container_width=True, on_click=change_room, args=("The Garden",))
    with col4:
        st.button("⚖️ The Grand Hall", use_container_width=True, on_click=change_room, args=("The Grand Hall",))
        
    st.divider()
    
    # Display inventory on the map screen
    st.header("🎒 Your Clues")
    if not st.session_state.clues:
        st.info("Explore the house to find clues!")
    else:
        for clue in set(st.session_state.clues):
            st.warning(clue)

# --- 4. INSIDE A ROOM ---
elif st.session_state.current_room != "The Grand Hall":
    room = st.session_state.current_room
    st.title(f"📍 {room}")
    
    # The crucial "Back" button
    st.button("⬅️ Back to Map", on_click=change_room, args=("Map",))
    st.divider()
    
    st.write("Look around... who do you want to talk to?")
    
    people_here = [name for name, details in suspects.items() if details["room"] == room]
    
    if people_here:
        cols = st.columns(len(people_here))
        for i, person in enumerate(people_here):
            with cols[i]:
                if st.button(f"Talk to {person}", use_container_width=True):
                    st.success(f"{person} says Happy Birthday!")
                    st.video(suspects[person]["video_url"])
                    
                    if suspects[person]["clue"] not in st.session_state.clues:
                        st.session_state.clues.append(suspects[person]["clue"])
                        st.balloons()
    else:
        st.write("It's quiet in here. Nobody is around.")

# --- 5. THE FINAL ACCUSATION (GRAND HALL) ---
elif st.session_state.current_room == "The Grand Hall":
    st.title("⚖️ The Grand Hall")
    st.button("⬅️ Back to Map", on_click=change_room, args=("Map",))
    st.divider()
    
    st.subheader("Time to solve the mystery!")
    st.write("Review your clues. Who did it? Where? And with what?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        guess_who = st.selectbox("Who is the murderer?", ["Select", "Rahul", "Aditi", "Karan"])
    with col2:
        guess_where = st.selectbox("Where did it happen?", ["Select", "The Kitchen", "The Library", "The Garden"])
    with col3:
        guess_weapon = st.selectbox("What was the weapon?", ["Select", "Candlestick", "Poison", "Rope"])
        
    if st.button("Submit Accusation", use_container_width=True):
        if guess_who == "Rahul" and guess_where == "The Kitchen" and guess_weapon == "Candlestick":
            st.session_state.solved = True
            st.success("🎉 YOU SOLVED IT! 🎉")
            st.snow()
        else:
            st.error("Not quite right... review your clues and try again!")
