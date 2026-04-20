```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive LED Board", layout="centered")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background: #141414 !important;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1100px;
}
iframe {
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)

html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<style>
    :root{
        --bg:#141414;
        --panel:#181818;
        --panel2:#202020;
        --tile-border:#222222;
        --led-on:#F9ED32;
        --led-off:#3B3C3D;
        --active:#4a4a4a;
        --text:#f2f2f2;
        --muted:#bdbdbd;
        --btn:#F9ED32;
        --btn-text:#111111;
    }

    * { box-sizing: border-box; }

    html, body {
        margin: 0;
        padding: 0;
        background: var(--bg);
        color: var(--text);
        font-family: Arial, Helvetica, sans-serif;
    }

    .app {
        width: 100%;
        max-width: 1100px;
        margin: 0 auto;
        padding: 10px;
    }

    .board-shell {
        background: var(--bg);
        border-radius: 16px;
        padding: 10px;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        border: 1px solid #1e1e1e;
    }

    canvas {
        background: var(--bg);
        display: block;
        margin: 0 auto;
        border-radius: 12px;
        box-shadow: inset 0 0 30px #000;
        touch-action: manipulation;
        max-width: 100%;
        height: auto;
    }

    .topbar {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin: 12px 0 10px;
    }

    .status-card {
        background: var(--panel);
        border-radius: 12px;
        padding: 12px 14px;
        border: 1px solid #242424;
    }

    .status-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .status-sub {
        font-size: 13px;
        color: var(--muted);
    }

    .controls {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }

    .row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }

    button, input, select, label.toggle-wrap {
        appearance: none;
        border: none;
        border-radius: 12px;
        font-size: 15px;
        min-height: 46px;
    }

    button {
        padding: 12px 16px;
        font-weight: 700;
        cursor: pointer;
    }

    .primary {
        background: var(--btn);
        color: var(--btn-text);
    }

    .secondary {
        background: #2a2a2a;
        color: #ffffff;
    }

    .danger {
        background: #3a2424;
        color: #fff;
    }

    .active-btn {
        outline: 2px solid var(--led-on);
        outline-offset: 0;
    }

    .field {
        display: flex;
        align-items: center;
        gap: 8px;
        background: var(--panel);
        color: #fff;
        padding: 8px 12px;
        border: 1px solid #242424;
        border-radius: 12px;
    }

    .field span {
        color: var(--muted);
        font-size: 14px;
        white-space: nowrap;
    }

    input[type="number"] {
        width: 110px;
        padding: 10px 12px;
        background: #111;
        color: #fff;
        border: 1px solid #333;
        outline: none;
    }

    input[type="checkbox"] {
        width: 18px;
        height: 18px;
        accent-color: var(--led-on);
    }

    .help {
        margin-top: 12px;
        text-align: center;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.45;
    }

    .mobile-pad {
        display: none;
        margin-top: 12px;
        gap: 8px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .mobile-pad button {
        min-width: 60px;
        padding: 12px 14px;
    }

    @media (max-width: 768px) {
        .app {
            padding: 6px;
        }

        .controls, .row {
            gap: 8px;
        }

        button {
            width: 100%;
        }

        .field {
            width: 100%;
            justify-content: space-between;
        }

        .mobile-pad {
            display: flex;
        }

        .mobile-pad button.small {
            width: calc(33.333% - 6px);
            min-width: unset;
        }

        .mobile-pad button.wide {
            width: calc(66.666% - 6px);
            min-width: unset;
        }
    }
</style>
</head>
<body>
<div class="app">
    <div class="board-shell">
        <canvas id="ledBoard"></canvas>
    </div>

    <div class="topbar">
        <div class="status-card">
            <div class="status-title" id="sceneStatus">Scene 1 of 1</div>
            <div class="status-sub" id="sceneDetails">Mode: Text Edit | Flash: Off | Duration: 1000 ms</div>
        </div>
    </div>

    <div class="controls">
        <button class="secondary" id="prevSceneBtn">Previous Scene</button>
        <button class="secondary" id="nextSceneBtn">Next Scene</button>
        <button class="secondary" id="addScenesBtn">Add Multiple Scenes</button>
        <button class="secondary" id="duplicateSceneBtn">Duplicate Scene</button>
        <button class="danger" id="deleteSceneBtn">Delete Scene</button>
    </div>

    <div class="row">
        <button class="secondary active-btn" id="textModeBtn">Text Mode</button>
        <button class="secondary" id="solidModeBtn">Solid Tile Mode</button>
        <button class="secondary" id="flashBtn">Flash This Scene: Off</button>
        <div class="field">
            <span>Scene Duration</span>
            <input type="number" id="durationInput" min="200" step="100" value="1000">
        </div>
        <label class="field">
            <span>Loop Scenes</span>
            <input type="checkbox" id="loopCheckbox" checked>
        </label>
    </div>

    <div class="controls">
        <button class="primary" id="playBtn">Play</button>
        <button class="secondary" id="stopBtn">Stop</button>
        <button class="primary" id="downloadPngBtn">Download Image (PNG)</button>
        <button class="primary" id="downloadVideoBtn">Download Video (.webm)</button>
        <button class="secondary" id="clearSceneBtn">Clear Scene</button>
    </div>

    <div class="mobile-pad">
        <button class="small secondary" data-key="←">←</button>
        <button class="small secondary" data-key="→">→</button>
        <button class="small secondary" data-key="↵">↵</button>
        <button class="wide secondary" data-key="SPACE">Space</button>
        <button class="small secondary" data-key="⌫">⌫</button>
    </div>

    <div class="help">
        Text Mode lets you type letters into tiles. Solid Tile Mode lets you tap one or multiple tiles and make the whole tile fully lit. Scenes can flash and play in sequence. PNG downloads without the highlight box. Video exports as .webm.
    </div>
</div>

<script>
// ---------- COLORS ----------
const LED_ON   = "#F9ED32";
const LED_OFF  = "#3B3C3D";
const BG_COLOR = "#141414";
const GAP_LINE = "#222222";
const ACTIVE_COLOR = "#4a4a4a";

// ---------- GRID ----------
const ROWS = 4, COLS = 10;
const DOT_W = 5, DOT_H = 7;
const DOT_SIZE = 10, DOT_GAP = 4;
const TILE_PAD = 6, TILE_GAP = 6, OUTER_PAD = 10;

// ---------- GEOMETRY ----------
function tileW(){ return DOT_W * DOT_SIZE + (DOT_W - 1) * DOT_GAP + 2 * TILE_PAD; }
function tileH(){ return DOT_H * DOT_SIZE + (DOT_H - 1) * DOT_GAP + 2 * TILE_PAD; }
const TW = tileW(), TH = tileH();
const BOARD_W = OUTER_PAD * 2 + COLS * TW + (COLS - 1) * TILE_GAP;
const BOARD_H = OUTER_PAD * 2 + ROWS * TH + (ROWS - 1) * TILE_GAP;

// ---------- FONT ----------
const FONT = {
" ":["00000","00000","00000","00000","00000","00000","00000"],
"A":["01110","10001","11111","10001","10001","10001","10001"],
"B":["11110","10001","11110","10001","10001","10001","11110"],
"C":["01110","10001","10000","10000","10000","10001","01110"],
"D":["11110","10001","10001","10001","10001","10001","11110"],
"E":["11111","10000","11110","10000","10000","10000","11111"],
"F":["11111","10000","11110","10000","10000","10000","10000"],
"G":["01110","10001","10000","10111","10001","10001","01110"],
"H":["10001","10001","11111","10001","10001","10001","10001"],
"I":["01110","00100","00100","00100","00100","00100","01110"],
"J":["00001","00001","00001","10001","10001","10001","01110"],
"K":["10001","10010","11100","10100","10010","10001","10001"],
"L":["10000","10000","10000","10000","10000","10000","11111"],
"M":["10001","11011","10101","10101","10001","10001","10001"],
"N":["10001","11001","10101","10011","10001","10001","10001"],
"O":["01110","10001","10001","10001","10001","10001","01110"],
"P":["11110","10001","11110","10000","10000","10000","10000"],
"Q":["01110","10001","10001","10001","10101","10010","01101"],
"R":["11110","10001","11110","10100","10010","10001","10001"],
"S":["01111","10000","10000","01110","00001","00001","11110"],
"T":["11111","00100","00100","00100","00100","00100","00100"],
"U":["10001","10001","10001","10001","10001","10001","01110"],
"V":["10001","10001","10001","01010","01010","00100","00100"],
"W":["10001","10001","10101","10101","10101","11011","10001"],
"X":["10001","01010","00100","00100","00100","01010","10001"],
"Y":["10001","01010","00100","00100","00100","00100","00100"],
"Z":["11111","00001","00010","00100","01000","10000","11111"],
"-":["00000","00000","00000","11111","00000","00000","00000"],
"!":["00100","00100","00100","00100","00100","00000","00100"],
"0":["01110","10001","10011","10101","11001","10001","01110"],
"1":["00100","01100","00100","00100","00100","00100","01110"],
"2":["01110","10001","00001","00110","01000","10000","11111"],
"3":["11110","00001","01110","00001","00001","00001","11110"],
"4":["00010","00110","01010","10010","11111","00010","00010"],
"5":["11111","10000","11110","00001","00001","10001","01110"],
"6":["01110","10000","11110","10001","10001","10001","01110"],
"7":["11111","00001","00010","00100","01000","01000","01000"],
"8":["01110","10001","01110","10001","10001","10001","01110"],
"9":["01110","10001","10001","01111","00001","00001","01110"],
".":["00000","00000","00000","00000","00000","00000","00100"]
};

// ---------- STATE ----------
let editMode = "text";
let isPlaying = false;
let playTimer = null;
let flashTimer = null;
let currentSceneIndex = 0;
let active = { r: 0, c: 0 };

function blankChars(){
    return Array.from({length: ROWS}, () => Array(COLS).fill(" "));
}
function blankSolid(){
    return Array.from({length: ROWS}, () => Array(COLS).fill(false));
}
function makeScene(){
    return {
        chars: blankChars(),
        solid: blankSolid(),
        flash: false,
        duration: 1000
    };
}
let scenes = [makeScene()];

// ---------- DOM ----------
const canvas = document.getElementById("ledBoard");
const ctx = canvas.getContext("2d", { alpha: false });

const sceneStatus = document.getElementById("sceneStatus");
const sceneDetails = document.getElementById("sceneDetails");
const durationInput = document.getElementById("durationInput");
const loopCheckbox = document.getElementById("loopCheckbox");
const flashBtn = document.getElementById("flashBtn");
const textModeBtn = document.getElementById("textModeBtn");
const solidModeBtn = document.getElementById("solidModeBtn");

// ---------- CANVAS ----------
function setupCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(BOARD_W * dpr);
    canvas.height = Math.round(BOARD_H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const shellWidth = document.querySelector(".board-shell").clientWidth - 20;
    const cssWidth = Math.min(shellWidth, BOARD_W);
    canvas.style.width = cssWidth + "px";
    canvas.style.height = (BOARD_H * cssWidth / BOARD_W) + "px";
    drawCurrentScene(true, true);
}

// ---------- HELPERS ----------
function currentScene() {
    return scenes[currentSceneIndex];
}
function cloneScene(scene) {
    return {
        chars: scene.chars.map(row => [...row]),
        solid: scene.solid.map(row => [...row]),
        flash: scene.flash,
        duration: scene.duration
    };
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ---------- DRAW ----------
function drawDot(x, y, on) {
    ctx.beginPath();
    ctx.arc(x + DOT_SIZE / 2, y + DOT_SIZE / 2, DOT_SIZE / 2, 0, Math.PI * 2);
    ctx.fillStyle = on ? LED_ON : LED_OFF;
    ctx.fill();
}

function drawTile(x, y, ch, solid, visible=true) {
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(x, y, TW, TH);

    ctx.strokeStyle = GAP_LINE;
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, TW, TH);

    const p = FONT[ch] || FONT[" "];
    const sx = x + TILE_PAD;
    const sy = y + TILE_PAD;

    for (let gy = 0; gy < DOT_H; gy++) {
        for (let gx = 0; gx < DOT_W; gx++) {
            let on = false;
            if (visible) {
                on = solid ? true : (p[gy][gx] === "1");
            }
            drawDot(sx + gx * (DOT_SIZE + DOT_GAP), sy + gy * (DOT_SIZE + DOT_GAP), on);
        }
    }
}

function drawScene(scene, showActive=true, visible=true) {
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, BOARD_W, BOARD_H);

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const x = OUTER_PAD + c * (TW + TILE_GAP);
            const y = OUTER_PAD + r * (TH + TILE_GAP);

            drawTile(x, y, scene.chars[r][c], scene.solid[r][c], visible);

            if (showActive && !isPlaying && active.r === r && active.c === c) {
                ctx.lineWidth = 2;
                ctx.strokeStyle = ACTIVE_COLOR;
                ctx.strokeRect(x - 1, y - 1, TW + 2, TH + 2);
            }
        }
    }
}

function drawCurrentScene(showActive=true, visible=true) {
    drawScene(currentScene(), showActive, visible);
}

// ---------- UI ----------
function refreshUi() {
    const s = currentScene();
    durationInput.value = s.duration;
    flashBtn.textContent = "Flash This Scene: " + (s.flash ? "On" : "Off");
    sceneStatus.textContent = "Scene " + (currentSceneIndex + 1) + " of " + scenes.length;
    sceneDetails.textContent =
        "Mode: " + (editMode === "text" ? "Text Edit" : "Solid Tile Select") +
        " | Flash: " + (s.flash ? "On" : "Off") +
        " | Duration: " + s.duration + " ms";

    textModeBtn.classList.toggle("active-btn", editMode === "text");
    solidModeBtn.classList.toggle("active-btn", editMode === "solid");

    drawCurrentScene(true, true);
}

// ---------- INPUT ----------
const hiddenInput = document.createElement("input");
hiddenInput.type = "text";
hiddenInput.autocapitalize = "characters";
hiddenInput.autocomplete = "off";
hiddenInput.spellcheck = false;
hiddenInput.style.position = "fixed";
hiddenInput.style.opacity = "0";
hiddenInput.style.pointerEvents = "none";
hiddenInput.style.bottom = "0";
hiddenInput.style.left = "0";
hiddenInput.style.width = "1px";
hiddenInput.style.height = "1px";
document.body.appendChild(hiddenInput);

function focusInput() {
    hiddenInput.focus();
}

function setTileFromPointer(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = BOARD_W / rect.width;
    const scaleY = BOARD_H / rect.height;
    const mx = (clientX - rect.left) * scaleX;
    const my = (clientY - rect.top) * scaleY;

    const x = mx - OUTER_PAD;
    const y = my - OUTER_PAD;

    const col = Math.floor(x / (TW + TILE_GAP));
    const row = Math.floor(y / (TH + TILE_GAP));

    if (row >= 0 && row < ROWS && col >= 0 && col < COLS) {
        active = { r: row, c: col };

        if (editMode === "solid") {
            const s = currentScene();
            s.solid[row][col] = !s.solid[row][col];
            if (s.solid[row][col]) {
                s.chars[row][col] = " ";
            }
        }

        refreshUi();
        focusInput();
    }
}

canvas.addEventListener("click", (e) => {
    setTileFromPointer(e.clientX, e.clientY);
});

canvas.addEventListener("touchstart", (e) => {
    const t = e.touches[0];
    if (t) setTileFromPointer(t.clientX, t.clientY);
}, { passive: true });

// ---------- NAV ----------
function advance() {
    active.c += 1;
    if (active.c >= COLS) {
        active.c = 0;
        active.r = Math.min(active.r + 1, ROWS - 1);
    }
    refreshUi();
}
function moveLeft() {
    if (active.c > 0) {
        active.c -= 1;
    } else if (active.r > 0) {
        active.r -= 1;
        active.c = COLS - 1;
    }
    refreshUi();
}
function moveRight() {
    if (active.c < COLS - 1) {
        active.c += 1;
    } else if (active.r < ROWS - 1) {
        active.r += 1;
        active.c = 0;
    }
    refreshUi();
}
function nextLine() {
    active.c = 0;
    active.r = Math.min(active.r + 1, ROWS - 1);
    refreshUi();
}

// ---------- EDIT ----------
function insertChar(ch) {
    const s = currentScene();
    s.solid[active.r][active.c] = false;
    if (FONT[ch]) {
        s.chars[active.r][active.c] = ch;
        advance();
    }
}
function backspace() {
    const s = currentScene();

    if (s.chars[active.r][active.c] !== " " || s.solid[active.r][active.c]) {
        s.chars[active.r][active.c] = " ";
        s.solid[active.r][active.c] = false;
    } else if (active.c > 0 || active.r > 0) {
        if (active.c > 0) {
            active.c -= 1;
        } else {
            active.r -= 1;
            active.c = COLS - 1;
        }
        s.chars[active.r][active.c] = " ";
        s.solid[active.r][active.c] = false;
    }

    refreshUi();
}

// ---------- KEYBOARD ----------
document.addEventListener("keydown", (e) => {
    if (isPlaying) return;

    if (e.key === "Backspace") {
        e.preventDefault();
        backspace();
        return;
    }

    if (e.key === "Enter") {
        e.preventDefault();
        nextLine();
        return;
    }

    if (e.key === "ArrowLeft") {
        e.preventDefault();
        moveLeft();
        return;
    }

    if (e.key === "ArrowRight") {
        e.preventDefault();
        moveRight();
        return;
    }

    if (e.key === " ") {
        e.preventDefault();
        advance();
        return;
    }

    if (editMode !== "text") return;

    if (e.key.length === 1) {
        let ch = e.key.toUpperCase();
        if (FONT[ch]) {
            e.preventDefault();
            insertChar(ch);
        }
    }
});

// ---------- MOBILE PAD ----------
document.querySelectorAll(".mobile-pad button").forEach((btn) => {
    btn.addEventListener("click", () => {
        if (isPlaying) return;
        const key = btn.getAttribute("data-key");
        focusInput();

        if (key === "←") return moveLeft();
        if (key === "→") return moveRight();
        if (key === "↵") return nextLine();
        if (key === "⌫") return backspace();
        if (key === "SPACE") return advance();
    });
});

// ---------- SCENES ----------
document.getElementById("prevSceneBtn").addEventListener("click", () => {
    if (currentSceneIndex > 0) {
        currentSceneIndex -= 1;
        refreshUi();
        focusInput();
    }
});

document.getElementById("nextSceneBtn").addEventListener("click", () => {
    if (currentSceneIndex < scenes.length - 1) {
        currentSceneIndex += 1;
        refreshUi();
        focusInput();
    }
});

document.getElementById("addScenesBtn").addEventListener("click", () => {
    const val = prompt("How many new scenes do you want to add?", "1");
    if (val === null) return;
    const count = parseInt(val, 10);
    if (!Number.isFinite(count) || count < 1) return;

    for (let i = 0; i < count; i++) {
        scenes.push(makeScene());
    }
    currentSceneIndex = scenes.length - count;
    refreshUi();
});

document.getElementById("duplicateSceneBtn").addEventListener("click", () => {
    scenes.splice(currentSceneIndex + 1, 0, cloneScene(currentScene()));
    currentSceneIndex += 1;
    refreshUi();
});

document.getElementById("deleteSceneBtn").addEventListener("click", () => {
    if (scenes.length === 1) {
        scenes[0] = makeScene();
        currentSceneIndex = 0;
    } else {
        scenes.splice(currentSceneIndex, 1);
        currentSceneIndex = Math.max(0, Math.min(currentSceneIndex, scenes.length - 1));
    }
    refreshUi();
});

document.getElementById("clearSceneBtn").addEventListener("click", () => {
    scenes[currentSceneIndex] = makeScene();
    active = { r: 0, c: 0 };
    refreshUi();
    focusInput();
});

// ---------- MODES ----------
document.getElementById("textModeBtn").addEventListener("click", () => {
    editMode = "text";
    refreshUi();
    focusInput();
});

document.getElementById("solidModeBtn").addEventListener("click", () => {
    editMode = "solid";
    refreshUi();
    focusInput();
});

flashBtn.addEventListener("click", () => {
    currentScene().flash = !currentScene().flash;
    refreshUi();
});

durationInput.addEventListener("change", () => {
    let v = parseInt(durationInput.value, 10);
    if (!Number.isFinite(v) || v < 200) v = 200;
    currentScene().duration = v;
    refreshUi();
});

// ---------- DOWNLOAD PNG ----------
document.getElementById("downloadPngBtn").addEventListener("click", () => {
    drawCurrentScene(false, true);
    const link = document.createElement("a");
    link.download = "led-board-scene-" + (currentSceneIndex + 1) + ".png";
    link.href = canvas.toDataURL("image/png");
    link.click();
    refreshUi();
});

// ---------- PLAYBACK ----------
function stopPlayback() {
    isPlaying = false;
    if (playTimer) {
        clearTimeout(playTimer);
        playTimer = null;
    }
    if (flashTimer) {
        clearInterval(flashTimer);
        flashTimer = null;
    }
    refreshUi();
}

function playSceneAt(index) {
    if (!isPlaying) return;

    currentSceneIndex = index;
    const s = currentScene();
    let flashVisible = true;

    if (flashTimer) clearInterval(flashTimer);
    flashTimer = null;

    drawScene(s, false, true);
    refreshUi();

    if (s.flash) {
        flashTimer = setInterval(() => {
            if (!isPlaying) return;
            flashVisible = !flashVisible;
            drawScene(s, false, flashVisible);
        }, 300);
    } else {
        drawScene(s, false, true);
    }

    playTimer = setTimeout(() => {
        if (!isPlaying) return;

        let nextIndex = index + 1;
        if (nextIndex >= scenes.length) {
            if (loopCheckbox.checked) {
                nextIndex = 0;
            } else {
                stopPlayback();
                return;
            }
        }
        playSceneAt(nextIndex);
    }, s.duration);
}

document.getElementById("playBtn").addEventListener("click", () => {
    if (isPlaying) return;
    isPlaying = true;
    playSceneAt(currentSceneIndex);
});

document.getElementById("stopBtn").addEventListener("click", () => {
    stopPlayback();
});

// ---------- VIDEO EXPORT ----------
async function recordScenesToWebm() {
    if (isPlaying) stopPlayback();

    const fps = 15;
    const stream = canvas.captureStream(fps);
    const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });
    const chunks = [];

    recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
            chunks.push(e.data);
        }
    };

    const done = new Promise((resolve) => {
        recorder.onstop = () => {
            const blob = new Blob(chunks, { type: "video/webm" });
            resolve(blob);
        };
    });

    recorder.start();

    const flashIntervalMs = 300;

    for (let i = 0; i < scenes.length; i++) {
        const s = scenes[i];
        currentSceneIndex = i;
        refreshUi();

        if (s.flash) {
            const cycles = Math.max(1, Math.floor(s.duration / flashIntervalMs));
            let visible = true;

            for (let j = 0; j < cycles; j++) {
                drawScene(s, false, visible);
                await sleep(flashIntervalMs);
                visible = !visible;
            }

            const remaining = s.duration - (cycles * flashIntervalMs);
            if (remaining > 0) {
                drawScene(s, false, visible);
                await sleep(remaining);
            }
        } else {
            drawScene(s, false, true);
            await sleep(s.duration);
        }
    }

    recorder.stop();
    const blob = await done;

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "led-board-scenes.webm";
    link.click();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
    refreshUi();
}

document.getElementById("downloadVideoBtn").addEventListener("click", async () => {
    await recordScenesToWebm();
});

// ---------- INIT ----------
window.addEventListener("resize", setupCanvas);
setupCanvas();
refreshUi();
focusInput();
</script>
</body>
</html>
"""

components.html(html_code, height=760, scrolling=False)
st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:2px; color:#aaa;'>Created by NN.</div>", unsafe_allow_html=True)
```
