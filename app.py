import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;700;900&display=swap');
    .main .block-container { padding-top: 1rem; max-width: 1200px; }
    h1 { font-family: 'Nunito', sans-serif; text-align: center; color: #fdd835; font-weight: 900; margin-bottom: 0px;}
    .instruction { text-align: center; color: #aaa; font-family: 'Nunito', sans-serif; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🕵️‍♀️ SHANAYA'S MYSTERY</h1>", unsafe_allow_html=True)
st.markdown("<div class='instruction'><b>WASD/Arrows</b> to explore | <b>Spacebar</b> to talk | <b>C</b> for Case File</div>", unsafe_allow_html=True)

# --- GAME DATA ---
suspects = [
    {"name": "Rahul", "clue": "The murderer has a sweet tooth.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#e50914", "avatar": "🧑🏻‍🍳"},
    {"name": "Aditi", "clue": "I saw someone carrying a candlestick into the west wing.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#9c27b0", "avatar": "👩🏽‍💼"},
    {"name": "Karan", "clue": "The crime happened indoors. The garden was empty.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#f5c518", "avatar": "🧍🏽‍♂️"},
    {"name": "Prof. Aris", "clue": "I heard a loud thud coming from the Kitchen.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#008080", "avatar": "🧙🏼‍♂️"},
    {"name": "Mme. Elara", "clue": "I found a strange liquid near the Garden gate.", "video": "https://www.youtube.com/embed/dQw4w9WgXcQ", "color": "#e5007d", "avatar": "🧝🏼‍♀️"}
]
weapons = ["Candlestick", "Poison", "Rope", "Axe", "Dagger"]
rooms = ["Kitchen", "Library", "Garden", "Study", "Grand Hall"]

# --- THE RPG ENGINE (HTML/JS) ---
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; background: #111; color: white; font-family: 'Nunito', sans-serif; overflow: hidden; display: flex; justify-content: center; }}
    #game-container {{ position: relative; width: 900px; height: 600px; border: 4px solid #333; border-radius: 12px; box-shadow: 0px 10px 30px rgba(0,0,0,0.8); overflow: hidden; background: #2d4a22; }}
    canvas {{ display: block; }}
    
    /* UI Overlays */
    #dialogue-box {{
        display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background: #1e1e24; border: 3px solid #fdd835; border-radius: 12px; padding: 25px;
        text-align: center; width: 80%; z-index: 100; box-shadow: 0px 20px 50px rgba(0,0,0,0.9);
    }}
    #dialogue-box h2 {{ color: #fdd835; margin-top: 0; }}
    .btn {{ background: #fdd835; color: #111; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 16px; margin-top: 15px; }}
    .btn:hover {{ background: #fff176; }}

    #clue-pad-overlay {{
        display: none; position: absolute; top: 20px; left: 20px; width: calc(100% - 40px); height: calc(100% - 40px);
        background: rgba(20, 20, 25, 0.95); border: 2px solid #555; border-radius: 12px; padding: 20px; z-index: 90; box-sizing: border-box; overflow-y: auto;
    }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
    .pad-row {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; padding: 5px 0; }}
    .toggle-cycle {{ background: #222; border: 1px solid #444; color: white; width: 35px; height: 30px; border-radius: 4px; cursor: pointer; font-weight: bold; }}
    .toggle-cycle.x {{ background: rgba(255,0,0,0.2); border-color: red; color: red; }}
    .toggle-cycle.check {{ background: rgba(0,255,0,0.2); border-color: lime; color: lime; }}
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="900" height="600"></canvas>
    
    <div id="dialogue-box">
        <h2 id="npc-name">Name</h2>
        <div id="video-container" style="border-radius: 8px; overflow: hidden;"></div>
        <p id="npc-clue" style="font-size: 18px; color: #eee;"></p>
        <button class="btn" onclick="closeModal()">Close & Resume</button>
    </div>

    <div id="clue-pad-overlay">
        <h2 style="text-align: center; color: #4fc3f7; margin-top: 0;">📋 Detective Pad</h2>
        <div class="grid" id="clue-grid">
            <div id="col-suspects"><h3 style="color:#aaa;">Suspects</h3></div>
            <div id="col-weapons"><h3 style="color:#aaa;">Weapons</h3></div>
            <div id="col-rooms"><h3 style="color:#aaa;">Rooms</h3></div>
        </div>
        <div style="text-align: center; margin-top: 20px;"><button class="btn" onclick="togglePad()">Close Pad (C)</button></div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // --- MASSIVE MAP DIMENSIONS ---
    const MAP_W = 2000;
    const MAP_H = 2000;

    // --- GAME STATE ---
    const player = {{ x: 1000, y: 1500, w: 30, h: 40, speed: 6, avatar: "🕵️‍♀️" }};
    const keys = {{}};
    let modalOpen = false; let padOpen = false;

    // --- WORLD BUILDING (AABB Collision) ---
    // Instead of lines, we use solid blocks
    const walls = [];
    const furniture = [];
    
    // Mansion Walls
    const mansion = {{ x: 500, y: 400, w: 1000, h: 800 }};
    
    // Create physical walls around the mansion (with a gap for the front door and back door)
    walls.push({{x: 500, y: 400, w: 1000, h: 20}}); // Top wall
    walls.push({{x: 500, y: 1180, w: 450, h: 20}}); // Bottom left
    walls.push({{x: 1050, y: 1180, w: 450, h: 20}}); // Bottom right (Door is at 950-1050)
    walls.push({{x: 500, y: 400, w: 20, h: 800}}); // Left wall
    walls.push({{x: 1480, y: 400, w: 20, h: 800}}); // Right wall

    // Internal Walls
    walls.push({{x: 800, y: 400, w: 20, h: 350}}); // Kitchen Right wall
    walls.push({{x: 500, y: 750, w: 200, h: 20}}); // Kitchen Bottom wall (door gap)
    
    walls.push({{x: 1150, y: 400, w: 20, h: 350}}); // Library Left wall
    walls.push({{x: 1250, y: 750, w: 250, h: 20}}); // Library Bottom wall

    walls.push({{x: 800, y: 850, w: 20, h: 350}}); // Study Right wall
    walls.push({{x: 500, y: 850, w: 200, h: 20}}); // Study Top wall

    // Add Furniture (Solid objects with Emoji Sprites)
    function addProp(x, y, w, h, emoji, size) {{
        furniture.push({{x, y, w, h, emoji, size}});
    }}
    // Kitchen
    addProp(550, 450, 60, 60, "🧊", 50); // Fridge
    addProp(650, 550, 100, 60, "🍳", 50); // Stove/Island
    addProp(550, 650, 80, 80, "🪑", 40); // Dining table

    // Library
    addProp(1200, 450, 200, 40, "📚", 40); // Bookshelves
    addProp(1200, 500, 200, 40, "📚", 40); 
    addProp(1300, 650, 60, 60, "🛋️", 50); // Couch

    // Study
    addProp(550, 900, 100, 60, "💻", 50); // Desk
    addProp(600, 1000, 40, 40, "🪴", 40); // Plant

    // Grand Hall
    addProp(950, 600, 100, 150, "🎹", 80); // Piano

    // Garden (Outside)
    for(let i=0; i<15; i++) {{
        let tx = 200 + Math.random()*1600;
        let ty = 50 + Math.random()*300;
        addProp(tx, ty, 60, 60, "🌲", 80);
    }}
    addProp(900, 250, 150, 100, "⛲", 100); // Fountain

    // --- NPCs ---
    const npcs = [
        {{ name: "Rahul", x: 600, y: 600, w: 30, h: 40, data: {json.dumps(suspects[0])} }}, // Kitchen
        {{ name: "Aditi", x: 1350, y: 550, w: 30, h: 40, data: {json.dumps(suspects[1])} }}, // Library
        {{ name: "Karan", x: 1000, y: 300, w: 30, h: 40, data: {json.dumps(suspects[2])} }}, // Garden
        {{ name: "Prof. Aris", x: 700, y: 1000, w: 30, h: 40, data: {json.dumps(suspects[3])} }}, // Study
        {{ name: "Mme. Elara", x: 950, y: 800, w: 30, h: 40, data: {json.dumps(suspects[4])} }} // Hall
    ];

    // --- INPUT ---
    window.addEventListener("keydown", (e) => {{
        keys[e.code] = true;
        if(e.code === "Space" && !modalOpen && !padOpen) interact();
        if(e.code === "KeyC") togglePad();
        if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space"].includes(e.code)) e.preventDefault();
    }});
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    // --- COLLISION LOGIC ---
    function isColliding(rect1, rect2) {{
        return rect1.x < rect2.x + rect2.w && rect1.x + rect1.w > rect2.x &&
               rect1.y < rect2.y + rect2.h && rect1.y + rect1.h > rect2.y;
    }}

    function canMove(newX, newY) {{
        let pNext = {{ x: newX, y: newY, w: player.w, h: player.h }};
        
        // World Bounds
        if(newX < 0 || newX + player.w > MAP_W || newY < 0 || newY + player.h > MAP_H) return false;
        
        // Walls
        for(let w of walls) if(isColliding(pNext, w)) return false;
        // Furniture
        for(let f of furniture) if(isColliding(pNext, f)) return false;
        // NPCs
        for(let n of npcs) if(isColliding(pNext, n)) return false;

        return true;
    }}

    // --- ENGINE LOOP ---
    function update() {{
        if(modalOpen || padOpen) return;

        let dx = 0, dy = 0;
        if (keys["KeyW"] || keys["ArrowUp"]) dy = -player.speed;
        if (keys["KeyS"] || keys["ArrowDown"]) dy = player.speed;
        if (keys["KeyA"] || keys["ArrowLeft"]) dx = -player.speed;
        if (keys["KeyD"] || keys["ArrowRight"]) dx = player.speed;

        if (dx !== 0 && canMove(player.x + dx, player.y)) player.x += dx;
        if (dy !== 0 && canMove(player.x, player.y + dy)) player.y += dy;
        
        // Proximity check for interaction
        npcs.forEach(n => {{
            let dist = Math.hypot((player.x + player.w/2) - (n.x + n.w/2), (player.y + player.h/2) - (n.y + n.h/2));
            n.near = dist < 70;
        }});
    }}

    function draw() {{
        // 1. CLEAR & SETUP CAMERA
        ctx.fillStyle = "#2d4a22"; // Grass color outside
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.save();
        // The magic camera math: center the canvas on the player
        let camX = canvas.width/2 - (player.x + player.w/2);
        let camY = canvas.height/2 - (player.y + player.h/2);
        ctx.translate(camX, camY);

        // 2. DRAW OUTSIDE WORLD
        // Draw dirt path to door
        ctx.fillStyle = "#5c4033"; ctx.fillRect(900, 1180, 200, 800);
        ctx.fillStyle = "#5c4033"; ctx.fillRect(900, 300, 200, 100);

        // 3. DRAW MANSION FLOOR
        ctx.fillStyle = "#8b5a2b"; // Wood floor
        ctx.fillRect(mansion.x, mansion.y, mansion.w, mansion.h);
        
        // Draw Carpets
        ctx.fillStyle = "#800000"; ctx.fillRect(850, 450, 300, 700); // Hall carpet
        ctx.fillStyle = "#3e2723"; ctx.fillRect(520, 420, 260, 310); // Kitchen tile
        ctx.fillStyle = "#1a237e"; ctx.fillRect(1170, 420, 310, 310); // Library rug

        // 4. DRAW WALLS
        ctx.fillStyle = "#111";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));

        // 5. DRAW FURNITURE (USING EMOJIS AS SPRITES!)
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        furniture.forEach(f => {{
            ctx.font = f.size + "px Arial";
            ctx.fillText(f.emoji, f.x + f.w/2, f.y + f.h/2);
            // Debug box: ctx.strokeStyle="red"; ctx.strokeRect(f.x, f.y, f.w, f.h);
        }});

        // 6. ROOM LABELS
        ctx.fillStyle = "rgba(255,255,255,0.2)"; ctx.font = "bold 40px 'Nunito'";
        ctx.fillText("KITCHEN", 650, 600);
        ctx.fillText("LIBRARY", 1350, 600);
        ctx.fillText("GARDEN", 1000, 200);
        ctx.fillText("GRAND HALL", 1000, 800);

        // 7. DRAW NPCs
        npcs.forEach(n => {{
            ctx.font = "40px Arial";
            ctx.fillText(n.data.avatar, n.x + n.w/2, n.y + n.h/2);
            ctx.fillStyle = "white"; ctx.font = "bold 14px 'Nunito'";
            ctx.fillText(n.name, n.x + n.w/2, n.y - 15);
            
            if(n.near) {{
                ctx.fillStyle = "#fdd835"; ctx.font = "bold 24px Arial";
                ctx.fillText("💬", n.x + n.w/2, n.y - 35);
            }}
        }});

        // 8. DRAW PLAYER
        ctx.font = "40px Arial";
        ctx.fillText(player.avatar, player.x + player.w/2, player.y + player.h/2);
        ctx.fillStyle = "#00d2ff"; ctx.font = "bold 14px 'Nunito'";
        ctx.fillText("Shanaya", player.x + player.w/2, player.y - 15);

        // 9. ADVANCED FOG OF WAR (Lighting System)
        // Determine player room
        let pRoom = "Outside";
        if(player.x > 500 && player.x < 1500 && player.y > 400 && player.y < 1200) {{
            if(player.x < 800 && player.y < 750) pRoom = "Kitchen";
            else if(player.x > 1150 && player.y < 750) pRoom = "Library";
            else if(player.x < 800 && player.y > 850) pRoom = "Study";
            else pRoom = "Hall";
        }}

        // Draw shadow over mansion
        ctx.fillStyle = "rgba(0,0,0,0.92)";
        if(pRoom !== "Outside") {{
            ctx.globalCompositeOperation = 'source-over';
            ctx.fillRect(500, 400, 1000, 800); // Darken whole house
            
            // Punch a hole for the active room
            ctx.globalCompositeOperation = 'destination-out';
            ctx.fillStyle = "black";
            if(pRoom === "Kitchen") ctx.fillRect(500, 400, 300, 350);
            else if(pRoom === "Library") ctx.fillRect(1150, 400, 350, 350);
            else if(pRoom === "Study") ctx.fillRect(500, 850, 300, 350);
            else ctx.fillRect(800, 400, 350, 800); // Hall
            
            // Light aura around player
            let grd = ctx.createRadialGradient(player.x+15, player.y+20, 10, player.x+15, player.y+20, 150);
            grd.addColorStop(0, "rgba(0,0,0,1)"); grd.addColorStop(1, "rgba(0,0,0,0)");
            ctx.fillStyle = grd;
            ctx.beginPath(); ctx.arc(player.x+15, player.y+20, 150, 0, Math.PI*2); ctx.fill();
        }}
        ctx.globalCompositeOperation = 'source-over';

        ctx.restore(); // END CAMERA
    }}

    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}

    // --- INTERACTIONS ---
    function interact() {{
        let target = npcs.find(n => n.near);
        if(target) {{
            document.getElementById("npc-name").innerText = "Talking to " + target.name;
            document.getElementById("npc-clue").innerText = '"' + target.data.clue + '"';
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="250" src="${{target.data.video}}?autoplay=1" frameborder="0"></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true;
        }}
    }}

    window.closeModal = function() {{
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = ""; 
        setTimeout(() => modalOpen = false, 200);
    }}

    // --- CASE FILE LOGIC ---
    const padData = {{}};
    window.togglePad = function() {{
        if(modalOpen) return;
        padOpen = !padOpen;
        document.getElementById("clue-pad-overlay").style.display = padOpen ? "block" : "none";
    }}

    function initPad() {{
        const s = {json.dumps([s["name"] for s in suspects])};
        const w = {json.dumps(weapons)};
        const r = {json.dumps(rooms)};
        
        function buildCol(id, list, prefix) {{
            let col = document.getElementById(id);
            list.forEach(item => {{
                let uid = prefix + item.replace(/\s/g, '');
                padData[uid] = 0;
                col.innerHTML += `<div class='pad-row'><span>${{item}}</span><button id='${{uid}}' class='toggle-cycle' onclick='cycle("${{uid}}")'>-</button></div>`;
            }});
        }}
        buildCol("col-suspects", s, "s_"); buildCol("col-weapons", w, "w_"); buildCol("col-rooms", r, "r_");
    }}

    window.cycle = function(id) {{
        padData[id] = (padData[id] + 1) % 3;
        let b = document.getElementById(id);
        if(padData[id] === 0) {{ b.innerText = "-"; b.className = "toggle-cycle"; }}
        if(padData[id] === 1) {{ b.innerText = "❌"; b.className = "toggle-cycle x"; }}
        if(padData[id] === 2) {{ b.innerText = "✓"; b.className = "toggle-cycle check"; }}
    }}

    initPad();
    loop();
</script>
</body>
</html>
"""

components.html(game_html, height=650)

st.divider()

# --- THE ACCUSATION ---
col1, col2, col3 = st.columns(3)
with col1: guess_who = st.selectbox("Suspect", ["Select"] + [s["name"] for s in suspects])
with col2: guess_where = st.selectbox("Location", ["Select"] + rooms)
with col3: guess_weapon = st.selectbox("Weapon", ["Select"] + weapons)
    
if st.button("MAKE ACCUSATION", use_container_width=True, type="primary"):
    if guess_who == "Rahul" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 CORRECT! You cracked the case, Shanaya! Happy Birthday! 🎂")
        st.balloons()
    else:
        st.error("Not quite! Keep exploring the mansion.")
