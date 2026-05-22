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
all_names = ["Mandira", "Selina", "Maanav", "Anoushka", "Shlokk", "Rahil", "Panthiv", "Samira", "Ishika", "Divya", "Alicia", "Kshitija", "Pareen", "Sahil", "Dua", "Manav T", "Rhea", "Jai", "Sharvil", "Alisha", "Ryan", "Shranay", "Sarthak", "Kabeer"]
colors = ["#e50914", "#9c27b0", "#3f51b5", "#009688", "#ff9800", "#795548", "#607d8b", "#e91e63", "#00bcd4", "#cddc39", "#ff5722"]

npcs_data = []
for name in all_names:
    clue = "Happy Birthday Shanaya! Have the best day ever!"
    if name == "Maanav": clue = "The murderer definitely has a sweet tooth. Check the Kitchen."
    elif name == "Divya": clue = "I saw someone carrying a heavy candlestick towards the West Wing."
    elif name == "Sarthak": clue = "The crime happened indoors for sure. The garden was empty all night."
    elif name == "Anoushka": clue = "I heard a loud thud near the Dining Room."
    elif name == "Rahil": clue = "Happy Birthday baby! I put this whole thing together for you. Have fun playing, I love you!"
    elif name == "Kshitija": clue = "Happy Birthday Shanaya! Can't wait for us to celebrate together soon!"
    elif name in ["Shlokk", "Jai"]: clue = "I didn't do it, I swear! I've been by the pool the whole time."

    npcs_data.append({
        "name": name, "clue": clue, "color": random.choice(colors),
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ" 
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

    const MAP_W = 2800; const MAP_H = 2200;

    const player = {{ x: 1400, y: 1950, w: 24, h: 32, speed: 6 }};
    const keys = {{}};
    let modalOpen = false; let padOpen = false;

    const rawNpcs = {json.dumps(npcs_data)};
    const npcs = [];
    const walls = []; const furniture = []; const interactables = [];

    function W(x, y, w, h) {{ walls.push({{x, y, w, h}}); }}
    function addFurn(x, y, w, h, type, solid=true) {{ furniture.push({{x, y, w, h, type, solid}}); }}
    function addProp(x, y, title, text) {{ interactables.push({{x, y, w: 24, h: 24, title, text, near: false}}); }}

    // 1. Estate Perimeter
    W(0, 0, MAP_W, 20); W(0, MAP_H-20, 1300, 20); W(1500, MAP_H-20, 1300, 20); 
    W(0, 0, 20, MAP_H); W(MAP_W-20, 0, 20, MAP_H);

    // 2. Mansion Walls
    W(1200, 400, 400, 20); W(1200, 400, 20, 400); W(1580, 400, 20, 400); // North Wing
    W(800, 800, 400, 20);  W(800, 800, 20, 400);  W(800, 1180, 400, 20);  // West Wing
    W(1600, 800, 400, 20); W(1980, 800, 20, 400); W(1600, 1180, 400, 20); // East Wing
    W(1200, 1580, 150, 20); W(1450, 1580, 150, 20); // Hall Bottom
    W(1200, 1200, 20, 380); W(1580, 1200, 20, 380); // Hall Sides
    W(1200, 780, 150, 20); W(1450, 780, 150, 20); // North door
    W(1180, 800, 20, 150); W(1180, 1050, 20, 150); // West door
    W(1600, 800, 20, 150); W(1600, 1050, 20, 150); // East door
    W(800, 980, 300, 20); W(1700, 980, 300, 20); W(1200, 580, 300, 20); 

    // 3. West Garden (Pickleball)
    addFurn(100, 900, 500, 800, "pickleball", true);

    // 4. East Garden (Pool Deck)
    addFurn(1900, 1300, 600, 500, "deck", false);
    addFurn(2000, 1350, 400, 250, "pool", false); // SOLID=FALSE, SHE CAN SWIM!
    addFurn(2250, 1650, 180, 80, "bar");
    addFurn(1950, 1650, 60, 90, "deckchair"); addFurn(2050, 1650, 60, 90, "deckchair");

    // 5. High-Def Interior Furniture
    addFurn(880, 830, 150, 60, "kitchen_island"); 
    addFurn(1100, 830, 60, 80, "fridge");
    addFurn(920, 1050, 160, 90, "dining_table");   
    addFurn(1650, 830, 300, 40, "bookshelf");     
    addFurn(1650, 900, 300, 40, "bookshelf");
    addFurn(1750, 1080, 140, 70, "desk");          
    addFurn(1350, 430, 150, 160, "bed");          
    addFurn(1250, 650, 200, 80, "couch");         
    addFurn(1280, 740, 140, 80, "rug", false);
    addFurn(1320, 1250, 140, 120, "piano");       

    // 6. Glowing Interactable Props
    addProp(900, 840, "Birthday Cake", "A gorgeous sugar-free chocolate cake from Ritual Cafe! Looks delicious.");
    addProp(1950, 1600, "Poolside Items", "A bottle of Isdin Fusion Water sunscreen and a Garmin smartwatch left on the deck.");
    addProp(940, 840, "Warm Food", "A freshly cooked wok of Egg Schezwan Fried Rice from Kuai Kitchen is sitting on the stove.");
    
    // 7. Garden Trees
    for(let i=0; i<60; i++) {{
        let tx = 100 + Math.random()*2600; let ty = 100 + Math.random()*2000;
        if(tx > 700 && tx < 2100 && ty > 300 && ty < 1650) continue; 
        if(tx > 1800 && ty > 1200) continue; 
        if(tx < 700 && ty > 800) continue; // Keep off pickleball
        if(tx > 1300 && tx < 1500 && ty > 1800) continue; 
        addFurn(tx, ty, 60, 60, "tree");
    }}

    // Spawn NPCs
    rawNpcs.forEach(data => {{
        let nx = 900 + Math.random()*1000; let ny = 500 + Math.random()*1000;
        if(Math.random() < 0.2) {{ nx = 2000 + Math.random()*400; ny = 1300 + Math.random()*400; }} // Pool
        if(Math.random() < 0.1) {{ nx = 200 + Math.random()*300; ny = 1000 + Math.random()*500; }} // Pickleball
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
        if(px > 800 && px < 1200 && py > 800 && py < 1000) return "Kitchen";
        if(px > 800 && px < 1200 && py > 1000 && py < 1200) return "Dining";
        if(px > 1600 && px < 2000 && py > 800 && py < 1000) return "Library";
        if(px > 1600 && px < 2000 && py > 1000 && py < 1200) return "Study";
        if(px > 1200 && px < 1600 && py > 400 && py < 600) return "MasterBed";
        if(px > 1200 && px < 1600 && py > 600 && py < 800) return "Lounge";
        if(px > 1200 && px < 1600 && py > 800 && py < 1600) return "Hall";
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
            prop.near = Math.hypot((player.x) - (prop.x), (player.y) - (prop.y)) < 60;
        }});
    }}

    // --- DRAWING WITH ARCHITECTURAL DETAIL ---
    function drawCharacter(x, y, color, name, isPlayer=false) {{
        ctx.fillStyle = color; ctx.fillRect(x, y+10, 24, 22); 
        ctx.fillStyle = '#FFDDC1'; ctx.beginPath(); ctx.arc(x+12, y+8, 10, 0, Math.PI*2); ctx.fill(); 
        ctx.fillStyle = 'black'; ctx.beginPath(); ctx.arc(x+8, y+6, 2, 0, Math.PI*2); ctx.fill(); 
        ctx.beginPath(); ctx.arc(x+16, y+6, 2, 0, Math.PI*2); ctx.fill();
        
        ctx.fillStyle = isPlayer ? '#00d2ff' : 'white'; 
        ctx.font = "bold 12px 'Nunito'"; ctx.textAlign = 'center';
        ctx.fillText(name, x+12, y-8);
    }}

    function draw() {{
        ctx.fillStyle = "#3a5f2b"; ctx.fillRect(0, 0, canvas.width, canvas.height); 
        
        ctx.save();
        let camX = canvas.width/2 - (player.x + player.w/2);
        let camY = canvas.height/2 - (player.y + player.h/2);
        ctx.translate(camX, camY);

        ctx.fillStyle = "#6B4423"; ctx.fillRect(1350, 1580, 100, 620); // Path
        ctx.fillStyle = "#111"; 
        ctx.fillRect(1280, MAP_H-30, 40, 40); ctx.fillRect(1480, MAP_H-30, 40, 40); // Gate Pillars
        ctx.fillStyle = "#333"; ctx.fillRect(1320, MAP_H-15, 160, 10); // Gate

        ctx.fillStyle = "#8b5a2b"; // Floors
        ctx.fillRect(1200, 400, 400, 400); ctx.fillRect(800, 800, 1200, 400); ctx.fillRect(1200, 1200, 400, 380); 

        ctx.fillStyle = "#1a1a1a";
        ctx.shadowColor = 'rgba(0,0,0,0.8)'; ctx.shadowBlur = 10;
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.shadowBlur = 0;

        // HIGH-DEF FURNITURE RENDERING
        furniture.forEach(f => {{
            if(f.type === "pool") {{
                ctx.fillStyle = '#f5f5f5'; ctx.fillRect(f.x-8, f.y-8, f.w+16, f.h+16); // Coping
                ctx.fillStyle = '#0288d1'; ctx.fillRect(f.x, f.y, f.w, f.h); // Water
                ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 2; // Water lines
                ctx.beginPath(); ctx.moveTo(f.x+20, f.y+20); ctx.lineTo(f.x+100, f.y+40); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(f.x+f.w-100, f.y+f.h-40); ctx.lineTo(f.x+f.w-20, f.y+f.h-20); ctx.stroke();
                ctx.fillStyle = "#e91e63"; ctx.beginPath(); ctx.arc(f.x+f.w/2, f.y+f.h/2, 25, 0, Math.PI*2); ctx.fill(); // Float
                ctx.fillStyle = "#0288d1"; ctx.beginPath(); ctx.arc(f.x+f.w/2, f.y+f.h/2, 12, 0, Math.PI*2); ctx.fill(); 
            }}
            else if(f.type === "pickleball") {{
                ctx.fillStyle = "#1b5e20"; ctx.fillRect(f.x, f.y, f.w, f.h); // Green outer
                ctx.fillStyle = "#1565c0"; ctx.fillRect(f.x+40, f.y+40, f.w-80, f.h-80); // Blue Inner
                ctx.strokeStyle = "white"; ctx.lineWidth = 4; ctx.strokeRect(f.x+40, f.y+40, f.w-80, f.h-80); // Bounds
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2); ctx.lineTo(f.x+f.w-40, f.y+f.h/2); ctx.stroke(); // Net
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2-80); ctx.lineTo(f.x+f.w-40, f.y+f.h/2-80); ctx.stroke(); // Top NVZ
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2+80); ctx.lineTo(f.x+f.w-40, f.y+f.h/2+80); ctx.stroke(); // Bottom NVZ
                ctx.beginPath(); ctx.moveTo(f.x+f.w/2, f.y+40); ctx.lineTo(f.x+f.w/2, f.y+f.h/2-80); ctx.stroke(); // Center top
                ctx.beginPath(); ctx.moveTo(f.x+f.w/2, f.y+f.h/2+80); ctx.lineTo(f.x+f.w/2, f.y+f.h-40); ctx.stroke(); // Center bot
            }}
            else if(f.type === "deck") {{ ctx.fillStyle = '#d4a373'; ctx.fillRect(f.x, f.y, f.w, f.h); }}
            else if(f.type === "bar") {{
                ctx.fillStyle = '#5d4037'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = '#333'; ctx.beginPath(); ctx.arc(f.x+30, f.y-15, 12, 0, Math.PI*2); ctx.fill(); 
                ctx.beginPath(); ctx.arc(f.x+90, f.y-15, 12, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+150, f.y-15, 12, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "deckchair") {{ ctx.fillStyle = '#fff'; ctx.fillRect(f.x, f.y, f.w, f.h); ctx.fillStyle = '#03a9f4'; ctx.fillRect(f.x+5, f.y+5, f.w-10, f.h-10);}}
            else if(f.type === "dining_table") {{
                ctx.fillStyle = '#4A2311'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = 'white'; ctx.beginPath(); ctx.arc(f.x+30, f.y+20, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+80, f.y+20, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+130, f.y+20, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+30, f.y+70, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+80, f.y+70, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+130, f.y+70, 10, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "bed") {{
                ctx.fillStyle = '#3e2723'; ctx.fillRect(f.x,f.y,f.w,f.h); // Frame
                ctx.fillStyle = '#fafafa'; ctx.fillRect(f.x+8,f.y+8,f.w-16,f.h-16); // Mattress
                ctx.fillStyle = '#e0e0e0'; ctx.fillRect(f.x+15,f.y+15,50,30); ctx.fillRect(f.x+85,f.y+15,50,30); // Pillows
                ctx.fillStyle = '#1565c0'; ctx.fillRect(f.x+8,f.y+60,f.w-16,f.h-68); // Blanket
            }}
            else if(f.type === "kitchen_island") {{
                ctx.fillStyle = '#eceff1'; ctx.fillRect(f.x,f.y,f.w,f.h); // Marble
                ctx.fillStyle = '#37474f'; ctx.fillRect(f.x+15,f.y+15,40,30); // Stove
                ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(f.x+25, f.y+30, 6, 0, Math.PI*2); ctx.fill(); // Burner
                ctx.fillStyle = '#b0bec5'; ctx.fillRect(f.x+90,f.y+15,40,30); // Sink
                ctx.fillStyle = '#03a9f4'; ctx.beginPath(); ctx.arc(f.x+110, f.y+30, 4, 0, Math.PI*2); ctx.fill(); // Water
            }}
            else if(f.type === "couch") {{
                ctx.fillStyle = '#455a64'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = '#37474f'; ctx.fillRect(f.x,f.y,20,f.h); ctx.fillRect(f.x+f.w-20,f.y,20,f.h);
            }}
            else if(f.type === "tree") {{
                ctx.fillStyle = '#2e7d32'; ctx.beginPath(); ctx.arc(f.x+30,f.y+30,40,0,Math.PI*2); ctx.fill();
                ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(f.x+30,f.y+30,25,0,Math.PI*2); ctx.fill();
            }}
            else {{ ctx.fillStyle = '#555'; ctx.fillRect(f.x,f.y,f.w,f.h); }}
        }});

        // Room Labels
        ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 35px 'Nunito'"; ctx.textAlign="center";
        ctx.fillText("MASTER BEDROOM", 1400, 500); ctx.fillText("LOUNGE", 1400, 700);
        ctx.fillText("KITCHEN", 1000, 900); ctx.fillText("DINING", 1000, 1100);
        ctx.fillText("LIBRARY", 1800, 900); ctx.fillText("STUDY", 1800, 1100);
        ctx.fillText("GRAND HALL", 1400, 1300); ctx.fillText("PICKLEBALL COURT", 350, 1350);

        // Pulsating Interactive Props
        let pulse = Math.sin(Date.now() / 150) * 4;
        interactables.forEach(p => {{
            ctx.fillStyle = "rgba(255, 215, 0, 0.4)";
            ctx.beginPath(); ctx.arc(p.x+12, p.y+12, 20 + pulse, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "rgba(255, 215, 0, 0.8)";
            ctx.beginPath(); ctx.arc(p.x+12, p.y+12, 12, 0, Math.PI*2); ctx.fill();
            if(p.near) {{ ctx.fillStyle = "#fff"; ctx.font = "bold 20px Arial"; ctx.fillText("🔍", p.x+12, p.y-15); }}
        }});

        npcs.forEach(n => {{
            drawCharacter(n.x, n.y, n.data.color, n.data.name);
            if(n.near) {{ ctx.fillStyle = "#fdd835"; ctx.font = "bold 20px Arial"; ctx.fillText("💬", n.x+12, n.y-20); }}
        }});
        
        drawCharacter(player.x, player.y, "#00d2ff", "Shanaya", true);

        // Translucent Fog
        let pRoom = getRoom(player.x + player.w/2, player.y + player.h/2);
        ctx.fillStyle = "rgba(0, 0, 0, 0.65)"; 

        if (pRoom === "Garden") {{
            ctx.fillRect(800, 400, 1200, 1180); 
        }} else {{
            if (pRoom !== "Kitchen") ctx.fillRect(800, 800, 400, 200);
            if (pRoom !== "Dining") ctx.fillRect(800, 1000, 400, 180);
            if (pRoom !== "Library") ctx.fillRect(1600, 800, 400, 200);
            if (pRoom !== "Study") ctx.fillRect(1600, 1000, 400, 180);
            if (pRoom !== "MasterBed") ctx.fillRect(1200, 400, 400, 200);
            if (pRoom !== "Lounge") ctx.fillRect(1200, 600, 400, 200);
            if (pRoom !== "Hall") ctx.fillRect(1200, 800, 400, 780); 
        }}
        ctx.restore(); 
    }}

    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}

    function interact() {{
        let targetProp = interactables.find(p => p.near);
        if(targetProp) {{
            document.getElementById("modal-title").innerText = targetProp.title;
            document.getElementById("modal-text").innerText = targetProp.text;
            document.getElementById("video-container").innerHTML = ""; 
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true; return;
        }}

        let target = npcs.find(n => n.near);
        if(target) {{
            document.getElementById("modal-title").innerText = "Talking to " + target.data.name;
            document.getElementById("modal-text").innerText = '"' + target.data.clue + '"';
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
