import streamlit as st
import streamlit.components.v1 as components
import json
import random

st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Nunito:wght@400;700;900&display=swap');
    .main .block-container { padding-top: 1rem; max-width: 1200px; }
    h1 { font-family: 'Cinzel', serif; text-align: center; color: #fdd835; font-weight: 900; margin-bottom: 0px; letter-spacing: 2px;}
    .instruction { text-align: center; color: #aaa; font-family: 'Nunito', sans-serif; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>SHANAYA'S MYSTERY</h1>", unsafe_allow_html=True)
st.markdown("<div class='instruction'><b>WASD/Arrows</b> to move | <b>Spacebar</b> to talk/inspect | <b>C</b> for Case File</div>", unsafe_allow_html=True)

# --- 1. GUEST LIST & NPC DATABASE ---
# Removed duplicates from your prompt
all_names = ["Mandira", "Selina", "Maanav", "Anoushka", "Shlokk", "Rahil", "Panthiv", "Samira", "Ishika", "Divya", "Alicia", "Kshitija", "Pareen", "Sahil", "Dua", "Manav T", "Rhea", "Jai", "Sharvil", "Alisha", "Ryan", "Shranay", "Sarthak", "Kabeer"]
colors = ["#e50914", "#9c27b0", "#3f51b5", "#009688", "#ff9800", "#795548", "#607d8b", "#e91e63", "#00bcd4", "#cddc39", "#ff5722"]

npcs_data = []
for name in all_names:
    clue = "Happy Birthday Shanaya! Have the best day ever!"
    
    # Custom clues & messages
    if name == "Maanav": clue = "The murderer definitely has a sweet tooth. Check the Kitchen."
    elif name == "Divya": clue = "I saw someone carrying a heavy candlestick towards the West Wing."
    elif name == "Sarthak": clue = "The crime happened indoors for sure. The garden was empty all night."
    elif name == "Anoushka": clue = "I heard a loud thud near the Dining Room."
    elif name == "Rahil": clue = "Happy Birthday baby! I put this whole thing together for you. Have fun playing, I love you!"
    elif name == "Kshitija": clue = "Happy Birthday Shanaya! Can't wait for us to celebrate together soon!"
    elif name in ["Shlokk", "Jai"]: clue = "I didn't do it, I swear! I've been by the pool the whole time."

    npcs_data.append({
        "name": name, "clue": clue, "color": random.choice(colors),
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ" # Replace these later
    })

# --- 2. THE CUSTOM CANVAS RPG ENGINE ---
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; background: #0a0a0a; color: white; font-family: 'Nunito', sans-serif; overflow: hidden; display: flex; justify-content: center; }}
    #game-container {{ position: relative; width: 1000px; height: 680px; border: 4px solid #222; border-radius: 12px; box-shadow: 0px 10px 40px rgba(0,0,0,0.9); overflow: hidden; background: #2d4a22; }}
    canvas {{ display: block; }}
    
    #dialogue-box {{
        display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background: #1e1e24; border: 3px solid #fdd835; border-radius: 12px; padding: 25px;
        text-align: center; width: 70%; max-width: 500px; z-index: 100; box-shadow: 0px 20px 60px rgba(0,0,0,0.95);
    }}
    #dialogue-box h2 {{ color: #fdd835; margin-top: 0; font-family: 'Cinzel', serif; }}
    .btn {{ background: #fdd835; color: #111; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 16px; margin-top: 15px; width: 100%; }}
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
    <canvas id="gameCanvas" width="1000" height="680"></canvas>
    
    <div id="dialogue-box">
        <h2 id="modal-title">Name</h2>
        <div id="video-container" style="border-radius: 8px; overflow: hidden;"></div>
        <p id="modal-text" style="font-size: 18px; color: #eee; margin: 15px 0; font-weight: bold;"></p>
        <button class="btn" onclick="closeModal()">Close & Resume</button>
    </div>

    <div id="clue-pad-overlay">
        <h2 style="text-align: center; color: #4fc3f7; margin-top: 0; font-family: 'Cinzel', serif;">📋 Detective Pad</h2>
        <div class="grid" id="clue-grid">
            <div id="col-suspects"><h3 style="color:#aaa;">Suspects</h3></div>
            <div id="col-weapons"><h3 style="color:#aaa;">Weapons</h3></div>
            <div id="col-rooms"><h3 style="color:#aaa;">Rooms</h3></div>
        </div>
        <div style="text-align: center; margin-top: 20px;"><button class="btn" style="width: 200px;" onclick="togglePad()">Close Pad (C)</button></div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    const MAP_W = 2400; const MAP_H = 2000;

    // Player starts at the South Gate
    const player = {{ x: 1200, y: 1850, w: 24, h: 32, speed: 6 }};
    const keys = {{}};
    let modalOpen = false; let padOpen = false;

    // --- GAME WORLD DATA ---
    const rawNpcs = {json.dumps(npcs_data)};
    const npcs = [];
    const walls = []; const furniture = []; const interactables = [];

    function W(x, y, w, h) {{ walls.push({{x, y, w, h}}); }}
    function addFurn(x, y, w, h, type, solid=true) {{ furniture.push({{x, y, w, h, type, solid}}); }}
    function addProp(x, y, title, text) {{ interactables.push({{x, y, w: 40, h: 40, title, text, near: false}}); }}

    // 1. Perimeter Estate Fences
    W(0, 0, MAP_W, 20); W(0, MAP_H-20, 1100, 20); W(1300, MAP_H-20, 1100, 20); // Gap for South Gate
    W(0, 0, 20, MAP_H); W(MAP_W-20, 0, 20, MAP_H);

    // 2. Mansion Walls
    W(1000, 200, 400, 20); W(1000, 200, 20, 400); W(1380, 200, 20, 400); // North Wing
    W(600, 600, 400, 20);  W(600, 600, 20, 400);  W(600, 980, 400, 20);  // West Wing
    W(1400, 600, 400, 20); W(1780, 600, 20, 400); W(1400, 980, 400, 20); // East Wing
    W(1000, 1380, 150, 20); W(1250, 1380, 150, 20); // Hall Bottom
    W(1000, 1000, 20, 380); W(1380, 1000, 20, 380); // Hall Sides

    // Dividers
    W(1000, 580, 150, 20); W(1250, 580, 150, 20); // North door
    W(980, 600, 20, 150); W(980, 850, 20, 150);   // West door
    W(1400, 600, 20, 150); W(1400, 850, 20, 150); // East door
    W(600, 780, 300, 20); W(1500, 780, 300, 20); W(1000, 380, 300, 20); 

    // 3. Pool Deck (East Garden)
    addFurn(1600, 1100, 600, 400, "deck", false);
    addFurn(1650, 1150, 400, 200, "pool");
    addFurn(1900, 1400, 150, 60, "bar");
    addFurn(1650, 1400, 50, 80, "deckchair"); addFurn(1750, 1400, 50, 80, "deckchair");

    // 4. Mansion Interior High-Def Furniture
    addFurn(650, 630, 120, 50, "kitchen_island"); // Kitchen
    addFurn(850, 630, 50, 70, "fridge");
    addFurn(700, 850, 140, 80, "dining_table");   // Dining Room
    addFurn(1450, 630, 250, 40, "bookshelf");     // Library
    addFurn(1450, 700, 250, 40, "bookshelf");
    addFurn(1500, 880, 120, 60, "desk");          // Study
    addFurn(1150, 230, 120, 140, "bed");          // Master Bedroom
    addFurn(1050, 450, 160, 60, "couch");         // Lounge
    addFurn(1080, 520, 100, 60, "rug", false);
    addFurn(1120, 1050, 120, 100, "piano");       // Grand Hall

    // 5. Environmental Storytelling Props (Magnifying Glasses)
    addProp(740, 860, "Birthday Cake", "A beautiful, sugar-free chocolate cake from Ritual Cafe! Looks delicious.");
    addProp(1660, 1420, "Poolside Items", "Someone left their Speedo swimming accessories resting on the deck chair.");
    addProp(670, 640, "Warm Food", "A freshly cooked wok of Egg Schezwan Fried Rice from Kuai Kitchen is sitting on the stove.");
    
    // 6. Garden Trees
    for(let i=0; i<45; i++) {{
        let tx = 100 + Math.random()*2200; let ty = 100 + Math.random()*1800;
        if(tx > 500 && tx < 1900 && ty > 150 && ty < 1450) continue; // Keep out of house
        if(tx > 1500 && ty > 1000) continue; // Keep out of pool
        if(tx > 1100 && tx < 1300 && ty > 1700) continue; // Keep out of driveway
        addFurn(tx, ty, 60, 60, "tree");
    }}

    // Spawn NPCs
    rawNpcs.forEach(data => {{
        let nx = 700 + Math.random()*1000; let ny = 300 + Math.random()*1000;
        if(Math.random() < 0.3) {{ nx = 1600 + Math.random()*300; ny = 1100 + Math.random()*300; }} // Spawn by pool
        npcs.push({{ x: nx, y: ny, w: 24, h: 32, data: data, vx: 0, vy: 0, timer: 0 }});
    }});

    // --- ENGINE LOGIC ---
    window.addEventListener("keydown", (e) => {{
        keys[e.code] = true;
        if(e.code === "Space" && !modalOpen && !padOpen) interact();
        if(e.code === "KeyC") togglePad();
        if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space","KeyW","KeyA","KeyS","KeyD"].includes(e.code)) e.preventDefault();
    }});
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    function isColliding(r1, r2) {{ return r1.x < r2.x + r2.w && r1.x + r1.w > r2.x && r1.y < r2.y + r2.h && r1.y + r1.h > r2.y; }}
    
    function canMove(newX, newY, w, h) {{
        let pNext = {{ x: newX, y: newY, w: w, h: h }};
        if(newX < 20 || newX + w > MAP_W-20 || newY < 20 || newY + h > MAP_H-20) return false;
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

    function update() {{
        if(modalOpen || padOpen) return;

        let dx = 0, dy = 0;
        if (keys["KeyW"] || keys["ArrowUp"]) dy = -player.speed;
        if (keys["KeyS"] || keys["ArrowDown"]) dy = player.speed;
        if (keys["KeyA"] || keys["ArrowLeft"]) dx = -player.speed;
        if (keys["KeyD"] || keys["ArrowRight"]) dx = player.speed;
        if (dx !== 0 && dy !== 0) {{ dx *= 0.7; dy *= 0.7; }}

        if (dx !== 0 && canMove(player.x + dx, player.y, player.w, player.h)) player.x += dx;
        if (dy !== 0 && canMove(player.x, player.y + dy, player.w, player.h)) player.y += dy;
        
        // NPC AI
        npcs.forEach(n => {{
            n.timer -= 1;
            if(n.timer <= 0) {{
                n.vx = (Math.random() - 0.5) * 2; n.vy = (Math.random() - 0.5) * 2;
                n.timer = Math.floor(Math.random() * 80) + 40;
                if(Math.random() < 0.3) {{ n.vx = 0; n.vy = 0; }} 
            }}
            if(canMove(n.x + n.vx, n.y, n.w, n.h)) n.x += n.vx; else n.vx *= -1;
            if(canMove(n.x, n.y + n.vy, n.w, n.h)) n.y += n.vy; else n.vy *= -1;

            n.near = Math.hypot((player.x) - (n.x), (player.y) - (n.y)) < 60;
        }});

        interactables.forEach(prop => {{
            prop.near = Math.hypot((player.x) - (prop.x), (player.y) - (prop.y)) < 50;
        }});
    }}

    // --- DRAWING WITH ADVANCED GRAPHICS ---
    function drawCharacter(x, y, color, name, isPlayer=false) {{
        ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 10; ctx.shadowOffsetY = 5;
        ctx.fillStyle = color; ctx.fillRect(x, y+10, 24, 22); 
        ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
        
        ctx.fillStyle = '#FFDDC1'; ctx.beginPath(); ctx.arc(x+12, y+8, 10, 0, Math.PI*2); ctx.fill(); 
        ctx.fillStyle = 'black'; ctx.beginPath(); ctx.arc(x+8, y+6, 2, 0, Math.PI*2); ctx.fill(); 
        ctx.beginPath(); ctx.arc(x+16, y+6, 2, 0, Math.PI*2); ctx.fill();
        
        ctx.fillStyle = isPlayer ? '#00d2ff' : 'white'; 
        ctx.font = "bold 12px 'Nunito'"; ctx.textAlign = 'center';
        ctx.fillText(name, x+12, y-8);
    }}

    function draw() {{
        ctx.fillStyle = "#3a5f2b"; ctx.fillRect(0, 0, canvas.width, canvas.height); // Grass
        
        ctx.save();
        let camX = canvas.width/2 - (player.x + player.w/2);
        let camY = canvas.height/2 - (player.y + player.h/2);
        ctx.translate(camX, camY);

        // Driveway & Gates
        ctx.fillStyle = "#6B4423"; ctx.fillRect(1150, 1380, 100, 620); // Path
        ctx.fillStyle = "#111"; 
        ctx.fillRect(1080, MAP_H-30, 40, 40); ctx.fillRect(1280, MAP_H-30, 40, 40); // Gate Pillars
        ctx.fillStyle = "#333"; ctx.fillRect(1120, MAP_H-15, 160, 10); // Wrought Iron Gate Line

        // Mansion Floors
        ctx.fillStyle = "#8b5a2b"; 
        ctx.fillRect(1000, 200, 400, 400); ctx.fillRect(600, 600, 1200, 400); ctx.fillRect(1000, 1000, 400, 380); 

        // Walls
        ctx.fillStyle = "#1a1a1a";
        ctx.shadowColor = 'rgba(0,0,0,0.8)'; ctx.shadowBlur = 15;
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.shadowBlur = 0;

        // Rich Furniture rendering
        furniture.forEach(f => {{
            ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 4;
            
            if(f.type === "pool") {{
                let grad = ctx.createLinearGradient(f.x, f.y, f.x+f.w, f.y+f.h);
                grad.addColorStop(0, '#00a8ff'); grad.addColorStop(1, '#0097e6');
                ctx.fillStyle = 'white'; ctx.fillRect(f.x-5, f.y-5, f.w+10, f.h+10); // Tiles
                ctx.fillStyle = grad; ctx.fillRect(f.x, f.y, f.w, f.h); // Water
                ctx.strokeStyle = 'rgba(255,255,255,0.3)'; ctx.lineWidth = 2; // Ripples
                ctx.beginPath(); ctx.arc(f.x+100, f.y+50, 30, 0, Math.PI); ctx.stroke();
            }}
            else if(f.type === "deck") {{ ctx.fillStyle = '#d4a373'; ctx.fillRect(f.x, f.y, f.w, f.h); }}
            else if(f.type === "bar") {{
                ctx.fillStyle = '#8B4513'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = '#333'; ctx.beginPath(); ctx.arc(f.x+20, f.y-15, 12, 0, Math.PI*2); ctx.fill(); // Stools
                ctx.beginPath(); ctx.arc(f.x+75, f.y-15, 12, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "deckchair") {{ ctx.fillStyle = '#fff'; ctx.fillRect(f.x, f.y, f.w, f.h); ctx.fillStyle = '#00a8ff'; ctx.fillRect(f.x+5, f.y+5, f.w-10, f.h-10);}}
            else if(f.type === "dining_table") {{
                ctx.fillStyle = '#4A2311'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = 'white'; ctx.beginPath(); ctx.arc(f.x+30, f.y+20, 8, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+110, f.y+60, 8, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "bed") {{
                ctx.fillStyle = '#2C3E50'; ctx.fillRect(f.x,f.y,f.w,f.h); 
                ctx.fillStyle = '#ECF0F1'; ctx.fillRect(f.x+10,f.y+10,40,30); ctx.fillRect(f.x+70,f.y+10,40,30);
                ctx.fillStyle = '#C0392B'; ctx.fillRect(f.x+5,f.y+50,f.w-10,85); 
            }}
            else if(f.type === "kitchen_island") {{
                ctx.fillStyle = '#bdc3c7'; ctx.fillRect(f.x,f.y,f.w,f.h); // Marble
                ctx.fillStyle = '#34495e'; ctx.fillRect(f.x+10,f.y+10,30,30); // Stove top
                ctx.fillStyle = '#e74c3c'; ctx.beginPath(); ctx.arc(f.x+25, f.y+25, 8, 0, Math.PI*2); ctx.fill(); // Burner
            }}
            else if(f.type === "tree") {{
                ctx.shadowBlur = 15;
                ctx.fillStyle = '#27AE60'; ctx.beginPath(); ctx.arc(f.x+30,f.y+30,35,0,Math.PI*2); ctx.fill();
            }}
            else {{
                ctx.fillStyle = '#555'; ctx.fillRect(f.x,f.y,f.w,f.h); 
            }}
            ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
        }});

        // Room Labels
        ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 30px 'Nunito'"; ctx.textAlign="center";
        ctx.fillText("MASTER BEDROOM", 1200, 300); ctx.fillText("LOUNGE", 1200, 500);
        ctx.fillText("KITCHEN", 800, 700); ctx.fillText("DINING", 800, 900);
        ctx.fillText("LIBRARY", 1600, 700); ctx.fillText("STUDY", 1600, 900);
        ctx.fillText("GRAND HALL", 1200, 1100); ctx.fillText("SOUTH GATE", 1200, 1800);

        // Draw Interactive Props
        interactables.forEach(p => {{
            if(p.near) {{
                ctx.fillStyle = "#fff"; ctx.font = "bold 24px Arial";
                ctx.fillText("🔍", p.x, p.y-10);
            }}
        }});

        // Draw NPCs & Player
        npcs.forEach(n => {{
            drawCharacter(n.x, n.y, n.data.color, n.data.name);
            if(n.near) {{ ctx.fillStyle = "#fdd835"; ctx.font = "bold 20px Arial"; ctx.fillText("💬", n.x+12, n.y-20); }}
        }});
        drawCharacter(player.x, player.y, "#00d2ff", "Shanaya", true);

        // Translucent Fog
        let pRoom = getRoom(player.x + player.w/2, player.y + player.h/2);
        ctx.fillStyle = "rgba(0, 0, 0, 0.65)"; 

        if (pRoom === "Garden") {{
            ctx.fillRect(600, 200, 1200, 1180); 
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
        // Check Props First
        let targetProp = interactables.find(p => p.near);
        if(targetProp) {{
            document.getElementById("modal-title").innerText = targetProp.title;
            document.getElementById("modal-text").innerText = targetProp.text;
            document.getElementById("video-container").innerHTML = ""; 
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true; return;
        }}

        // Check NPCs
        let target = npcs.find(n => n.near);
        if(target) {{
            document.getElementById("modal-title").innerText = "Talking to " + target.data.name;
            document.getElementById("modal-text").innerText = '"' + target.data.clue + '"';
            
            // Only show video iframe if we eventually add real links to them, for now it plays the placeholder
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
        const s = {json.dumps(["Rahul", "Aditi", "Karan", "Prof. Aris", "Mme. Elara", "Maanav", "Divya", "Sarthak"])};
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

    initPad(); loop();
</script>
</body>
</html>
"""

components.html(game_html, height=730)

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
