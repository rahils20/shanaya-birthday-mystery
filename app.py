import streamlit as st
import streamlit.components.v1 as components
import json
import random

st.set_page_config(page_title="Shanaya's Birthday Mystery", layout="wide")

# =====================================================================
# 🎬 PASTE YOUR YOUTUBE LINKS HERE 🎬
# You can paste ANY YouTube link format here now.
# E.g., "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
# or "https://youtu.be/dQw4w9WgXcQ"
# =====================================================================

VIDEO_LINKS = {
    "Rahil": "https://youtu.be/Iy5IVA1YsZ0",
    "CCTV": "https://youtube.com/shorts/GxdqpSUJ6-Y",
    "Maanav": "https://youtube.com/shorts/82v7Clu82zw",
    "Divya": "https://youtube.com/shorts/esov4ekN_U4",
    "Anoushka": "https://youtu.be/gH8ZwvmjCAE",
    "Manav T": "https://youtube.com/shorts/BNWa3urR7Mg",
    "Selina": "https://youtu.be/lVrMwKIgIno",
    "Panthiv": "https://youtube.com/shorts/nCGuCFt2Enc",
    "Shlokk": "https://youtu.be/GGvGN_xT2Cc",
    "Kshitija": "https://youtu.be/xItmHrKGy58",
    "Pareen": "https://youtu.be/9j_SiPlCNYA",
    "Alisha": "https://youtube.com/shorts/xeYM_-xl7pE",
    "Ishika": "https://youtu.be/OTQnL4-mN4w",
    "Mandira": "https://youtu.be/HGH41tJfEKs",
    "Mom": "https://youtu.be/eJmeRFUMY4s",
    "Dadu": "https://youtu.be/BYVapyQAR0c",
    "Dad": "https://youtube.com/shorts/QkHpilw4rY0",
    "Suchi": "https://youtube.com/shorts/npfQppAsh0I?feature=share",
    "Miloni": "https://youtu.be/lwiMKsqemg4",
    "Rahil Patel": "https://youtu.be/ISOpeP2Oc2Y",
    "Shlok patel": "https://youtu.be/IrKXd_F5unQ",
    "Sahil": "https://youtube.com/shorts/bMzjf1EcNu4",
    "Ryan": "https://youtu.be/6G3ye1aCYgA",
    "Aashna": "https://youtu.be/YQ4-MfeSOXI",
    "Sharvil": "https://youtube.com/shorts/YsFrWMuOnyw",
    "Dua": "https://youtube.com/shorts/LpQZlpSj3UI",
    "Jai Kedia": "https://youtube.com/shorts/Psel2DKnMns?feature=share"
}

# --- YOUTUBE URL AUTO-CONVERTER ---
def fix_youtube_link(url):
    if not url or url == "YOUR_LINK_HERE":
        return "https://www.youtube.com/embed/dQw4w9WgXcQ" # Default Placeholder
    
    # Handle standard watch links
    if "youtube.com/watch?v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    
    # Handle short mobile share links
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
        
    # Handle YouTube Shorts links
    elif "youtube.com/shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
        
    # Return as-is if already an embed link
    return url

# =====================================================================

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

# --- GUEST LIST & NPC DATABASE (30 Characters) ---
colors = ["#e50914", "#9c27b0", "#3f51b5", "#009688", "#ff9800", "#795548", "#607d8b", "#e91e63", "#00bcd4", "#cddc39", "#ff5722"]

