import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. GAME CONFIGURATION ---
st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

st.title("🕵️‍♀️ Shanaya's Birthday Mystery")
st.markdown("### The lights are out in the mansion...")
st.write("Use **W, A, S, D** or the **Arrow Keys** to explore. Rooms are completely pitch black until you walk inside. Approach a suspect and press **Spacebar** to interrogate them.")

# --- 2. THE 2D GAME ENGINE (HTML/JS) ---
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; display: flex; justify-content: center; font-family: sans-serif; background-color: #0e1117;}
    canvas { 
        border: 4px solid #444; 
        border-radius: 8px;
        box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.1);
    }
    #game-container { position: relative; margin-bottom: 20px;}
    #dialogue-box {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #1e1e1e;
        color: white;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #555;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.8);
        text-align: center;
        width: 80%;
        max-width: 500px;
        z-index: 10;
    }
    #dialogue-box h2 { margin-top: 0; color: #ffeb3b; }
    #dialogue-box p { font-size: 18px; color: #ddd; }
    button { 
        background: #ff4b4b; color: white; border: none; 
        padding: 10px 20px; font-size: 16px; border-radius: 5px; 
        cursor: pointer; margin-top: 15px; font-weight: bold;
    }
    button:hover { background: #ff3333; }
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="800" height="500"></canvas>
    
    <div id="dialogue-box">
        <h2 id="npc-name">Name</h2>
        <div id="video-container"></div>
        <p id="npc-clue">Clue text goes here.</p>
        <button onclick="closeModal()">Close & Keep Searching</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // --- GAME DATA ---
    const player = { x: 400, y: 250, size: 24, color: "#00d2ff", speed: 5 };
    
    // Suspect Placements
    const npcs = [
        { name: "Rahul", x: 125, y: 125, size: 24, color: "#ff4b4b", clue: "The murderer has a sweet tooth.", video: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Aditi", x: 650, y: 125, size: 24, color: "#9c27b0", clue: "I saw someone carrying a heavy candlestick earlier.", video: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Karan", x: 125, y: 375, size: 24, color: "#ff9800", clue: "The crime definitely happened indoors.", video: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Prof. Aris", x: 650, y: 375, size: 24, color: "#4caf50", clue: "I was reading here all night. I heard a loud thud in the Kitchen.", video: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Mme. Elara", x: 400, y: 100, size: 24, color: "#e91e63", clue: "I found a strange liquid near the Garden.", video: "https://www.youtube.com/embed/dQw4w9WgXcQ" }
    ];

    let keys = {};
    let modalOpen = false;

    // --- INPUT HANDLING ---
    window.addEventListener("keydown", (e) => { 
        keys[e.code] = true; 
        if (e.code === "Space" && !modalOpen) { checkInteraction(); e.preventDefault(); }
        if (["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space"].includes(e.code)) e.preventDefault();
    });
    window.addEventListener("keyup", (e) => { keys[e.code] = false; });

    // --- ROOM LOGIC (Calculates where Shanaya is) ---
    function getCurrentRoom(x, y) {
        let cx = x + player.size/2;
        let cy = y + player.size/2;
        if (cx < 250 && cy < 250) return "Kitchen";
        if (cx >= 550 && cy < 250) return "Library";
        if (cx < 250 && cy >= 250) return "Garden";
        if (cx >= 550 && cy >= 250) return "Study";
        return "Hall";
    }

    // --- GAME LOOP ---
    function update() {
        if (!modalOpen) {
            if ((keys["KeyW"] || keys["ArrowUp"]) && player.y > 0) player.y -= player.speed;
            if ((keys["KeyS"] || keys["ArrowDown"]) && player.y < canvas.height - player.size) player.y += player.speed;
            if ((keys["KeyA"] || keys["ArrowLeft"]) && player.x > 0) player.x -= player.speed;
            if ((keys["KeyD"] || keys["ArrowRight"]) && player.x < canvas.width - player.size) player.x += player.speed;
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. Draw Base Rooms
        ctx.fillStyle = "#4a2511"; ctx.fillRect(0, 0, 250, 250); // Kitchen
        ctx.fillStyle = "#2c3e50"; ctx.fillRect(550, 0, 250, 250); // Library
        ctx.fillStyle = "#2d4a22"; ctx.fillRect(0, 250, 250, 250); // Garden
        ctx.fillStyle = "#3e2723"; ctx.fillRect(550, 250, 250, 250); // Study
        ctx.fillStyle = "#a67c52"; ctx.fillRect(250, 0, 300, 500); // Hall

        // Room Labels
        ctx.fillStyle = "rgba(255,255,255,0.3)"; ctx.font = "bold 24px Arial"; ctx.textAlign = "center";
        ctx.fillText("KITCHEN", 125, 135);
        ctx.fillText("LIBRARY", 675, 135);
        ctx.fillText("GARDEN", 125, 385);
        ctx.fillText("STUDY", 675, 385);
        ctx.fillStyle = "rgba(0,0,0,0.2)";
        ctx.fillText("GRAND HALL", 400, 260);

        // 2. Lighting System (Draw Darkness)
        let activeRoom = getCurrentRoom(player.x, player.y);
        ctx.fillStyle = "rgba(0, 0, 0, 0.95)"; // Pitch black overlay
        
        if (activeRoom !== "Kitchen") ctx.fillRect(0, 0, 250, 250);
        if (activeRoom !== "Library") ctx.fillRect(550, 0, 250, 250);
        if (activeRoom !== "Garden") ctx.fillRect(0, 250, 250, 250);
        if (activeRoom !== "Study") ctx.fillRect(550, 250, 250, 250);

        // 3. Draw NPCs (Only if in the same room, or if NPC is in the Hall)
        ctx.textAlign = "left";
        npcs.forEach(npc => {
            let npcRoom = getCurrentRoom(npc.x, npc.y);
            if (npcRoom === activeRoom || npcRoom === "Hall") {
                ctx.fillStyle = npc.color;
                ctx.beginPath();
                ctx.arc(npc.x + npc.size/2, npc.y + npc.size/2, npc.size/2, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "white"; ctx.font = "12px Arial";
                ctx.fillText(npc.name, npc.x - 10, npc.y - 10);
            }
        });

        // 4. Draw Player (Shanaya)
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(player.x + player.size/2, player.y + player.size/2, player.size/2, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "white"; ctx.font = "bold 12px Arial";
        ctx.fillText("You", player.x - 2, player.y - 10);
    }

    function loop() { update(); draw(); requestAnimationFrame(loop); }

    // --- INTERACTION ---
    function checkInteraction() {
        npcs.forEach(npc => {
            let dx = (player.x + player.size/2) - (npc.x + npc.size/2);
            let dy = (player.y + player.size/2) - (npc.y + npc.size/2);
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 50) {
                document.getElementById("npc-name").innerText = npc.name;
                document.getElementById("npc-clue").innerText = npc.clue;
                document.getElementById("video-container").innerHTML = `<iframe width="100%" height="250" src="${npc.video}" frameborder="0" allowfullscreen></iframe>`;
                document.getElementById("dialogue-box").style.display = "block";
                modalOpen = true;
            }
        });
    }

    window.closeModal = function() {
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = "";
        setTimeout(() => { modalOpen = false; }, 200);
    }

    loop();
</script>
</body>
</html>
"""

components.html(game_html, height=550)

st.divider()

# --- 3. DIGITAL CLUEDO TRACKER ---
st.header("📝 Detective's Clue Pad")
st.write("Use this board to track your findings. Check the boxes to rule out suspects, weapons, and rooms!")

# Initialize Cluedo card data inside session state so it remembers her ticks
if "clue_data" not in st.session_state:
    st.session_state.clue_data = pd.DataFrame({
        "Category": ["Suspect", "Suspect", "Suspect", "Suspect", "Suspect", 
                     "Weapon", "Weapon", "Weapon", "Weapon", "Weapon",
                     "Room", "Room", "Room", "Room", "Room"],
        "Item": ["Rahul", "Aditi", "Karan", "Prof. Aris", "Madame Elara",
                 "Candlestick", "Poison", "Rope", "Axe", "Dagger",
                 "Kitchen", "Library", "Garden", "Study", "Grand Hall"],
        "Possible 🤔": [False] * 15,
        "Ruled Out ❌": [False] * 15,
        "The Answer! 🎯": [False] * 15
    })

# Render the interactive dataframe
st.session_state.clue_data = st.data_editor(
    st.session_state.clue_data,
    hide_index=True,
    use_container_width=True,
    disabled=["Category", "Item"], # She can't accidentally delete the names
    height=570
)

st.divider()

# --- 4. THE FINAL ACCUSATION ---
st.subheader("⚖️ Ready to make the final accusation?")
col1, col2, col3 = st.columns(3)
with col1:
    guess_who = st.selectbox("Who did it?", ["Select", "Rahul", "Aditi", "Karan", "Prof. Aris", "Madame Elara"])
with col2:
    guess_where = st.selectbox("Where?", ["Select", "Kitchen", "Library", "Garden", "Study", "Grand Hall"])
with col3:
    guess_weapon = st.selectbox("With what?", ["Select", "Candlestick", "Poison", "Rope", "Axe", "Dagger"])
    
if st.button("Submit Accusation", use_container_width=True, type="primary"):
    if guess_who == "Rahul" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 YOU SOLVED IT! The mystery is unraveled. 🎉")
        st.balloons()
    else:
        st.error("Not quite right... keep investigating the dark rooms!")
