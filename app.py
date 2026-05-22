import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. GAME CONFIGURATION ---
st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

# Center title and subtitle with custom styling
st.markdown("<h1 style='text-align: center; color: #ffeb3b;'>🕵️‍♀️ Shanaya's Birthday Mystery</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ddd; margin-bottom: 20px;'>Explore the dark mansion, interrogate suspects, and crack the case!</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Controls: WASD/Arrows to move, Space to interrogate, C to toggle Clue Pad.</p>", unsafe_allow_html=True)

# --- 2. GAME DATA (Python side) ---
suspects = [
    {"name": "Rahul", "clue": "The murderer has a sweet tooth.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#ff4b4b"},
    {"name": "Aditi", "clue": "I saw someone carrying a heavy candlestick earlier.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#9c27b0"},
    {"name": "Karan", "clue": "The crime definitely happened indoors.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#ff9800"},
    {"name": "Prof. Aris", "clue": "I heard a loud thud in the Kitchen while reading.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#4caf50"},
    {"name": "Mme. Elara", "clue": "I found a strange liquid near the Garden entrance.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#e91e63"}
]
weapons = ["Candlestick", "Poison", "Rope", "Axe", "Dagger"]
rooms = ["Kitchen", "Library", "Garden", "Study", "Grand Hall"]

# Convert suspects to JSON for JavaScript
suspects_json = json.dumps(suspects)
weapons_json = json.dumps(weapons)
rooms_json = json.dumps(rooms)