npcs_data = [
    {"name": "Rahil", "clue": "Hey babe! I locked the CCTV computer in the Lounge to keep the footage safe. Some of the items I have been using store some secret information. Find the 3 numbers to unlock it!"},
    {"name": "Maanav", "clue": "Happy Birthday! Honestly, I hit a massive tempo sprint session today and my macros are completely depleted. I'd kill for some carbs right now."},
    {"name": "Divya", "clue": "I was in the Library at 11:30 PM. The heavy brass candlestick was on the desk. By 12:15 AM, it was missing!"},
    {"name": "Anoushka", "clue": "I was grabbing a drink near the Dining Room right around midnight. I heard a loud crash coming from the Kitchen. And I saw wet footprints!"},
    {"name": "Manav T", "clue": "I saw someone sprinting away from the West Wing in the dark. I couldn't see their face, but the screen on their Whoop strap was glowing."},
    {"name": "Selina", "clue": "A Whoop strap? That's interesting. Maanav and Shlokk are the only ones here obsessed with tracking their recovery on their Whoops."},
    {"name": "Panthiv", "clue": "Pool party is where it's at! Me and Shlokk have been in the water since 10 PM. He hasn't left the pool deck."},
    {"name": "Shlokk", "clue": "I didn't do it! Yes, I was wearing my Whoop, but Panthiv and I have been doing cannonballs since 11 PM! Look at my hair, it's soaking wet."},
    {"name": "Kshitija", "clue": "It's true, Shlokk hasn't left the pool. But I noticed Maanav wasn't with us OR the pickleball crew at midnight. Where was he?"},
    {"name": "Pareen", "clue": "I saw Maanav earlier staring at the dessert menu on his phone. I thought he was doing strict Keto?"},
    {"name": "Alisha", "clue": "Whoever broke the lock on the cake fridge must have used something super heavy and blunt. Definitely not a knife or a dagger."},
    {"name": "Ishika", "clue": "I was dropping my bag in the Master Bedroom. Did you see the graduation photo? The note on it said 'The day we celebrated.' When did you graduate again? June what?"},
    {"name": "Mandira", "clue": "I was just touching up my makeup in the Bathroom. Did you notice the sticky note on your Bum Bum Cream? It said: 'The iconic scent number on the front of the tub.'"},
    {"name": "Mom", "clue": "Shanaya beta, you look so beautiful! Please be careful walking in the Hallway, someone spilled a massive cooler of ice water right in the middle around 11:30 PM."},
    {"name": "Dadu", "clue": "Is it time for dinner yet? All this running around is making me dizzy. Happy Birthday, beta!"},
    {"name": "Dad", "clue": "Happy Birthday Shanaya! Has anyone seen my glasses? I can't read this menu."},
    {"name": "Suchi", "clue": "Omg this party is so aesthetic! Need to take some pictures for the gram. Happy Birthday!"},
    {"name": "Miloni", "clue": "Happy birthday girl!! Love the decor in here."},
    {"name": "Rahil Patel", "clue": "Great party! The food is amazing. Happy Birthday!"},
    {"name": "Shlok patel", "clue": "Are we playing pickleball later? Happy Birthday Shanaya!"},
    {"name": "Sahil", "clue": "I'm just here for the free drinks. Happy B-Day!"},
    {"name": "Ryan", "clue": "Happy Birthday! I've literally just been wandering around looking for the bathroom."},
    {"name": "Aashna", "clue": "This house is huge! I keep getting lost looking for the pool. Happy Birthday Shanaya!"},
    {"name": "Sharvil", "clue": "Tequilla?"},
    {"name": "Dua", "clue": "Did you see the Dining Room table? There are empty boxes of Sushi. The delivery guy left a weird note: 'Subtract the number of sushi boxes (3) from the delivery hour (23:00).'"},
    {"name": "Jai Kedia", "clue": "Can we play Mafia now?'"}
]

# Map the links from the dictionary at the top to the characters using the auto-fixer
for npc in npcs_data:
    npc["color"] = random.choice(colors)
    raw_link = VIDEO_LINKS.get(npc["name"], "YOUR_LINK_HERE")
    npc["video"] = fix_youtube_link(raw_link)

