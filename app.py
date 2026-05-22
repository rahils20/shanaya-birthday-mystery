import streamlit as st
import streamlit.components.v1 as components
import json
import random

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
st.markdown("<div class='instruction'><b>WASD/Arrows</b> to move | <b>Spacebar</b> to interact | <b>C</b> for Case File</div>", unsafe_allow_html=True)

# --- 1. GUEST LIST & NPC DATABASE ---
# All requested friends are here. I assigned specific clues to a few, and customized messages for others.
all_names = ["Mandira", "Selina", "Maanav", "Anoushka", "Shlokk", "Rahil", "Panthiv", "Samira", "Ishika", "Divya", "Alicia", "Kshitija", "Pareen", "Sahil", "Dua", "Manav T", "Rhea", "Jai", "Sharvil", "Alisha", "Ryan", "Shranay", "Sarthak", "Kabeer"]

colors = ["#e50914", "#9c27b0", "#3f51b5", "#009688", "#ff9800", "#795548", "#607d8b", "#e91e63", "#00bcd4", "#cddc39", "#ff5722"]

npcs_data = []
for name in all_names:
    clue = "Happy Birthday Shanaya! Have the best day ever!"
    
    # Core clues for the mystery
    if name == "Maanav": clue = "The murderer definitely has a sweet tooth. Check the Kitchen."
    elif name == "Divya": clue = "I saw someone carrying a heavy candlestick towards the West Wing."
    elif name == "Sarthak": clue = "The crime happened indoors for sure. The garden was empty all night."
    elif name == "Anoushka": clue = "I heard a loud thud near the Dining Room."
    
    # Custom messages
    elif name == "Rahil": clue = "Happy Birthday baby! I put this whole thing together for you. Have fun playing, I love you!"
    elif name == "Kshitija": clue = "Happy Birthday Shanaya! Can't wait for us to celebrate together soon!"
    elif name in ["Shlokk", "Jai"]: clue = "I didn't do it, I swear! I've been outside the whole time."

    npcs_data.append({
        "name": name,
        "clue": clue,
        "color": random.choice(colors),
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ" # You will replace these later
    })

