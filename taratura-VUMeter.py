import time
import math
import board
import analogio

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

adc = analogio.AnalogIn( SENSOR_PIN )

# ---- Parametri di misura ----
DC_TAU = 1.0        # media lenta per stimare il bias
PRINT_EVERY = 0.5   # secondi
SAMPLE_SLEEP = 0.002  # ~500 Hz

def alpha(dt, tau):
    return 1.0 - math.exp(-dt / tau) if tau > 0 else 1.0

# Stato
dc = adc.value
last_t = time.monotonic()

# Statistiche finestra
t0 = time.monotonic()
count = 0
amp_sum = 0.0
amp_sum2 = 0.0
amp_max = 0.0

# Per una stima robusta del "picco tipico"
# (salviamo solo 64 massimi locali della finestra)
peaks = []

print("TARATURA MICROFONO (ampiezza = |raw - dc|)")
print("Fase A: SILENZIO 10s -> annota amp_max e amp_rms")
print("Fase B: FORTE (batti mani/voce) 10s -> annota amp_max e amp_p95\n")

while True:
    now = time.monotonic()
    dt = now - last_t
    last_t = now

    raw = adc.value

    # Bias (DC) stimato lentamente
    a_dc = alpha(dt, DC_TAU)
    dc = dc + a_dc * (raw - dc)

    # Ampiezza istantanea
    amp = abs(raw - dc)

    # Accumula statistiche
    count += 1
    amp_sum += amp
    amp_sum2 += amp * amp
    if amp > amp_max:
        amp_max = amp

    # Campiona alcuni "peaks" (massimi locali semplici)
    # (usiamo una decimazione: 1 peak ogni ~20 campioni)
    if count % 20 == 0:
        peaks.append(amp)
        if len(peaks) > 64:
            peaks.pop(0)

    # Stampa ogni PRINT_EVERY
    if (now - t0) >= PRINT_EVERY:
        amp_mean = amp_sum / count
        amp_rms = math.sqrt(amp_sum2 / count)

        # stima "p95" sui peak campionati (approssimata ma utile)
        p95 = 0.0
        if peaks:
            s = sorted(peaks)
            idx = int(0.95 * (len(s) - 1))
            p95 = s[idx]

        print(
            "amp_mean={:7.1f}  amp_rms={:7.1f}  amp_p95~={:7.1f}  amp_max={:7.1f}".format(
                amp_mean, amp_rms, p95, amp_max
            )
        )

        # reset finestra
        t0 = now
        count = 0
        amp_sum = 0.0
        amp_sum2 = 0.0
        amp_max = 0.0
        peaks.clear()

    time.sleep(SAMPLE_SLEEP)