all_names_json = json.dumps([n["name"] for n in npcs_data])

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
        text-align: center; width: 70%; max-width: 600px; z-index: 100; box-shadow: 0px 20px 60px rgba(0,0,0,0.95); max-height: 90vh; overflow-y: auto;
    }}
    #dialogue-box h2 {{ color: #fdd835; margin-top: 0; font-family: 'Cinzel', serif; line-height: 1.2;}}
    .btn {{ background: #fdd835; color: #111; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 16px; margin-top: 15px; width: 100%; }}
    .btn:hover {{ background: #fff176; }}

    #passcode-box {{
        display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background: #111; border: 3px solid #00d2ff; border-radius: 12px; padding: 30px;
        text-align: center; width: 80%; max-width: 450px; z-index: 110; box-shadow: 0px 20px 60px rgba(0,0,0,0.95);
    }}
    #passcode-box input {{ width: 80%; padding: 15px; font-size: 20px; text-align: center; border-radius: 8px; border: 2px solid #555; background: #222; color: white; margin: 15px 0; font-weight: bold; letter-spacing: 5px;}}
    #passcode-box input:focus {{ outline: none; border-color: #00d2ff; }}

    #clue-pad-overlay {{
        display: none; position: absolute; top: 20px; left: 20px; width: calc(100% - 40px); height: calc(100% - 40px);
        background: rgba(20, 20, 25, 0.98); border: 2px solid #555; border-radius: 12px; padding: 20px; z-index: 90; box-sizing: border-box; overflow-y: auto;
    }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
    .pad-row {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; padding: 5px 0; }}
    .toggle-cycle {{ background: #222; border: 1px solid #444; color: white; width: 35px; height: 30px; border-radius: 4px; cursor: pointer; font-weight: bold; }}
    .toggle-cycle.x {{ background: rgba(255,0,0,0.2); border-color: red; color: red; }}
    .toggle-cycle.check {{ background: rgba(0,255,0,0.2); border-color: lime; color: lime; }}
    
    #progress-tracker {{ position: absolute; top: 15px; right: 20px; background: rgba(0,0,0,0.8); padding: 10px 20px; border-radius: 8px; font-weight: bold; border: 2px solid #fdd835; z-index: 50;}}
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="1000" height="680"></canvas>
    <div id="progress-tracker">Guests Interrogated: <span id="guest-count">0</span>/26</div>
    
    <div id="dialogue-box">
        <h2 id="modal-title">Name</h2>
        <div id="video-container" style="border-radius: 8px; overflow: hidden; margin-top: 10px;"></div>
        <p id="modal-text" style="font-size: 18px; color: #eee; margin: 15px 0; font-weight: bold; line-height: 1.5;"></p>
        <button class="btn" onclick="closeModal()">Close & Resume</button>
    </div>

    <div id="passcode-box">
        <h2 style="color: #00d2ff; font-family: 'Cinzel', serif; margin-top: 0;">SECURITY TERMINAL</h2>
        <p style="color: #ccc; font-size: 14px;">Hint: Bum Bum Cream Scent + (Delivery Hour - Sushi Boxes) + Grad Day</p>
        <p id="passcode-error" style="color: #ff5252; font-weight: bold; display: none; margin-bottom: 0;">ACCESS DENIED. INCORRECT CODE.</p>
        <input type="text" id="passcode-input" placeholder="000000" maxlength="6" autocomplete="off">
        <button class="btn" style="background: #00d2ff; color: black;" onclick="checkPasscode()">UNLOCK SYSTEM</button>
        <button class="btn" style="background: #444; color: white; margin-top: 10px;" onclick="closePasscode()">CANCEL</button>
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

    const MAP_W = 3200; const MAP_H = 2600;
    const player = {{ x: 1500, y: 2200, w: 24, h: 32, speed: 7 }};
    const keys = {{}};
    let modalOpen = false; let padOpen = false;
    
    const interrogatedGuests = new Set();
    const allNamesList = {all_names_json};
    const TOTAL_GUESTS = 26;

    const rawNpcs = {json.dumps(npcs_data)};
    const npcs = [];
    const walls = []; const furniture = []; const interactables = [];

    function W(x, y, w, h) {{ walls.push({{x, y, w, h}}); }}
    function addFurn(x, y, w, h, type, solid=true) {{ furniture.push({{x, y, w, h, type, solid}}); }}
    function addProp(x, y, title, text, type="prop", radius=130) {{ interactables.push({{x, y, w: 24, h: 24, title, text, type, radius, near: false}}); }}

    function isColliding(r1, r2) {{ return r1.x < r2.x + r2.w && r1.x + r1.w > r2.x && r1.y < r2.y + r2.h && r1.y + r1.h > r2.y; }}
    function canMove(newX, newY, w, h) {{
        let pNext = {{ x: newX, y: newY, w: w, h: h }};
        if(newX < 20 || newX + w > MAP_W-20 || newY < 20 || newY + h > MAP_H-20) return false;
        for(let wl of walls) if(isColliding(pNext, wl)) return false;
        for(let f of furniture) if(f.solid && isColliding(pNext, f)) return false;
        return true;
    }}

    // --- ARCHITECTURE ---
    W(0, 0, MAP_W, 20); W(0, MAP_H-20, 1400, 20); W(1600, MAP_H-20, 1600, 20); 
    W(0, 0, 20, MAP_H); W(MAP_W-20, 0, 20, MAP_H);

    W(1000, 400, 1000, 20); W(1000, 400, 20, 380); W(1980, 400, 20, 380);  
    W(1000, 780, 300, 20); W(1450, 780, 550, 20);  
    W(1600, 420, 20, 80); W(1600, 600, 20, 50); W(1600, 730, 20, 50); W(1620, 600, 360, 20);  

    W(600, 800, 400, 20); W(600, 800, 20, 1000); W(600, 1800, 600, 20);  
    W(620, 1100, 560, 20); W(620, 1400, 560, 20);  
    W(1180, 800, 20, 100); W(1180, 1050, 20, 150); W(1180, 1350, 20, 200); W(1180, 1700, 20, 100); 

    W(1800, 800, 600, 20); W(2380, 800, 20, 1000); W(1800, 1800, 600, 20); W(1820, 1300, 560, 20); 
    W(1800, 800, 20, 200); W(1800, 1150, 20, 350); W(1800, 1650, 20, 150); 
    W(1200, 1800, 200, 20); W(1600, 1800, 200, 20); 

    // --- FURNITURE ---
    addFurn(100, 1000, 450, 700, "pickleball", false);
    addFurn(2450, 900, 700, 800, "deck", false);
    addFurn(2550, 1000, 400, 400, "pool", false); 
    addFurn(2850, 1500, 180, 80, "bar");
    addFurn(2550, 1500, 60, 100, "deckchair"); addFurn(2650, 1500, 60, 100, "deckchair");

    addFurn(1250, 450, 200, 220, "bed");
    addFurn(1050, 650, 150, 80, "couch");
    addFurn(1150, 480, 60, 40, "nightstand"); addFurn(1480, 480, 60, 40, "nightstand");
    addFurn(1650, 420, 300, 50, "wardrobe");
    addFurn(1650, 530, 250, 50, "clothing_rack");
    addFurn(1850, 620, 100, 150, "bathtub"); 
    addFurn(1650, 620, 120, 60, "vanity");
    addFurn(1900, 750, 50, 40, "toilet");

    addFurn(800, 950, 200, 80, "kitchen_island"); 
    addFurn(620, 820, 60, 100, "fridge");
    addFurn(620, 950, 60, 120, "counters");
    addFurn(750, 1200, 300, 120, "dining_table");   
    addFurn(800, 1500, 250, 100, "lounge_sofa");
    
    addFurn(650, 1600, 120, 80, "computer_desk");

    addFurn(2100, 820, 40, 400, "bookshelf_vert");     
    addFurn(1850, 1150, 300, 40, "bookshelf");
    addFurn(1900, 950, 100, 100, "reading_chair");
    addFurn(2000, 1450, 160, 80, "desk");          
    addFurn(2200, 1450, 60, 60, "plant");
    
    addFurn(1300, 1450, 180, 140, "piano");       
    addFurn(1300, 850, 400, 900, "red_carpet", false);

    // --- GLOWING PROPS ---
    addProp(650, 1600, "Security Computer", "System Locked.", "computer", 140);
    addProp(900, 970, "Empty Stand", "Wait... this is where the Paleo Bakes sugar-free chocolate cake was supposed to be! It's completely missing, but there is a smear of sugar-free icing leading towards the door.", "prop");
    addProp(1700, 640, "Vanity Setup", "A very specific skincare regimen: CeraVe face wash for normal to oily skin, Isdin Fusion Water sunscreen, and a tub of Brazilian Bum Bum Cream 62.", "prop");
    addProp(1300, 480, "Graduation Photo", "A framed photo from your graduation ceremony on June 16th.", "prop");
    addProp(850, 1230, "Sushi Delivery", "Exactly 3 empty boxes of Sushi. The receipt shows a delivery time of 23:00.", "prop");
    addProp(2600, 1520, "Poolside Items", "A Whoop strap and some Speedo swimming gear left by the water.", "prop");
    
    // Spawn Trees Safely
    for(let i=0; i<80; i++) {{
        let tx = 100 + Math.random()*3000; let ty = 100 + Math.random()*2400;
        if(tx > 500 && tx < 2500 && ty > 300 && ty < 1900) continue; 
        if(tx > 2400 && ty > 800) continue; 
        if(tx < 600 && ty > 900 && ty < 1800) continue; 
        if(tx > 1300 && tx < 1700 && ty > 1800) continue; 
        if(!canMove(tx, ty, 60, 60)) continue;
        addFurn(tx, ty, 60, 60, "tree");
    }}

    // Spawn NPCs Safely
    const spawnZones = [
        {{x: 650, y: 850, w: 400, h: 200}}, {{x: 650, y: 1150, w: 400, h: 200}}, {{x: 650, y: 1450, w: 400, h: 200}}, 
        {{x: 1850, y: 850, w: 400, h: 400}}, {{x: 1850, y: 1350, w: 400, h: 300}}, {{x: 1250, y: 850, w: 400, h: 800}}, 
        {{x: 2500, y: 1000, w: 200, h: 300}}, {{x: 200, y: 1000, w: 300, h: 400}}
    ];

    rawNpcs.forEach(data => {{
        let placed = false; let attempts = 0;
        while(!placed && attempts < 100) {{
            let zone = spawnZones[Math.floor(Math.random() * spawnZones.length)];
            let nx = zone.x + Math.random() * zone.w; let ny = zone.y + Math.random() * zone.h;
            if(canMove(nx, ny, 24, 32)) {{
                npcs.push({{ x: nx, y: ny, w: 24, h: 32, data: data, vx: 0, vy: 0, timer: 0, near: false }});
                placed = true;
            }}
            attempts++;
        }}
    }});

    // --- ENGINE LOGIC ---
    window.addEventListener("keydown", (e) => {{
        keys[e.code] = true;
        if(e.code === "Space" && !modalOpen && !padOpen) interact();
        if(e.code === "KeyC") togglePad();
        if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space","KeyW","KeyA","KeyS","KeyD"].includes(e.code)) e.preventDefault();
    }});
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    function getRoom(px, py) {{
        if(px > 600 && px < 1200 && py > 800 && py < 1100) return "Kitchen";
        if(px > 600 && px < 1200 && py > 1100 && py < 1400) return "Dining";
        if(px > 600 && px < 1200 && py > 1400 && py < 1800) return "Lounge";
        if(px > 1800 && px < 2400 && py > 800 && py < 1300) return "Library";
        if(px > 1800 && px < 2400 && py > 1300 && py < 1800) return "Study";
        if(px > 1000 && px < 1600 && py > 400 && py < 800) return "MasterBed";
        if(px > 1600 && px < 2000 && py > 400 && py < 600) return "WIW";
        if(px > 1600 && px < 2000 && py > 600 && py < 800) return "Bathroom";
        if(px > 1200 && px < 1800 && py > 800 && py < 1800) return "Hall";
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
            prop.near = Math.hypot((player.x + player.w/2) - (prop.x + 12), (player.y + player.h/2) - (prop.y + 12)) < prop.radius;
        }});
    }}

    function drawCharacter(x, y, color, name, isPlayer=false) {{
        ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 4;
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
        ctx.fillStyle = "#3a5f2b"; ctx.fillRect(0, 0, canvas.width, canvas.height); 
        
        ctx.save();
        let camX = canvas.width/2 - (player.x + player.w/2);
        let camY = canvas.height/2 - (player.y + player.h/2);
        ctx.translate(camX, camY);

        ctx.fillStyle = "#6B4423"; ctx.fillRect(1450, 1780, 100, 820); 
        ctx.fillStyle = "#111"; ctx.fillRect(1380, MAP_H-30, 40, 40); ctx.fillRect(1580, MAP_H-30, 40, 40); 
        ctx.fillStyle = "#333"; ctx.fillRect(1420, MAP_H-15, 160, 10); 

        ctx.fillStyle = "#8b5a2b"; 
        ctx.fillRect(1000, 400, 1000, 400); 
        ctx.fillRect(600, 800, 1800, 1000); 
        ctx.fillStyle = "#cfd8dc"; ctx.fillRect(1600, 400, 400, 400); 

        ctx.fillStyle = "#1a1a1a";
        ctx.shadowColor = 'rgba(0,0,0,0.8)'; ctx.shadowBlur = 12;
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.shadowBlur = 0;

        furniture.forEach(f => {{
            ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 4;
            if(f.type === "pool") {{
                ctx.fillStyle = '#e0e0e0'; ctx.fillRect(f.x-10, f.y-10, f.w+20, f.h+20); 
                let grad = ctx.createLinearGradient(f.x, f.y, f.x+f.w, f.y+f.h);
                grad.addColorStop(0, '#00a8ff'); grad.addColorStop(1, '#0097e6');
                ctx.fillStyle = grad; ctx.fillRect(f.x, f.y, f.w, f.h); 
                ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 3; 
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+40); ctx.lineTo(f.x+150, f.y+60); ctx.stroke();
                ctx.fillStyle = "#e91e63"; ctx.beginPath(); ctx.arc(f.x+f.w/2, f.y+f.h/2, 25, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "pickleball") {{
                ctx.fillStyle = "#1b5e20"; ctx.fillRect(f.x, f.y, f.w, f.h); 
                ctx.fillStyle = "#1565c0"; ctx.fillRect(f.x+40, f.y+40, f.w-80, f.h-80); 
                ctx.strokeStyle = "white"; ctx.lineWidth = 4; ctx.strokeRect(f.x+40, f.y+40, f.w-80, f.h-80); 
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2); ctx.lineTo(f.x+f.w-40, f.y+f.h/2); ctx.stroke(); 
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2-100); ctx.lineTo(f.x+f.w-40, f.y+f.h/2-100); ctx.stroke(); 
                ctx.beginPath(); ctx.moveTo(f.x+40, f.y+f.h/2+100); ctx.lineTo(f.x+f.w-40, f.y+f.h/2+100); ctx.stroke(); 
                ctx.beginPath(); ctx.moveTo(f.x+f.w/2, f.y+40); ctx.lineTo(f.x+f.w/2, f.y+f.h/2-100); ctx.stroke(); 
                ctx.beginPath(); ctx.moveTo(f.x+f.w/2, f.y+f.h/2+100); ctx.lineTo(f.x+f.w/2, f.y+f.h-40); ctx.stroke(); 
            }}
            else if(f.type === "deck") {{ ctx.fillStyle = '#d4a373'; ctx.fillRect(f.x, f.y, f.w, f.h); }}
            else if(f.type === "bar") {{
                ctx.fillStyle = '#5d4037'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = '#222'; ctx.beginPath(); ctx.arc(f.x+30, f.y-15, 15, 0, Math.PI*2); ctx.fill(); 
                ctx.beginPath(); ctx.arc(f.x+90, f.y-15, 15, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(f.x+150, f.y-15, 15, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "deckchair") {{ ctx.fillStyle = '#fff'; ctx.fillRect(f.x, f.y, f.w, f.h); ctx.fillStyle = '#03a9f4'; ctx.fillRect(f.x+5, f.y+5, f.w-10, f.h-10);}}
            else if(f.type === "dining_table") {{
                ctx.fillStyle = '#3E2723'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = 'white'; 
                for(let i=0; i<4; i++) {{
                    ctx.beginPath(); ctx.arc(f.x+40 + (i*70), f.y+20, 10, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(f.x+40 + (i*70), f.y+100, 10, 0, Math.PI*2); ctx.fill();
                }}
            }}
            else if(f.type === "computer_desk") {{
                ctx.fillStyle = '#2c3e50'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = '#ecf0f1'; ctx.fillRect(f.x+30, f.y+20, 60, 40); 
                ctx.fillStyle = '#3498db'; ctx.fillRect(f.x+35, f.y+25, 50, 30); 
            }}
            else if(f.type === "bed") {{
                ctx.fillStyle = '#3e2723'; ctx.fillRect(f.x,f.y,f.w,f.h); 
                ctx.fillStyle = '#fafafa'; ctx.fillRect(f.x+8,f.y+8,f.w-16,f.h-16); 
                ctx.fillStyle = '#e0e0e0'; ctx.fillRect(f.x+20,f.y+20,60,40); ctx.fillRect(f.x+120,f.y+20,60,40); 
                ctx.fillStyle = '#1565c0'; ctx.fillRect(f.x+8,f.y+80,f.w-16,f.h-88); 
            }}
            else if(f.type === "kitchen_island") {{
                ctx.fillStyle = '#eceff1'; ctx.fillRect(f.x,f.y,f.w,f.h); 
                ctx.fillStyle = '#37474f'; ctx.fillRect(f.x+20,f.y+20,50,40); 
                ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(f.x+35, f.y+40, 8, 0, Math.PI*2); ctx.fill(); 
                ctx.fillStyle = '#b0bec5'; ctx.fillRect(f.x+120,f.y+20,50,40); 
            }}
            else if(f.type === "lounge_sofa") {{
                ctx.fillStyle = '#455a64'; ctx.fillRect(f.x,f.y,f.w,f.h);
                ctx.fillStyle = '#37474f'; ctx.fillRect(f.x,f.y,25,f.h); ctx.fillRect(f.x+f.w-25,f.y,25,f.h); ctx.fillRect(f.x,f.y,f.w,25);
            }}
            else if(f.type === "bathtub") {{
                ctx.fillStyle = 'white'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = '#e0e0e0'; ctx.fillRect(f.x+10, f.y+10, f.w-20, f.h-20);
            }}
            else if(f.type === "vanity") {{
                ctx.fillStyle = '#5D4037'; ctx.fillRect(f.x, f.y, f.w, f.h);
                ctx.fillStyle = 'white'; ctx.beginPath(); ctx.arc(f.x+f.w/2, f.y+f.h/2, 15, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "toilet") {{
                ctx.fillStyle = 'white'; ctx.fillRect(f.x, f.y, f.w, 20);
                ctx.beginPath(); ctx.arc(f.x+f.w/2, f.y+40, 20, 0, Math.PI*2); ctx.fill();
            }}
            else if(f.type === "wardrobe") {{ ctx.fillStyle = '#4E342E'; ctx.fillRect(f.x, f.y, f.w, f.h); }}
            else if(f.type === "clothing_rack") {{
                ctx.fillStyle = '#757575'; ctx.fillRect(f.x, f.y+f.h/2-2, f.w, 4);
                ctx.fillStyle = '#c62828'; ctx.fillRect(f.x+20, f.y+10, 10, 30); ctx.fillStyle = '#1565c0'; ctx.fillRect(f.x+40, f.y+10, 10, 30);
            }}
            else if(f.type === "tree") {{
                ctx.fillStyle = '#2e7d32'; ctx.beginPath(); ctx.arc(f.x+30,f.y+30,45,0,Math.PI*2); ctx.fill();
                ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(f.x+30,f.y+30,25,0,Math.PI*2); ctx.fill();
            }}
            else {{ ctx.fillStyle = '#555'; ctx.fillRect(f.x,f.y,f.w,f.h); }}
            
            ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
        }});

        ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 40px 'Nunito'"; ctx.textAlign="center";
        ctx.fillText("MASTER BEDROOM", 1300, 600); 
        ctx.fillText("BATHROOM", 1800, 720); ctx.fillText("WALK-IN", 1800, 520);
        ctx.fillText("KITCHEN", 900, 950); ctx.fillText("DINING", 900, 1250); ctx.fillText("LOUNGE", 900, 1600);
        ctx.fillText("LIBRARY", 2100, 1050); ctx.fillText("STUDY", 2100, 1550);
        ctx.fillText("GRAND HALL", 1500, 1300); ctx.fillText("PICKLEBALL COURT", 350, 1400);

        let pulse = Math.sin(Date.now() / 150) * 4;
        interactables.forEach(p => {{
            ctx.fillStyle = p.type === "computer" ? "rgba(0, 215, 255, 0.4)" : "rgba(255, 215, 0, 0.4)";
            ctx.beginPath(); ctx.arc(p.x+12, p.y+12, 20 + pulse, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = p.type === "computer" ? "rgba(0, 215, 255, 0.8)" : "rgba(255, 215, 0, 0.8)";
            ctx.beginPath(); ctx.arc(p.x+12, p.y+12, 12, 0, Math.PI*2); ctx.fill();
            if(p.near) {{ ctx.fillStyle = "#fff"; ctx.font = "bold 20px Arial"; ctx.fillText("🔍", p.x+12, p.y-15); }}
        }});

        npcs.forEach(n => {{
            drawCharacter(n.x, n.y, n.data.color, n.data.name);
            if(n.near) {{ ctx.fillStyle = "#fdd835"; ctx.font = "bold 20px Arial"; ctx.fillText("💬", n.x+12, n.y-20); }}
        }});
        
        drawCharacter(player.x, player.y, "#00d2ff", "Shanaya", true);

        let pRoom = getRoom(player.x + player.w/2, player.y + player.h/2);
        ctx.fillStyle = "rgba(0, 0, 0, 0.65)"; 

        if (pRoom === "Garden") {{
            ctx.fillRect(600, 400, 1800, 1400); 
        }} else {{
            if (pRoom !== "Kitchen") ctx.fillRect(600, 800, 600, 300);
            if (pRoom !== "Dining") ctx.fillRect(600, 1100, 600, 300);
            if (pRoom !== "Lounge") ctx.fillRect(600, 1400, 600, 400);
            if (pRoom !== "Library") ctx.fillRect(1800, 800, 600, 500);
            if (pRoom !== "Study") ctx.fillRect(1800, 1300, 600, 500);
            if (pRoom !== "MasterBed") ctx.fillRect(1000, 400, 600, 400);
            if (pRoom !== "WIW") ctx.fillRect(1600, 400, 400, 200);
            if (pRoom !== "Bathroom") ctx.fillRect(1600, 600, 400, 200);
            if (pRoom !== "Hall") ctx.fillRect(1200, 800, 600, 1000); 
        }}
        ctx.restore(); 
    }}

    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}

    function interact() {{
        let targetProp = interactables.find(p => p.near);
        if(targetProp) {{
            if(targetProp.type === "computer") {{
                if(interrogatedGuests.size < TOTAL_GUESTS) {{
                    let missing = allNamesList.filter(n => !interrogatedGuests.has(n));
                    document.getElementById("modal-title").innerText = targetProp.title;
                    document.getElementById("modal-text").innerText = `Access Denied. You must interrogate all guests first to unlock the security system. (Progress: ${{interrogatedGuests.size}} / ${{TOTAL_GUESTS}})\n\nMissing statements from:\n${{missing.join(", ")}}`;
                    document.getElementById("video-container").innerHTML = ""; 
                    document.getElementById("dialogue-box").style.display = "block";
                }} else {{
                    document.getElementById("passcode-box").style.display = "block";
                    document.getElementById("passcode-input").value = "";
                    document.getElementById("passcode-error").style.display = "none";
                    document.getElementById("passcode-input").focus();
                }}
            }} else {{
                document.getElementById("modal-title").innerText = targetProp.title;
                document.getElementById("modal-text").innerText = targetProp.text;
                document.getElementById("video-container").innerHTML = ""; 
                document.getElementById("dialogue-box").style.display = "block";
            }}
            modalOpen = true; return;
        }}

        let target = npcs.find(n => n.near);
        if(target) {{
            interrogatedGuests.add(target.data.name);
            document.getElementById("guest-count").innerText = interrogatedGuests.size;
            
            document.getElementById("modal-title").innerText = "Talking to " + target.data.name;
            document.getElementById("modal-text").innerText = '"' + target.data.clue + '"';
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="280" src="${{target.data.video}}?autoplay=1" frameborder="0"></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
            modalOpen = true;
        }}
    }}

    window.checkPasscode = function() {{
        let code = document.getElementById("passcode-input").value;
        if(code === "622016") {{
            document.getElementById("passcode-box").style.display = "none";
            document.getElementById("modal-title").innerText = "SYSTEM UNLOCKED - CCTV FOOTAGE";
            document.getElementById("modal-text").innerText = "The camera feed is heavily glitched, but you pull a 5-second clip from exactly 11:58 PM. You cannot see the culprit's face. However, you clearly see them carrying a heavy brass CANDLESTICK from the Library. As they pry open the cake box in the KITCHEN, a glowing WHOOP strap illuminates their wrist. They grab a slice of the Paleo Bakes cake and sprint out!";
            
            // This pulls Rahil's video from the links dictionary to act as the "CCTV footage" reveal
            let cctv_link = "{fix_youtube_link(VIDEO_LINKS.get('CCTV', ''))}"; 
            
            document.getElementById("video-container").innerHTML = `<iframe width="100%" height="280" src="${{cctv_link}}?autoplay=1" frameborder="0"></iframe>`;
            document.getElementById("dialogue-box").style.display = "block";
        }} else {{
            document.getElementById("passcode-error").style.display = "block";
        }}
    }}

    window.closePasscode = function() {{
        document.getElementById("passcode-box").style.display = "none";
        setTimeout(() => modalOpen = false, 200);
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
        const s = {all_names_json};
        const w = {json.dumps(["Candlestick", "Poison", "Rope", "Axe", "Dagger"])};
        const r = {json.dumps(["Kitchen", "Dining", "Library", "Study", "Lounge", "MasterBed", "Bathroom", "WIW", "Grand Hall"])};
        
        function buildCol(id, list, prefix) {{
            let col = document.getElementById(id);
            list.forEach(item => {{
                let uid = prefix + item.split(' ').join('');
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
with col1: guess_who = st.selectbox("Suspect", ["Select"] + [n["name"] for n in npcs_data])
with col2: guess_where = st.selectbox("Location", ["Select", "Kitchen", "Dining", "Library", "Study", "MasterBed", "Lounge", "Bathroom", "WIW", "Grand Hall"])
with col3: guess_weapon = st.selectbox("Weapon", ["Select", "Candlestick", "Poison", "Rope", "Axe", "Dagger"])
    
if st.button("MAKE ACCUSATION", use_container_width=True, type="primary"):
    if guess_who == "Maanav" and guess_where == "Kitchen" and guess_weapon == "Candlestick":
        st.success("🎉 CORRECT! You cracked the case, Shanaya! Happy Birthday! 🎂")
        st.markdown("### 🎁 YOUR SURPRISE GIFT VOUCHER: `HAPPY-B-DAY-SHANAYA-100`")
        st.balloons()
    else:
        st.error("Not quite! Keep exploring the mansion, check your Detective Pad, or check the CCTV footage on the Lounge computer.")
