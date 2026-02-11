import time
import board
import analogio

adc = analogio.AnalogIn(board.A1)

RAW_ZERO = 500
RAW_MAX  = 23500  # taratura iniziale, la puoi alzare se satura

# smoothing (0..1) più alto = più reattivo, più basso = più stabile
ALPHA = 0.15

filt = 0.0

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

print("Anemometro analogico A1 - 0 sotto RAW_ZERO")
print("RAW_ZERO:", RAW_ZERO, "RAW_MAX:", RAW_MAX)

while True:
    raw = adc.value

    if raw < RAW_ZERO:
        speed_pct = 0.0
    else:
        x = (raw - RAW_ZERO) / (RAW_MAX - RAW_ZERO)  # 0..1
        x = clamp(x, 0.0, 1.0)
        speed_pct = x * 100.0

    # filtro IIR per stabilizzare
    filt = (1 - ALPHA) * filt + ALPHA * speed_pct

    print(f"raw={raw:5d}  speed={speed_pct:6.1f}%  filt={filt:6.1f}%")
    time.sleep(0.1)
z