import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. PAGE SETUP & MODERN TYPOGRAPHY ---
st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

# Inject Google Fonts and professional dark-theme UI styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Montserrat:wght@300;400;600&display=swap');
    
    .main .block-container { padding-top: 2rem; max-width: 1100px; }
    h1 {
        font-family: 'Cinzel', serif;
        text-align: center;
        color: #f5c518;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 5px !important;
    }
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        color: #b3b3b3;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 25px;
    }
    .instruction-bar {
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        color: #8c8c8c;
        font-size: 0.85rem;
        background: #1a1a1a;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #2d2d2d;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>THE MANSION MYSTERY</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A Personalized Birthday Investigation for Shanaya</div>", unsafe_allow_html=True)
st.markdown("<div class='instruction-bar'>🎮 <b>Controls:</b> Move with <b>WASD</b> or <b>Arrow Keys</b> | Interrogate suspects with <b>Spacebar</b> | Toggle Case File with <b>C</b></div>", unsafe_allow_html=True)

# --- 2. GAME DATA SYSTEM ---
suspects = [
    {"name": "Rahul", "clue": "The murderer has a sweet tooth.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#e50914"},
    {"name": "Aditi", "clue": "I saw someone carrying a heavy brass candlestick into the west wing earlier.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#b81d24"},
    {"name": "Karan", "clue": "The crime definitely happened indoors. The garden grass was completely untouched.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#f5c518"},
    {"name": "Prof. Aris", "clue": "I heard a loud, heavy thud coming straight from the Kitchen floor around midnight.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#008080"},
    {"name": "Mme. Elara", "clue": "I found a strange, sweet crystalline residue wiped near the pantry entrance.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#e5007d"}
]
weapons = ["Candlestick", "Poison", "Rope", "Axe", "Dagger"]
rooms = ["Kitchen", "Library", "Garden", "Study", "Grand Hall"]

suspects_json = json.dumps(suspects)
weapons_json = json.dumps(weapons)
rooms_json = json.dumps(rooms)

# --- 3. THE NEXT-GEN JAVASCRIPT GAME ENGINE ---
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ 
        margin: 0; 
        display: flex; 
        justify-content: center; 
        background-color: #0f0f11; 
        color: #ffffff; 
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
    }}
    #wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 920px;
        position: relative;
    }}
    canvas {{ 
        border: 3px solid #2d2d35; 
        border-radius: 12px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.8);
    }}
    
    /* Modern Dialogue Cinematic Box */
    #dialogue-box {{
        display: none;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: #16161a;
        color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border: 2px solid #f5c518;
        box-shadow: 0px 15px 60px rgba(0,0,0,0.9);
        text-align: center;
        width: 85%; max-width: 550px;
        z-index: 20;
    }}
    #dialogue-box h2 {{ 
        font-family: 'Cinzel', serif; 
        margin-top: 0; 
        color: #f5c518; 
        letter-spacing: 1px;
    }}
    #dialogue-box p {{ font-size: 16px; color: #dcdcdc; line-height: 1.6; margin: 15px 0; }}
    #video-container {{ border-radius: 8px; overflow: hidden; border: 1px solid #333; background: #000; }}
    
    .action-btn {{ 
        background: #f5c518; color: #111; border: none; 
        padding: 12px 28px; font-size: 14px; border-radius: 6px; 
        cursor: pointer; font-weight: 600; font-family: 'Montserrat', sans-serif;
        text-transform: uppercase; letter-spacing: 1px; transition: all 0.2s;
    }}
    .action-btn:hover {{ background: #dfb210; transform: scale(1.02); }}

    /* Integrated Case File / Detective Pad */
    #clue-pad-overlay {{
        display: none;
        position: absolute;
        top: 15px; left: 15px;
        width: calc(100% - 30px); height: calc(100% - 30px);
        background: rgba(20, 20, 25, 0.98);
        border-radius: 12px;
        border: 2px solid #3d3d4d;
        box-shadow: 0px 0px 50px rgba(0,0,0,0.95);
        z-index: 30;
        padding: 30px;
        box-sizing: border-box;
        overflow-y: auto;
    }}
    #clue-pad-overlay h2 {{ font-family: 'Cinzel', serif; text-align: center; color: #f5c518; margin-top: 0; }}
    .grid-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 10px; }}
    .category-column h3 {{ font-family: 'Cinzel', serif; color: #aeaeae; border-bottom: 1px solid #333; padding-bottom: 8px; margin-bottom: 12px; }}
    .pad-row {{ display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1f1f24; }}
    .pad-label {{ font-size: 14px; font-weight: 400; color: #e0e0e0; }}
    .toggle-cycle {{
        background: #222227; color: #888; border: 1px solid #444;
        width: 36px; height: 32px; border-radius: 4px; cursor: pointer;
        font-size: 14px; font-weight: bold; display: flex; align-items: center; justify-content: center;
    }}
    .toggle-cycle.active-x {{ color: #ff4b4b; border-color: #ff4b4b; background: rgba(255,75,75,0.05); }}
    .toggle-cycle.active-check {{ color: #00cc66; border-color: #00cc66; background: rgba(0,204,102,0.05); }}

    #bottom-controls {{ margin-top: 15px; display: flex; justify-content: center; }}
    .pad-trigger {{ background: #1f1f26; color: #ccc; border: 1px solid #3a3a45; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; font-family: 'Montserrat', sans-serif; }}
    .pad-trigger:hover {{ color: #fff; border-color: #f5c518; }}
</style>
</head>
<body>

<div id="wrapper">
    <div style="position: relative;">
        <canvas id="mansionCanvas" width="900" height="550"></canvas>
        
        <div id="dialogue-box">
            <h2 id="npc-name">Interrogation</h2>
            <div id="video-container"></div>
            <p id="npc-clue"></p>
            <button class="action-btn" onclick="closeModal()">Resume Search</button>
        </div>

        <div id="clue-pad-overlay">
            <h2>📋 DETECTIVE CASE FILE</h2>
            <p style="text-align:center; color:#777; font-size:12px; margin-top:-10px;">Click the buttons to cycle statuses: Blank ➔ ❌ Ruled Out ➔  Guilty</p>
            <div class="grid-container" id="clue-grid">
                <div class="category-column" id="col-suspects"><h3>Suspects</h3></div>
                <div class="category-column" id="col-weapons"><h3>Weapons</h3></div>
                <div class="category-column" id="col-rooms"><h3>Rooms</h3></div>
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <button class="action-btn" onclick="toggleCluePad()">Return to Mansion (C)</button>
            </div>
        </div>
    </div>
    
    <div id="bottom-controls">
        <button class="pad-trigger" onclick="toggleCluePad()">📋 Open Case File (C)</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("mansionCanvas");
    const ctx = canvas.getContext("2d");

    // --- GAME ENGINE DATABASES ---
    const suspectsData = {suspects_json};
    const weaponsData = {weapons_json};
    const roomsData = {rooms_json};

    const player = {{ x: 450, y: 275, r: 12, speed: 5, color: "#00d2ff" }};
    
    // Suspect spatial positioning matching the interior room layouts
    const npcs = [
        {{ name: "Rahul", x: 120, y: 110, r: 12, color: suspectsData[0].color, clue: suspectsData[0].clue, video: suspectsData[0].video, near: false }},
        {{ name: "Aditi", x: 780, y: 110, r: 12, color: suspectsData[1].color, clue: suspectsData[1].clue, video: suspectsData[1].video, near: false }},
        {{ name: "Karan", x: 120, y: 440, r: 12, color: suspectsData[2].color, clue: suspectsData[2].clue, video: suspectsData[2].video, near: false }},
        {{ name: "Prof. Aris", x: 780, y: 440, r: 12, color: suspectsData[3].color, clue: suspectsData[3].clue, video: suspectsData[3].video, near: false }},
        {{ name: "Mme. Elara", x: 450, y: 90, r: 12, color: suspectsData[4].color, clue: suspectsData[4].clue, video: suspectsData[4].video, near: false }}
    ];

    let keys = {{}};
    let modalOpen = false;
    let padOpen = false;
    let padMemory = {{}};

    // --- ARCHITECTURAL WALL BOUNDARIES (Collision Mapping) ---
    // Houses layout bounds. Hard blocks to force walking through real doors.
    const walls = [
        // Perimeter Outer Walls
        {{ x1: 30, y1: 30, x2: 870, y2: 30 }},
        {{ x1: 870, y1: 30, x2: 870, y2: 520 }},
        {{ x1: 870, y1: 520, x2: 30, y2: 520 }},
        {{ x1: 30, y1: 520, x2: 30, y2: 30 }},
        
        // West Wing Internal Divider (with Kitchen door at 100-170, Garden door at 380-450)
        {{ x1: 280, y1: 30, x2: 280, y2: 100 }},
        {{ x1: 280, y1: 170, x2: 280, y2: 380 }},
        {{ x1: 280, y1: 450, x2: 280, y2: 520 }},

        // East Wing Internal Divider (with Library door at 100-170, Study door at 380-450)
        {{ x1: 620, y1: 30, x2: 620, y2: 100 }},
        {{ x1: 620, y1: 170, x2: 620, y2: 380 }},
        {{ x1: 620, y1: 450, x2: 620, y2: 520 }},

        // Horizontal Room Dividers
        {{ x1: 30, y1: 240, x2: 280, y2: 240 }},  // Kitchen floor baseline
        {{ x1: 30, y1: 310, x2: 280, y2: 310 }},  // Garden floor top-line
        {{ x1: 620, y1: 240, x2: 870, y2: 240 }}, // Library floor baseline
        {{ x1: 620, y1: 310, x2: 870, y2: 310 }}  // Study floor top-line
    ];

    // --- KEYBOARD LISTNERS ---
    window.addEventListener("keydown", (e) => {{
        keys[e.code] = true;
        if (e.code === "Space" && !modalOpen && !padOpen) {{ checkInterrogation(); e.preventDefault(); }}
        if (e.code === "KeyC") {{ toggleCluePad(); e.preventDefault(); }}
        if (["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space","KeyW","KeyA","KeyS","KeyD"].includes(e.code)) e.preventDefault();
    }});
    window.addEventListener("keyup", (e) => {{ keys[e.code] = false; }});

    // --- SPATIAL ROOM TRACKER ---
    function checkCurrentRoom(x, y) {{
        if (x < 280 && y < 240) return "Kitchen";
        if (x > 620 && y < 240) return "Library";
        if (x < 280 && y > 310) return "Garden";
        if (x > 620 && y > 310) return "Study";
        return "Grand Hall";
    }}

    // --- MATHEMATICAL COLLISION SOLVER ---
    function distanceToLineSegment(px, py, x1, y1, x2, y2) {{
        let A = px - x1; let B = py - y1; let C = x2 - x1; let D = y2 - y1;
        let dot = A * C + B * D; let len_sq = C * C + D * D;
        let param = -1;
        if (len_sq != 0) param = dot / len_sq;
        let xx, yy;
        if (param < 0) {{ xx = x1; yy = y1; }}
        else if (param > 1) {{ xx = x2; yy = y2; }}
        else {{ xx = x1 + param * C; yy = y2 + param * D; }}
        let dx = px - xx; let dy = py - yy;
        return Math.sqrt(dx * dx + dy * dy);
    }}

    function canMoveTo(nx, ny) {{
        // Canvas edge check
        if (nx - player.r < 30 || nx + player.r > 870 || ny - player.r < 30 || ny + player.r > 520) return false;
        // Architectural wall check
        for (let wall of walls) {{
            if (distanceToLineSegment(nx, ny, wall.x1, wall.y1, wall.x2, wall.wall2 || wall.y2) < player.r + 2) {{
                return false;
            }}
        }}
        return true;
    }}

    // --- GAME ENGINE PROCESSORS ---
    function update() {{
        if (modalOpen || padOpen) return;
        
        let dx = 0; let dy = 0;
        if (keys["KeyW"] || keys["ArrowUp"]) dy = -player.speed;
        if (keys["KeyS"] || keys["ArrowDown"]) dy = player.speed;
        if (keys["KeyA"] || keys["ArrowLeft"]) dx = -player.speed;
        if (keys["KeyD"] || keys["ArrowRight"]) dx = player.speed;

        if (dx !== 0 && dy !== 0) {{ dx *= 0.7071; dy *= 0.7071; }} // Normalize diagonal speeds

        if (dx !== 0 && canMoveTo(player.x + dx, player.y)) player.x += dx;
        if (dy !== 0 && canMoveTo(player.x, player.y + dy)) player.y += dy;

        // Reset indicators
        npcs.forEach(npc => npc.near = false);
        npcs.forEach(npc => {{
            let dist = Math.sqrt((player.x - npc.x)**2 + (player.y - npc.y)**2);
            if (dist < 45) npc.near = true;
        }});
    }}

    // --- FURNITURE ARCHITECT DRAWING SYSTEM ---
    function drawFurniture() {{
        ctx.lineWidth = 1.5;
        
        // --- KITCHEN FURNITURE ---
        ctx.strokeStyle = "rgba(184, 134, 11, 0.4)"; // Soft wood outlines
        ctx.strokeRect(50, 50, 60, 100); // Grand Banquet Dining Table
        ctx.fillStyle = "rgba(255,255,255,0.05)"; ctx.fillRect(50,50,60,100);
        ctx.strokeRect(200, 50, 50, 40); // Kitchen Island Countertop
        
        // --- LIBRARY FURNITURE ---
        ctx.strokeStyle = "rgba(70, 130, 180, 0.4)";
        ctx.strokeRect(650, 50, 180, 15); // Bookshelf North Row
        ctx.strokeRect(840, 70, 15, 120); // Bookshelf East Row
        // Cozy Fireplace and Armchair vector outlines
        ctx.beginPath(); ctx.arc(740, 140, 15, 0, Math.PI*2); ctx.stroke(); // Reading Rug
        
        // --- GARDEN ELEMENTS ---
        ctx.strokeStyle = "rgba(46, 139, 87, 0.4)";
        ctx.beginPath(); ctx.arc(140, 420, 25, 0, Math.PI*2); ctx.stroke(); // Central Stone Fountain
        ctx.strokeRect(50, 460, 40, 15); // Wooden Park Bench 1
        
        // --- STUDY FURNITURE ---
        ctx.strokeStyle = "rgba(153, 50, 204, 0.4)";
        ctx.strokeRect(700, 420, 90, 45); // Heavy Executive Mahogany Desk
        ctx.fillStyle = "rgba(255,255,255,0.03)"; ctx.fillRect(700,420,90,45);
        ctx.strokeRect(810, 360, 35, 35); // Metal Document Safe
        
        // --- GRAND HALL ART PIECES ---
        ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        ctx.strokeRect(360, 220, 280, 60); // Elegant Long Red Welcoming Carpet
        ctx.fillStyle = "rgba(255, 0, 0, 0.02)"; ctx.fillRect(360, 220, 280, 60);
        ctx.strokeRect(330, 60, 50, 40); // Grand Piano Wing
    }}

    function draw() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. Draw Architectural Floor Mapping Blueprint Background
        ctx.fillStyle = "#13131a"; ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 2. Draw Furniture Outlines underneath shadows
        drawFurniture();

        // 3. Draw Room Hard Architectural Borders Always Visible (Architectural Style)
        ctx.strokeStyle = "#2f2f3d"; ctx.lineWidth = 3;
        walls.forEach(w => {{
            ctx.beginPath(); ctx.moveTo(w.x1, w.y1); ctx.lineTo(w.x2, w.y2); ctx.stroke();
        }});

        // Draw Door Openings explicitly visually mapped
        ctx.strokeStyle = "#13131a"; ctx.lineWidth = 5;
        ctx.beginPath(); ctx.moveTo(280, 102); ctx.lineTo(280, 168); ctx.stroke(); // Kitchen Doorway
        ctx.beginPath(); ctx.moveTo(280, 382); ctx.lineTo(280, 448); ctx.stroke(); // Garden Doorway
        ctx.beginPath(); ctx.moveTo(620, 102); ctx.lineTo(620, 168); ctx.stroke(); // Library Doorway
        ctx.beginPath(); ctx.moveTo(620, 382); ctx.lineTo(620, 448); ctx.stroke(); // Study Doorway

        // 4. Room Typography Mapping Always Visibly Emplaced
        ctx.fillStyle = "rgba(255, 255, 255, 0.18)"; ctx.font = "bold 16px 'Cinzel'"; ctx.textAlign = "center";
        ctx.fillText("KITCHEN", 150, 140);
        ctx.fillText("LIBRARY", 750, 140);
        ctx.fillText("GARDEN PARLOR", 150, 400);
        ctx.fillText("THE STUDY", 750, 400);
        ctx.fillStyle = "rgba(255, 255, 255, 0.1)"; ctx.font = "bold 20px 'Cinzel'";
        ctx.fillText("GRAND HALL", 450, 280);

        let activeRoom = checkCurrentRoom(player.x, player.y);

        // 5. Advanced Selective Fog-of-War Real-Time Rendering Engine
        ctx.fillStyle = "rgba(7, 7, 10, 0.92)"; // Clean, smooth dark shroud overlay
        if (activeRoom !== "Kitchen") ctx.fillRect(32, 32, 246, 206);
        if (activeRoom !== "Library") ctx.fillRect(622, 32, 246, 206);
        if (activeRoom !== "Garden") ctx.fillRect(32, 312, 246, 206);
        if (activeRoom !== "Study") ctx.fillRect(622, 312, 246, 206);

        // 6. Draw Characters (Only if uncovered by lights or in Hallway)
        npcs.forEach(npc => {{
            let npcRoom = checkCurrentRoom(npc.x, npc.y);
            if (npcRoom === activeRoom || npcRoom === "Grand Hall") {{
                // Render suspect base body
                ctx.fillStyle = npc.color; ctx.beginPath(); ctx.arc(npc.x, npc.y, npc.r, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5; ctx.stroke();
                
                // Suspect Text Label styling
                ctx.fillStyle = "#ffffff"; ctx.font = "600 11px 'Montserrat'"; ctx.textAlign = "center";
                ctx.fillText(npc.name, npc.x, npc.y - 18);

                // Pokémon style Interactivity Prompt (!)
                if (npc.near) {{
                    ctx.fillStyle = "#f5c518"; ctx.font = "900 18px 'Montserrat'";
                    ctx.fillText("!", npc.x, npc.y - 32);
                }}
            }}
        }});

        // 7. Render Player (Shanaya)
        ctx.fillStyle = player.color; ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.stroke();
        // Inner core graphic
        ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(player.x, player.y, player.r/2, 0, Math.PI*2); ctx.fill();
        
        ctx.fillStyle = "#00d2ff"; ctx.font = "600 12px 'Montserrat'"; ctx.textAlign = "center";
        ctx.fillText("Shanaya", player.x, player.y - 18);
    }}

    function runEngine() {{ update(); draw(); requestAnimationFrame(runEngine); }}

    // --- INTERROGATION POPUP MANAGER ---
    function checkInterrogation() {{
        let match = null;
        npcs.forEach(npc => {{
            let dist = Math.sqrt((player.x - npc.x)**2 + (player.y - npc.y)**2);
            if (dist < 45) match = npc;
        }});

        if (match) {{
            document.getElementById("npc-name").innerText = "Interrogating: " + match.name;
            document.getElementById("npc-clue").innerText = '"' + match.clue + '"';
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="280" src="${{match.video}}?autoplay=1" frameborder="0" allow='autoplay; encrypted-media' allowfullscreen></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true;
        }}
    }}

    window.closeModal = function() {{
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = ""; // Hard breaks the audio track
        setTimeout(() => {{ modalOpen = false; }}, 200);
    }}

    // --- INTEGRATED CASE FILE LOGIC ---
    window.toggleCluePad = function() {{
        if (modalOpen) return;
        padOpen = !padOpen;
        document.getElementById("clue-pad-overlay").style.display = padOpen ? "block" : "none";
    }}

    function buildCaseFileLayout() {{
        populateColumn("col-suspects", suspectsData.map(s => s.name), 's');
        populateColumn("col-weapons", weaponsData, 'w');
        populateColumn("col-rooms", roomsData, 'r');
    }}

    function populateColumn(elementId, dataset, keyPrefix) {{
        const target = document.getElementById(elementId);
        dataset.forEach(item => {{
            let uniqueId = keyPrefix + "_" + item.replace(/\s+/g, '');
            padMemory[uniqueId] = 0; // Default state

            let row = document.createElement("div");
            row.className = "pad-row";
            row.innerHTML = `<span class="pad-label">${{item}}</span>
                             <button class="toggle-cycle" id="${{uniqueId}}" onclick="cycleState('${{uniqueId}}')"></button>`;
            target.appendChild(row);
        }});
    }}

    window.cycleState = function(id) {{
        // States: 0 = None, 1 = X (Ruled Out), 2 = Check (Guilty Option)
        padMemory[id] = (padMemory[id] + 1) % 3;
        let btn = document.getElementById(id);
        if (padMemory[id] === 0) {{ btn.innerText = ""; btn.className = "toggle-cycle"; }}
        if (padMemory[id] === 1) {{ btn.innerText = "❌"; btn.className = "toggle-cycle active-x"; }}
        if (padMemory[id] === 2) {{ btn.innerText = "✓"; btn.className = "toggle-cycle active-check"; }}
    }}

    // Boot execution systems
    buildCaseFileLayout();
    runEngine();
</script>
</body>
</html>
"""

components.html(game_html, height=600)

st.divider()

# --- 4. THE ULTIMATE ACCUSATION SCREEN ---
st.markdown("<h2 style='text-align: center; font-family: \"Cinzel\", serif; color: #fdd835; margin-bottom: 25px;'>⚖️ SUBMIT MANSION VERDICT</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    guess_who = st.selectbox("Identify the Killer", ["Select Suspect"] + [s["name"] for s in suspects])
with col2:
    guess_where = st.selectbox("Identify the Crime Scene", ["Select Location"] + rooms)
with col3:
    guess_weapon = st.selectbox("Identify the Murder Weapon", ["Select Weapon"] + weapons)
    
if st.button("EXECUTE ARREST WARRANT", use_container_width=True, type="primary"):
    if guess_who == "Rahul" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 CORE VERDICT VALIDATED! You completely unraveled the mystery of the dark mansion! 🎉")
        st.balloons()
        st.markdown("<h3 style='text-align: center; font-family: \"Cinzel\", serif; color: #fff;'>Happy Birthday Shanaya! Your prize awaits! 🎂🎁</h3>", unsafe_allow_html=True)
    elif guess_who == "Select Suspect" or guess_where == "Select Location" or guess_weapon == "Select Weapon":
        st.warning("Please make sure all three fields of the arrest warrant are filled out.")
    else:
        st.error("Warrant Denied! Your current hypothesis contains flaws. Keep analyzing the crime scenes, Detective.")