# --- 2. THE CUSTOM CANVAS RPG ENGINE ---
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; background: #0a0a0a; color: white; font-family: 'Nunito', sans-serif; overflow: hidden; display: flex; justify-content: center; }}
    #game-container {{ position: relative; width: 950px; height: 650px; border: 4px solid #222; border-radius: 12px; box-shadow: 0px 10px 40px rgba(0,0,0,0.9); overflow: hidden; background: #2d4a22; }}
    canvas {{ display: block; }}
    
    #dialogue-box {{
        display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background: #1e1e24; border: 3px solid #fdd835; border-radius: 12px; padding: 25px;
        text-align: center; width: 70%; z-index: 100; box-shadow: 0px 20px 60px rgba(0,0,0,0.95);
    }}
    #dialogue-box h2 {{ color: #fdd835; margin-top: 0; }}
    .btn {{ background: #fdd835; color: #111; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 16px; margin-top: 15px; }}
    .btn:hover {{ background: #fff176; }}

    #clue-pad-overlay {{
        display: none; position: absolute; top: 20px; left: 20px; width: calc(100% - 40px); height: calc(100% - 40px);
        background: rgba(20, 20, 25, 0.98); border: 2px solid #555; border-radius: 12px; padding: 20px; z-index: 90; box-sizing: border-box; overflow-y: auto;
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
    <canvas id="gameCanvas" width="950" height="650"></canvas>
    
    <div id="dialogue-box">
        <h2 id="npc-name">Name</h2>
        <div id="video-container" style="border-radius: 8px; overflow: hidden;"></div>
        <p id="npc-clue" style="font-size: 18px; color: #eee; margin: 15px 0; font-weight: bold;"></p>
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

    const MAP_W = 2400;
    const MAP_H = 1800;

    // Player starts at the front gate
    const player = {{ x: 1200, y: 1600, w: 24, h: 32, speed: 6 }};
    const keys = {{}};
    let modalOpen = false; let padOpen = false;

    const rawNpcs = {json.dumps(npcs_data)};
    const npcs = [];

    // --- ARCHITECTURE: T-SHAPED MANSION ---
    const walls = [];
    const furniture = [];

    function W(x, y, w, h) {{ walls.push({{x, y, w, h}}); }}
    
    // Perimeter Exterior Walls
    W(1000, 200, 400, 20); // North Wing Top
    W(1000, 200, 20, 400); // North Wing Left
    W(1380, 200, 20, 400); // North Wing Right
    
    W(600, 600, 400, 20);  // West Wing Top
    W(600, 600, 20, 400);  // West Wing Left
    W(600, 980, 400, 20);  // West Wing Bottom

    W(1400, 600, 400, 20); // East Wing Top
    W(1780, 600, 20, 400); // East Wing Right
    W(1400, 980, 400, 20); // East Wing Bottom

    W(1000, 1380, 150, 20); // Hall Bottom Left
    W(1250, 1380, 150, 20); // Hall Bottom Right (Front Door Gap at 1150-1250)
    W(1000, 1000, 20, 380); // Hall Lower Left
    W(1380, 1000, 20, 380); // Hall Lower Right

    // Interior Dividers (with Doorways)
    W(1000, 580, 150, 20); W(1250, 580, 150, 20); // North door
    W(980, 600, 20, 150); W(980, 850, 20, 150);   // West door
    W(1400, 600, 20, 150); W(1400, 850, 20, 150); // East door
    
    // Room Splitters
    W(600, 780, 300, 20); // Splits West into Kitchen/Dining
    W(1500, 780, 300, 20); // Splits East into Library/Study
    W(1000, 380, 300, 20); // Splits North into Bed/Lounge

    // --- CUSTOM CANVAS FURNITURE (Pixel Art Style) ---
    function addFurn(x, y, w, h, type, solid=true) {{ furniture.push({{x, y, w, h, type, solid}}); }}

    // Kitchen & Dining (West)
    addFurn(650, 630, 80, 40, "counter");
    addFurn(850, 630, 40, 60, "fridge");
    addFurn(700, 850, 120, 80, "dining_table");

    // Library & Study (East)
    addFurn(1450, 630, 250, 30, "bookshelf");
    addFurn(1450, 680, 250, 30, "bookshelf");
    addFurn(1500, 850, 100, 50, "desk");
    addFurn(1700, 850, 50, 50, "plant");

    // North Wing (Bed/Lounge)
    addFurn(1150, 230, 100, 120, "bed");
    addFurn(1050, 450, 150, 50, "couch");
    addFurn(1080, 520, 90, 50, "rug", false); // Rugs aren't solid

    // Grand Hall
    addFurn(1100, 1050, 150, 100, "piano");
    addFurn(1150, 650, 100, 350, "red_carpet", false);

    // Garden Trees
    for(let i=0; i<40; i++) {{
        let tx = 100 + Math.random()*2200;
        let ty = 100 + Math.random()*1600;
        // Don't spawn trees inside the house bounds
        if(tx > 500 && tx < 1900 && ty > 150 && ty < 1450) continue;
        addFurn(tx, ty, 40, 40, "tree");
    }}
    addFurn(1150, 1650, 100, 100, "fountain");

    // --- INITIALIZE NPCs ---
    rawNpcs.forEach(data => {{
        // Spawn them randomly inside the house mostly
        let nx = 700 + Math.random()*1000;
        let ny = 300 + Math.random()*1000;
        if(Math.random() < 0.2) {{ nx = 300 + Math.random()*1800; ny = 1450 + Math.random()*300; }} // Some outside
        
        npcs.push({{
            x: nx, y: ny, w: 24, h: 32,
            data: data, vx: 0, vy: 0, timer: 0
        }});
    }});

    // --- INPUT ---
    window.addEventListener("keydown", (e) => {{
        keys[e.code] = true;
        if(e.code === "Space" && !modalOpen && !padOpen) interact();
        if(e.code === "KeyC") togglePad();
        if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space","KeyW","KeyA","KeyS","KeyD"].includes(e.code)) e.preventDefault();
    }});
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    // --- COLLISION ---
    function isColliding(r1, r2) {{
        return r1.x < r2.x + r2.w && r1.x + r1.w > r2.x && r1.y < r2.y + r2.h && r1.y + r1.h > r2.y;
    }}
    function canMove(newX, newY, w, h) {{
        let pNext = {{ x: newX, y: newY, w: w, h: h }};
        if(newX < 40 || newX + w > MAP_W-40 || newY < 40 || newY + h > MAP_H-40) return false;
        for(let wl of walls) if(isColliding(pNext, wl)) return false;
        for(let f of furniture) if(f.solid && isColliding(pNext, f)) return false;
        return true;
    }}

    function getRoom(px, py) {{
        if(px > 600 && px < 1000 && py > 600 && py < 800) return "Kitchen";
        if(px > 600 && px < 1000 && py > 800 && py < 1000) return "Dining";
        if(px > 1400 && px < 1800 && py > 600 && py < 800) return "Library";
        if(px > 1400 && px < 1800 && py > 800 && py < 1000) return "Study";
        if(px > 1000 && px < 1400 && py > 200 && py < 400) return "MasterBed";
        if(px > 1000 && px < 1400 && py > 400 && py < 600) return "Lounge";
        if(px > 1000 && px < 1400 && py > 600 && py < 1400) return "Hall";
        return "Garden";
    }}

    // --- GAME LOOP ---
    function update() {{
        if(modalOpen || padOpen) return;

        // Player Movement
        let dx = 0, dy = 0;
        if (keys["KeyW"] || keys["ArrowUp"]) dy = -player.speed;
        if (keys["KeyS"] || keys["ArrowDown"]) dy = player.speed;
        if (keys["KeyA"] || keys["ArrowLeft"]) dx = -player.speed;
        if (keys["KeyD"] || keys["ArrowRight"]) dx = player.speed;
        if (dx !== 0 && dy !== 0) {{ dx *= 0.7; dy *= 0.7; }}

        if (dx !== 0 && canMove(player.x + dx, player.y, player.w, player.h)) player.x += dx;
        if (dy !== 0 && canMove(player.x, player.y + dy, player.w, player.h)) player.y += dy;
        
        // NPC AI Wandering
        npcs.forEach(n => {{
            n.timer -= 1;
            if(n.timer <= 0) {{
                n.vx = (Math.random() - 0.5) * 2;
                n.vy = (Math.random() - 0.5) * 2;
                n.timer = Math.floor(Math.random() * 80) + 40;
                if(Math.random() < 0.3) {{ n.vx = 0; n.vy = 0; }} // Stand still sometimes
            }}
            if(canMove(n.x + n.vx, n.y, n.w, n.h)) n.x += n.vx; else n.vx *= -1;
            if(canMove(n.x, n.y + n.vy, n.w, n.h)) n.y += n.vy; else n.vy *= -1;

            let dist = Math.hypot((player.x) - (n.x), (player.y) - (n.y));
            n.near = dist < 60;
        }});
    }}

    // --- DRAWING FUNCTIONS ---
    function drawCharacter(x, y, color, name, isPlayer=false) {{
        ctx.fillStyle = color; ctx.fillRect(x, y+10, 24, 22); // Body
        ctx.fillStyle = '#FFDDC1'; ctx.beginPath(); ctx.arc(x+12, y+8, 10, 0, Math.PI*2); ctx.fill(); // Head
        ctx.fillStyle = 'black'; ctx.beginPath(); ctx.arc(x+8, y+6, 2, 0, Math.PI*2); ctx.fill(); // Eyes
        ctx.beginPath(); ctx.arc(x+16, y+6, 2, 0, Math.PI*2); ctx.fill();
        
        ctx.fillStyle = isPlayer ? '#00d2ff' : 'white'; 
        ctx.font = "bold 12px 'Nunito'"; ctx.textAlign = 'center';
        ctx.fillText(name, x+12, y-6);
    }}

    function draw() {{
        ctx.fillStyle = "#3a5f2b"; // Bright Garden Grass
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.save();
        let camX = canvas.width/2 - (player.x + player.w/2);
        let camY = canvas.height/2 - (player.y + player.h/2);
        ctx.translate(camX, camY);

        // Draw Dirt Paths
        ctx.fillStyle = "#6B4423"; ctx.fillRect(1150, 1380, 100, 420); 

        // Draw Wooden Fence around the map
        ctx.fillStyle = '#5c3a21';
        for(let i=0; i<MAP_W; i+=60) {{ ctx.fillRect(i, 10, 15, 30); ctx.fillRect(i, MAP_H-40, 15, 30); }}
        for(let i=0; i<MAP_H; i+=60) {{ ctx.fillRect(10, i, 30, 15); ctx.fillRect(MAP_W-40, i, 30, 15); }}
        ctx.fillRect(15, 25, MAP_W-30, 10); ctx.fillRect(15, MAP_H-25, MAP_W-30, 10);
        ctx.fillRect(25, 15, 10, MAP_H-30); ctx.fillRect(MAP_W-25, 15, 10, MAP_H-30);

        // Draw Mansion Floor
        ctx.fillStyle = "#8b5a2b"; 
        ctx.fillRect(1000, 200, 400, 400); // North
        ctx.fillRect(600, 600, 1200, 400); // West to East
        ctx.fillRect(1000, 1000, 400, 380); // Hall bottom

        // Draw Walls
        ctx.fillStyle = "#111";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));

        // Draw Custom Furniture
        furniture.forEach(f => {{
            if(f.type === "dining_table") {{
                ctx.fillStyle = '#4A2311'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = '#6B3E26'; ctx.fillRect(f.x+5,f.y+5,f.w-10,f.h-10);
                // Plates
                ctx.fillStyle = 'white';
                ctx.beginPath(); ctx.arc(f.x+30, f.y+20, 8, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+90, f.y+60, 8, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "bed") {{
                ctx.fillStyle = '#2C3E50'; ctx.fillRect(f.x,f.y,f.w,f.h); // Frame
                ctx.fillStyle = '#ECF0F1'; ctx.fillRect(f.x+10,f.y+10,f.w-20,30); // Pillows
                ctx.fillStyle = '#C0392B'; ctx.fillRect(f.x+5,f.y+45,f.w-10,70); // Blanket
            }}
            else if(f.type === "couch") {{
                ctx.fillStyle = '#2980B9'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = '#1F618D'; ctx.fillRect(f.x,f.y,20,f.h); ctx.fillRect(f.x+f.w-20,f.y,20,f.h);
            }}
            else if(f.type === "rug") {{
                ctx.fillStyle = '#8E44AD'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.strokeStyle = '#F1C40F'; ctx.lineWidth=3; ctx.strokeRect(f.x+5,f.y+5,f.w-10,f.h-10);
            }}
            else if(f.type === "red_carpet") {{
                ctx.fillStyle = '#800000'; ctx.fillRect(f.x,f.y,f.w,f.h);
            }}
            else if(f.type === "tree") {{
                ctx.fillStyle = '#4A2311'; ctx.fillRect(f.x+15,f.y+20,10,20);
                ctx.fillStyle = '#27AE60'; ctx.beginPath(); ctx.arc(f.x+20,f.y+15,22,0,Math.PI*2); ctx.fill();
            }}
            else if(f.type === "bookshelf") {{
                ctx.fillStyle = '#3E2723'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = '#5D4037'; ctx.fillRect(f.x+2,f.y+2,f.w-4,f.h-4);
            }}
            else if(f.type === "fountain") {{
                ctx.fillStyle = '#7F8C8D'; ctx.beginPath(); ctx.arc(f.x+f.w/2,f.y+f.h/2,40,0,Math.PI*2); ctx.fill();
                ctx.fillStyle = '#3498DB'; ctx.beginPath(); ctx.arc(f.x+f.w/2,f.y+f.h/2,30,0,Math.PI*2); ctx.fill();
            }}
            else {{
                ctx.fillStyle = '#555'; ctx.fillRect(f.x,f.y,f.w,f.h); // Generic fallback
            }}
        }});

        // Draw Room Typography
        ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 30px 'Nunito'"; ctx.textAlign="center";
        ctx.fillText("MASTER BEDROOM", 1200, 300);
        ctx.fillText("LOUNGE", 1200, 500);
        ctx.fillText("KITCHEN", 800, 700);
        ctx.fillText("DINING", 800, 900);
        ctx.fillText("LIBRARY", 1600, 700);
        ctx.fillText("STUDY", 1600, 900);
        ctx.fillText("GRAND HALL", 1200, 900);

        // Draw NPCs
        npcs.forEach(n => {{
            drawCharacter(n.x, n.y, n.data.color, n.data.name);
            if(n.near) {{
                ctx.fillStyle = "#fdd835"; ctx.font = "bold 20px Arial";
                ctx.fillText("💬", n.x+12, n.y-25);
            }}
        }});

        // Draw Player
        drawCharacter(player.x, player.y, "#00d2ff", "Shanaya", true);

        // --- TRANSLUCENT FOG OF WAR ---
        // Instead of pitch black, it's 65% opacity. She can clearly see the layout of the unvisited rooms.
        let pRoom = getRoom(player.x + player.w/2, player.y + player.h/2);
        ctx.fillStyle = "rgba(0, 0, 0, 0.65)"; 

        if (pRoom === "Garden") {{
            ctx.fillRect(600, 200, 1200, 1180); // Darken whole house
        }} else {{
            if (pRoom !== "Kitchen") ctx.fillRect(600, 600, 400, 180);
            if (pRoom !== "Dining") ctx.fillRect(600, 800, 400, 180);
            if (pRoom !== "Library") ctx.fillRect(1400, 600, 400, 180);
            if (pRoom !== "Study") ctx.fillRect(1400, 800, 400, 180);
            if (pRoom !== "MasterBed") ctx.fillRect(1000, 200, 400, 180);
            if (pRoom !== "Lounge") ctx.fillRect(1000, 400, 400, 180);
            if (pRoom !== "Hall") ctx.fillRect(1000, 600, 400, 780); 
        }}

        ctx.restore(); 
    }}

    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}

    function interact() {{
        let target = npcs.find(n => n.near);
        if(target) {{
            document.getElementById("npc-name").innerText = "Talking to " + target.data.name;
            document.getElementById("npc-clue").innerText = '"' + target.data.clue + '"';
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="280" src="${{target.data.video}}?autoplay=1" frameborder="0"></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true;
        }}
    }}

    window.closeModal = function() {{
        document.getElementById("dialogue-box").style.display = "none";
        document.getElementById("video-container").innerHTML = ""; 
        setTimeout(() => modalOpen = false, 200);
    }}

    const padData = {{}};
    window.togglePad = function() {{
        if(modalOpen) return;
        padOpen = !padOpen;
        document.getElementById("clue-pad-overlay").style.display = padOpen ? "block" : "none";
    }}

    function initPad() {{
        const s = {json.dumps(["Rahul", "Aditi", "Karan", "Prof. Aris", "Mme. Elara", "Maanav", "Divya"])};
        const w = {json.dumps(["Candlestick", "Poison", "Rope", "Axe", "Dagger"])};
        const r = {json.dumps(["Kitchen", "Dining", "Library", "Study", "Lounge", "MasterBed", "Grand Hall"])};
        
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

components.html(game_html, height=700)

st.divider()

col1, col2, col3 = st.columns(3)
with col1: guess_who = st.selectbox("Suspect", ["Select", "Maanav", "Anoushka", "Divya", "Sarthak", "Rahil"])
with col2: guess_where = st.selectbox("Location", ["Select", "Kitchen", "Dining", "Library", "Study", "MasterBed", "Lounge", "Grand Hall"])
with col3: guess_weapon = st.selectbox("Weapon", ["Select", "Candlestick", "Poison", "Rope", "Axe", "Dagger"])
    
if st.button("MAKE ACCUSATION", use_container_width=True, type="primary"):
    if guess_who == "Maanav" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 CORRECT! You cracked the case, Shanaya! Happy Birthday! 🎂")
        st.balloons()
    else:
        st.error("Not quite! Keep exploring the mansion and interrogating the guests.")
