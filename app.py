import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

st.title("🕵️‍♀️ Shanaya's Birthday Mystery")
st.write("Use **W, A, S, D** or the **Arrow Keys** to move. Walk up to someone and press **Spacebar** to talk to them!")

# --- THE 2D GAME ENGINE (HTML/JS) ---
# We write the game in raw web code and embed it into Streamlit
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; display: flex; justify-content: center; font-family: sans-serif; }
    canvas { 
        background-color: #8FBC8F; /* Grassy/Carpet green background */
        border: 4px solid #2F4F4F; 
        border-radius: 8px;
    }
    #game-container { position: relative; }
    #dialogue-box {
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        width: 80%;
        max-width: 500px;
        z-index: 10;
    }
    #dialogue-box h2 { margin-top: 0; color: #333; }
    #dialogue-box p { font-size: 18px; color: #555; }
    button { 
        background: #FF4B4B; color: white; border: none; 
        padding: 10px 20px; font-size: 16px; border-radius: 5px; 
        cursor: pointer; margin-top: 15px;
    }
    button:hover { background: #FF3333; }
    iframe { border-radius: 8px; }
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
    const player = { x: 400, y: 250, size: 30, color: "blue", speed: 4 };
    
    // You can change their positions (x,y) and embed real YouTube video IDs later
    const npcs = [
        { name: "Rahul", x: 150, y: 100, size: 30, color: "red", clue: "The murderer has a sweet tooth.", video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Aditi", x: 650, y: 150, size: 30, color: "purple", clue: "I saw someone carrying a heavy candlestick earlier.", video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ" },
        { name: "Karan", x: 350, y: 400, size: 30, color: "orange", clue: "The crime definitely happened indoors.", video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ" }
    ];

    let keys = {};
    let modalOpen = false;

    // --- INPUT HANDLING ---
    window.addEventListener("keydown", (e) => { 
        keys[e.code] = true; 
        
        // Check for interaction when Spacebar is pressed
        if (e.code === "Space" && !modalOpen) {
            checkInteraction();
            e.preventDefault(); // Stop page from scrolling down
        }
    });
    window.addEventListener("keyup", (e) => { keys[e.code] = false; });

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

        // Draw NPCs
        npcs.forEach(npc => {
            ctx.fillStyle = npc.color;
            ctx.fillRect(npc.x, npc.y, npc.size, npc.size);
            ctx.fillStyle = "black";
            ctx.font = "14px Arial";
            ctx.fillText(npc.name, npc.x - 5, npc.y - 10);
        });

        // Draw Player (Shanaya)
        ctx.fillStyle = player.color;
        ctx.fillRect(player.x, player.y, player.size, player.size);
        ctx.fillStyle = "black";
        ctx.fillText("Shanaya", player.x - 15, player.y - 10);
    }

    function loop() {
        update();
        draw();
        requestAnimationFrame(loop);
    }

    // --- INTERACTION LOGIC ---
    function checkInteraction() {
        npcs.forEach(npc => {
            // Calculate distance between player and NPC
            let dx = (player.x + player.size/2) - (npc.x + npc.size/2);
            let dy = (player.y + player.size/2) - (npc.y + npc.size/2);
            let distance = Math.sqrt(dx * dx + dy * dy);

            // If close enough, open the modal
            if (distance < 60) {
                document.getElementById("npc-name").innerText = npc.name;
                document.getElementById("npc-clue").innerText = npc.clue;
                document.getElementById("video-container").innerHTML = `<iframe width="100%" height="250" src="${npc.video_url}" title="YouTube video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
                
                document.getElementById("dialogue-box").style.display = "block";
                modalOpen = true;
            }
        });
    }

    window.closeModal = function() {
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = ""; // Stop video from playing in background
        // Small delay to prevent instant re-triggering
        setTimeout(() => { modalOpen = false; }, 200);
    }

    // Start the game!
    loop();
</script>
</body>
</html>
"""

# Embed the game into the Streamlit app
components.html(game_html, height=550)

st.divider()

# Leave the accusation form at the bottom for when she finishes
st.subheader("⚖️ Ready to make an accusation?")
col1, col2, col3 = st.columns(3)
with col1:
    guess_who = st.selectbox("Who did it?", ["Select", "Rahul", "Aditi", "Karan"])
with col2:
    guess_where = st.selectbox("Where?", ["Select", "The Kitchen", "The Library", "The Garden"])
with col3:
    guess_weapon = st.selectbox("With what?", ["Select", "Candlestick", "Poison", "Rope"])
    
if st.button("Submit Final Accusation", use_container_width=True):
    if guess_who == "Rahul" and guess_where == "The Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 YOU SOLVED IT! 🎉")
        st.balloons()
    else:
        st.error("Not quite right... keep looking for clues!")