# --- 3. THE 2D GAME ENGINE & CLUE PAD (HTML/CSS/JS) ---
# Embed the entire game experience
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; display: flex; justify-content: center; font-family: 'Courier New', Courier, monospace; background-color: #121212; color: white; overflow: hidden;}}
    #game-pad-container {{ display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 1000px; padding: 20px; box-sizing: border-box;}}
    canvas {{ 
        border: 6px solid #444; 
        border-radius: 12px;
        box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.1);
        cursor: none; /* Hide standard cursor over game */
    }}
    #game-ui {{ position: relative; width: 100%; display: flex; flex-direction: column; align-items: center;}}

    /* Dialogue/Video Modal */
    #dialogue-box {{
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(30, 30, 30, 0.95);
        color: white;
        padding: 30px;
        border-radius: 16px;
        border: 3px solid #666;
        box-shadow: 0px 10px 50px rgba(0,0,0,1);
        text-align: center;
        width: 80%;
        max-width: 600px;
        z-index: 20;
    }}
    #dialogue-box h2 {{ margin-top: 0; color: #ffeb3b; font-size: 28px;}}
    #dialogue-box p {{ font-size: 20px; color: #ddd; margin: 20px 0; font-family: sans-serif;}}
    #video-container {{ margin: 20px 0; border-radius: 8px; overflow: hidden; border: 2px solid #555;}}
    .close-btn {{ 
        background: #ff4b4b; color: white; border: none; 
        padding: 12px 24px; font-size: 18px; border-radius: 8px; 
        cursor: pointer; font-weight: bold; transition: background 0.2s;
    }}
    .close-btn:hover {{ background: #ff3333; }}

    /* Clue Pad Overlay */
    #clue-pad-overlay {{
        display: none; /* Hidden by default */
        position: absolute;
        top: 10px;
        left: 10px;
        width: calc(100% - 20px);
        height: calc(100% - 20px);
        background: rgba(40, 40, 40, 0.98);
        border-radius: 12px;
        border: 4px solid #777;
        box-shadow: 0px 0px 40px rgba(0,0,0,0.9);
        z-index: 30;
        padding: 20px;
        box-sizing: border-box;
        overflow-y: auto; /* Allow scrolling within the pad */
    }}
    #clue-pad-overlay h2 {{ text-align: center; color: #81d4fa; margin-top: 0; }}
    #clue-pad-overlay h3 {{ color: #eee; margin-top: 25px; border-bottom: 2px solid #555; padding-bottom: 5px;}}
    .clue-category {{ margin-bottom: 20px; }}
    .clue-item {{ 
        display: flex; align-items: center; justify-content: space-between; 
        padding: 10px; border-bottom: 1px solid #333; 
        background: rgba(50, 50, 50, 0.5); border-radius: 4px; margin-bottom: 5px;
    }}
    .clue-item:last-child {{ border-bottom: none; }}
    .clue-name {{ font-size: 18px; color: #fff; font-weight: bold; flex-grow: 1; margin-right: 15px;}}
    .clue-status-buttons {{ display: flex; gap: 5px; }}
    .status-btn {{
        background: #444; color: #999; border: 1px solid #555;
        padding: 6px 12px; font-size: 16px; border-radius: 4px;
        cursor: pointer; transition: background 0.2s, color 0.2s;
    }}
    .status-btn.active {{ background: #555; color: #fff; border-color: #777;}}
    .status-btn.possible {{ color: #ffe082; }}
    .status-btn.possible.active {{ background: #616161; border-color: #fdd835;}}
    .status-btn.ruled-out {{ color: #ef9a9a; }}
    .status-btn.ruled-out.active {{ background: #616161; border-color: #e53935;}}
    .status-btn.answer {{ color: #a5d6a7; }}
    .status-btn.answer.active {{ background: #616161; border-color: #43a047;}}

    #pad-controls {{ display: flex; gap: 10px; justify-content: center; margin-top: 15px; width: 100%; }}
    .pad-toggle-btn {{
        background: #0288d1; color: white; border: none;
        padding: 10px 20px; font-size: 16px; border-radius: 8px;
        cursor: pointer; font-weight: bold; transition: background 0.2s;
    }}
    .pad-toggle-btn:hover {{ background: #0277bd; }}

    /* Custom Cursor */
    #custom-cursor {{
        position: absolute;
        width: 20px; height: 20px;
        background: rgba(255, 255, 255, 0.5);
        border: 2px solid white;
        border-radius: 50%;
        pointer-events: none; /* Don't interfere with clicks */
        transform: translate(-50%, -50%);
        z-index: 100;
        display: none; /* Hide initially */
    }}
</style>
</head>
<body>

<div id="game-pad-container">
    <div id="game-ui">
        <canvas id="gameCanvas" width="800" height="500"></canvas>
        <div id="custom-cursor"></div>
        
        <div id="dialogue-box">
            <h2 id="npc-name">Name</h2>
            <div id="video-container"></div>
            <p id="npc-clue">Clue text goes here.</p>
            <button class="close-btn" onclick="closeModal()">Close & Keep Searching</button>
        </div>

        <div id="clue-pad-overlay">
            <h2>🕵️‍♀️ Shanaya's Detective Pad</h2>
            <div id="clue-content"></div>
            <div style="text-align: center; margin-top: 20px;">
                <button class="pad-toggle-btn" onclick="toggleCluePad()">Close Pad (C)</button>
            </div>
        </div>
    </div>
    <div id="pad-controls">
        <button class="pad-toggle-btn" onclick="toggleCluePad()">Toggle Clue Pad (C)</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const cursor = document.getElementById("custom-cursor");

    // --- GAME DATA ---
    const suspects = {suspects_json};
    const weapons = {weapons_json};
    const rooms = {rooms_json};
    
    // Player - Pokémon styled sprite properties
    const player = {{ x: 400, y: 250, size: 28, color: "#00d2ff", speed: 6, facing: 'down' }};
    
    // NPC Properties (including new ones)
    const npcs = [
        {{ name: "Rahul", x: 125, y: 125, size: 28, color: suspects[0].color, clue: suspects[0].clue, video: suspects[0].video, canInteract: false }},
        {{ name: "Aditi", x: 675, y: 125, size: 28, color: suspects[1].color, clue: suspects[1].clue, video: suspects[1].video, canInteract: false }},
        {{ name: "Karan", x: 125, y: 375, size: 28, color: suspects[2].color, clue: suspects[2].clue, video: suspects[2].video, canInteract: false }},
        {{ name: "Prof. Aris", x: 675, y: 375, size: 28, color: suspects[3].color, clue: suspects[3].clue, video: suspects[3].video, canInteract: false }},
        {{ name: "Mme. Elara", x: 400, y: 100, size: 28, color: suspects[4].color, clue: suspects[4].clue, video: suspects[4].video, canInteract: false }}
    ];

    let keys = {{}};
    let modalOpen = false;
    let padOpen = false;
    let cluePadData = {{}}; // Store clue status (Possible/RuledOut/Answer)

    // --- INITIALIZE CLUE PAD DATA ---
    function initializeCluePadData() {{
        cluePadData = {{
            suspects: suspects.reduce((acc, s) => ({{ ...acc, [s.name]: 'none' }}), {{}}),
            weapons: weapons.reduce((acc, w) => ({{ ...acc, [w]: 'none' }}), {{}}),
            rooms: rooms.reduce((acc, r) => ({{ ...acc, [r]: 'none' }}), {{}})
        }};
    }}
    initializeCluePadData();

    // --- INPUT HANDLING ---
    window.addEventListener("keydown", (e) => {{ 
        keys[e.code] = true; 
        if (e.code === "Space" && !modalOpen && !padOpen) {{ checkInteraction(); e.preventDefault(); }}
        if (e.code === "KeyC") {{ toggleCluePad(); e.preventDefault(); }}
        if (["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space","KeyC","KeyW","KeyA","KeyS","KeyD"].includes(e.code)) e.preventDefault();
        
        // Update player facing direction
        if (e.code === "ArrowUp" || e.code === "KeyW") player.facing = 'up';
        if (e.code === "ArrowDown" || e.code === "KeyS") player.facing = 'down';
        if (e.code === "ArrowLeft" || e.code === "KeyA") player.facing = 'left';
        if (e.code === "ArrowRight" || e.code === "KeyD") player.facing = 'right';
    }});
    window.addEventListener("keyup", (e) => {{ keys[e.code] = false; }});

    // Custom Cursor tracking
    canvas.addEventListener('mousemove', (e) => {{
        const rect = canvas.getBoundingClientRect();
        cursor.style.left = (e.clientX - rect.left) + 'px';
        cursor.style.top = (e.clientY - rect.top) + 'px';
        cursor.style.display = 'block';
    }});
    canvas.addEventListener('mouseleave', () => {{ cursor.style.display = 'none'; }});


    // --- ROOM LOGIC (Calculates where Shanaya is) ---
    function getCurrentRoom(x, y) {{
        let cx = x + player.size/2;
        let cy = y + player.size/2;
        if (cx < 250 && cy < 250) return "Kitchen";
        if (cx >= 550 && cy < 250) return "Library";
        if (cx < 250 && cy >= 250) return "Garden";
        if (cx >= 550 && cy >= 250) return "Study";
        return "Grand Hall";
    }}

    // --- GAME LOOP ---
    function update() {{
        if (!modalOpen && !padOpen) {{
            if ((keys["KeyW"] || keys["ArrowUp"]) && player.y > 0) player.y -= player.speed;
            if ((keys["KeyS"] || keys["ArrowDown"]) && player.y < canvas.height - player.size) player.y += player.speed;
            if ((keys["KeyA"] || keys["ArrowLeft"]) && player.x > 0) player.x -= player.speed;
            if ((keys["KeyD"] || keys["ArrowRight"]) && player.x < canvas.width - player.size) player.x += player.speed;
        
            // Reset interaction flag
            npcs.forEach(npc => npc.canInteract = false);
        }}
    }}

    // Pokémon-style generic character drawing
    function drawCharacter(ctx, x, y, size, color, facing, isPlayer=false, name='') {{
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x + size/2, y + size/2, size/2, 0, Math.PI * 2);
        ctx.fill();
        
        // Dynamic generic sprite parts (eyes, directional indicator)
        ctx.fillStyle = isPlayer ? "white" : "black"; 
        let eyeSize = size * 0.15;
        let eyeOffset = size * 0.25;
        
        // Generic eyes
        ctx.beginPath();
        if (facing === 'down') {{
            ctx.arc(x + size/2 - eyeOffset, y + size/2, eyeSize, 0, Math.PI * 2);
            ctx.arc(x + size/2 + eyeOffset, y + size/2, eyeSize, 0, Math.PI * 2);
        }} else if (facing === 'up') {{
             ctx.arc(x + size/2 - eyeOffset, y + size/2 - eyeOffset/2, eyeSize/1.5, 0, Math.PI * 2);
             ctx.arc(x + size/2 + eyeOffset, y + size/2 - eyeOffset/2, eyeSize/1.5, 0, Math.PI * 2);
        }} else if (facing === 'left') {{
             ctx.arc(x + size/2 - eyeOffset, y + size/2, eyeSize, 0, Math.PI * 2);
        }} else if (facing === 'right') {{
             ctx.arc(x + size/2 + eyeOffset, y + size/2, eyeSize, 0, Math.PI * 2);
        }}
        ctx.fill();
        
        // Name label
        if(name) {{
            ctx.fillStyle = "white"; ctx.font = "bold 14px 'Courier New'"; ctx.textAlign = "center";
            ctx.fillText(name, x + size/2, y - 10);
        }} else if (isPlayer) {{
            ctx.fillStyle = player.color; ctx.font = "bold 14px 'Courier New'"; ctx.textAlign = "center";
            ctx.fillText("Shanaya", x + size/2, y - 10);
        }}
    }}

    function draw() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. Draw Base Rooms (Styled generic textures/colors)
        ctx.fillStyle = "#3e2723"; ctx.fillRect(0, 0, 250, 250); // Kitchen (Brown)
        ctx.fillStyle = "#1a237e"; ctx.fillRect(550, 0, 250, 250); // Library (Dark Blue)
        ctx.fillStyle = "#1b5e20"; ctx.fillRect(0, 250, 250, 250); // Garden (Green)
        ctx.fillStyle = "#4a148c"; ctx.fillRect(550, 250, 250, 250); // Study (Purple)
        ctx.fillStyle = "#795548"; ctx.fillRect(250, 0, 300, 500); // Grand Hall (Lighter Brown)

        // Grand Hall Compass design
        ctx.fillStyle = "rgba(255, 255, 255, 0.05)";
        ctx.beginPath(); ctx.arc(400, 250, 100, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = "rgba(255, 255, 255, 0.1)"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(400, 150); ctx.lineTo(400, 350); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(300, 250); ctx.lineTo(500, 250); ctx.stroke();


        // Room Labels
        ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 28px 'Courier New'"; ctx.textAlign = "center";
        ctx.fillText("KITCHEN", 125, 135);
        ctx.fillText("LIBRARY", 675, 135);
        ctx.fillText("GARDEN", 125, 385);
        ctx.fillText("STUDY", 675, 385);
        ctx.fillStyle = "rgba(0,0,0,0.3)"; ctx.font = "bold 32px 'Courier New'";
        ctx.fillText("GRAND HALL", 400, 260);

        // 2. Lighting System (Draw Darkness)
        let activeRoom = getCurrentRoom(player.x, player.y);
        ctx.fillStyle = "rgba(0, 0, 0, 0.98)"; // Very dark overlay
        
        if (activeRoom !== "Kitchen") ctx.fillRect(0, 0, 250, 250);
        if (activeRoom !== "Library") ctx.fillRect(550, 0, 250, 250);
        if (activeRoom !== "Garden") ctx.fillRect(0, 250, 250, 250);
        if (activeRoom !== "Study") ctx.fillRect(550, 250, 250, 250);

        // 3. Draw NPCs (Only if in visible room, or if NPC is in the Hall)
        ctx.textAlign = "left";
        npcs.forEach(npc => {{
            let npcRoom = getCurrentRoom(npc.x, npc.y);
            if (npcRoom === activeRoom || npcRoom === "Grand Hall") {{
                drawCharacter(ctx, npc.x, npc.y, npc.size, npc.color, 'down', false, npc.name);
                
                // Interaction Cue (!)
                if(npc.canInteract) {{
                    ctx.fillStyle = "#ffeb3b"; ctx.font = "bold 30px 'Courier New'"; ctx.textAlign = "center";
                    ctx.fillText("!", npc.x + npc.size/2, npc.y - 35);
                }}
            }}
        }});

        // 4. Draw Player (Shanaya)
        drawCharacter(ctx, player.x, player.y, player.size, player.color, player.facing, true);
    }}

    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}

    // --- INTERACTION ---
    function checkInteraction() {{
        if (modalOpen || padOpen) return;
        let closestNpc = null;
        let minDistance = Infinity;

        npcs.forEach(npc => {{
            let dx = (player.x + player.size/2) - (npc.x + npc.size/2);
            let dy = (player.y + player.size/2) - (npc.y + npc.size/2);
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 55) {{
                npc.canInteract = true; // Mark as interactable this frame
                if (distance < minDistance) {{
                    minDistance = distance;
                    closestNpc = npc;
                }}
            }}
        }});

        if (closestNpc) {{
            document.getElementById("npc-name").innerText = closestNpc.name;
            document.getElementById("npc-clue").innerText = closestNpc.clue;
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="250" src="${{closestNpc.video}}?autoplay=1" frameborder="0" allowfullscreen allow='autoplay'></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true;
        }}
    }}

    window.closeModal = function() {{
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = ""; // Stop video/audio
        setTimeout(() => {{ modalOpen = false; }}, 200);
    }}

    // --- CLUE PAD OVERLAY FUNCTIONS ---
    window.toggleCluePad = function() {{
        if(modalOpen) return;
        padOpen = !padOpen;
        const pad = document.getElementById("clue-pad-overlay");
        pad.style.display = padOpen ? "block" : "none";
        
        if(padOpen) {{
            renderCluePadContent();
            // Pause player movement while pad is open (handled in update())
        }} else {{
            // Custom cursor already hidden over pad by default mouse behavior, ensure hidden when closing via 'C'
            cursor.style.display = 'none';
        }}
    }}

    function renderCluePadContent() {{
        const content = document.getElementById("clue-content");
        content.innerHTML = ''; // Clear previous content

        // Render Categories
        renderCategory(content, "Suspects", suspects.map(s => s.name), 'suspects');
        renderCategory(content, "Weapons", weapons, 'weapons');
        renderCategory(content, "Rooms", rooms, 'rooms');
    }}

    function renderCategory(container, title, items, dataKey) {{
        const catDiv = document.createElement('div');
        catDiv.className = 'clue-category';
        catDiv.innerHTML = `<h3>${{title}}</h3>`;
        
        items.forEach(item => {{
            const itemDiv = document.createElement('div');
            itemDiv.className = 'clue-item';
            
            const nameSpan = document.createElement('span');
            nameSpan.className = 'clue-name';
            nameSpan.innerText = item;
            itemDiv.appendChild(nameSpan);

            const buttonsDiv = document.createElement('div');
            buttonsDiv.className = 'clue-status-buttons';
            
            // Generic Status Buttons (Possible, Ruled Out, Answer)
            renderStatusButton(buttonsDiv, '🤔', 'possible', item, dataKey);
            renderStatusButton(buttonsDiv, '❌', 'ruled-out', item, dataKey);
            renderStatusButton(buttonsDiv, '🎯', 'answer', item, dataKey);
            
            itemDiv.appendChild(buttonsDiv);
            catDiv.appendChild(itemDiv);
        }});
        container.appendChild(catDiv);
    }}

    function renderStatusButton(container, label, statusKey, itemName, dataKey) {{
        const btn = document.createElement('button');
        btn.className = `status-btn ${{statusKey}}`;
        btn.innerText = label;
        if(cluePadData[dataKey][itemName] === statusKey) btn.classList.add('active');
        
        btn.onclick = () => {{
            // Toggle status - if already active, set to 'none'
            if(cluePadData[dataKey][itemName] === statusKey) {{
                cluePadData[dataKey][itemName] = 'none';
                btn.classList.remove('active');
            }} else {{
                // Deactivate other buttons for this item
                const siblingBtns = container.querySelectorAll('.status-btn');
                siblingBtns.forEach(sb => sb.classList.remove('active'));
                
                cluePadData[dataKey][itemName] = statusKey;
                btn.classList.add('active');
            }}
            // Data is kept in cluePadData for now, not saved persistently beyond game session
        }};
        container.appendChild(btn);
    }}

    loop();
</script>
</body>
</html>
"""

# Embed the dynamic game component with appropriate height
components.html(game_html, height=700)

st.divider()

# --- 4. THE FINAL ACCUSATION (Streamlit side) ---
st.markdown("<h2 style='text-align: center; color: #fdd835; margin-bottom: 20px;'>⚖️ Final Accusation</h2>", unsafe_allow_html=True)
st.write("Ready to crack the case, Shanaya? Select the guilty party, location, and weapon!")

col1, col2, col3 = st.columns(3)
with col1:
    guess_who = st.selectbox("Suspect", ["Select"] + [s["name"] for s in suspects])
with col2:
    guess_where = st.selectbox("Location", ["Select"] + rooms)
with col3:
    guess_weapon = st.selectbox("Weapon", ["Select"] + weapons)
    
if st.button("Submit Final Accusation", use_container_width=True, type="primary"):
    # Define the correct answer logic here
    if guess_who == "Rahul" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 CONGRATULATIONS, SHANAYA! You solved the mystery of the dark mansion! 🎉")
        st.balloons()
        st.markdown("<h3 style='text-align: center; color: #fff;'>Happy Birthday! You are truly the best detective! 🎂🎁</h3>", unsafe_allow_html=True)
    elif guess_who == "Select" or guess_where == "Select" or guess_weapon == "Select":
        st.warning("Please select a valid Suspect, Location, and Weapon.")
    else:
        st.error("Not quite right, Detective. Check your clues, use your pad, and try again!")
