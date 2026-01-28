# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import neopixel
import wifi
import socketpool

from secrets import secrets
from adafruit_httpserver import Server, Request, Response

# --- WS2812 ---
NUM_LEDS = 8
PIXEL_PIN = board.D6
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_LEDS, brightness=0.2, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

# --- Wi-Fi ---
wifi.radio.connect(secrets["ssid"], secrets["password"])
ip = str(wifi.radio.ipv4_address)
print("IP:", ip)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

HTML = """<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RGB</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .row { margin: 16px 0; }
    input[type=range] { width: 100%; }
    .v { font-variant-numeric: tabular-nums; }
    .swatch { width: 100%; height: 48px; border-radius: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h2>WS2812 RGB</h2>
  <div class="swatch" id="sw"></div>

  <div class="row">R: <span class="v" id="rv">0</span>
    <input id="r" type="range" min="0" max="255" value="0" />
  </div>
  <div class="row">G: <span class="v" id="gv">0</span>
    <input id="g" type="range" min="0" max="255" value="0" />
  </div>
  <div class="row">B: <span class="v" id="bv">0</span>
    <input id="b" type="range" min="0" max="255" value="0" />
  </div>

<script>
const r = document.getElementById('r');
const g = document.getElementById('g');
const b = document.getElementById('b');
const rv = document.getElementById('rv');
const gv = document.getElementById('gv');
const bv = document.getElementById('bv');
const sw = document.getElementById('sw');

let t = null;

function updateUI() {
  rv.textContent = r.value; gv.textContent = g.value; bv.textContent = b.value;
  sw.style.background = `rgb(${r.value},${g.value},${b.value})`;
}

async function send() {
  const url = `/set?r=${r.value}&g=${g.value}&b=${b.value}`;
  try { await fetch(url, { method: 'GET' }); } catch(e) {}
}

function onChange() {
  updateUI();
  if (t) clearTimeout(t);
  t = setTimeout(send, 80);
}

[r,g,b].forEach(el => el.addEventListener('input', onChange));
updateUI();
</script>
</body>
</html>
"""

@server.route("/")
def index(request: Request):
    return Response(request, HTML, content_type="text/html")

@server.route("/set")
def set_rgb(request: Request):
    try:
        r = int(request.query_params.get("r", "0"))
        g = int(request.query_params.get("g", "0"))
        b = int(request.query_params.get("b", "0"))
    except Exception:
        r, g, b = 0, 0, 0

    # clamp
    if r < 0: r = 0
    if r > 255: r = 255
    if g < 0: g = 0
    if g > 255: g = 255
    if b < 0: b = 0
    if b > 255: b = 255

    pixels.fill((r, g, b))
    pixels.show()
    return Response(request, "OK", content_type="text/plain")

# Bind robusto
server.start("0.0.0.0", port=80)
print("Apri dal telefono: http://%s/" % ip)

while True:
    try:
        server.poll()
    except Exception as e:
        print("poll error:", repr(e))
    time.sleep(0.01)
