# scegliCPU.py
import board

BOARD_ID = getattr(board, "board_id", "unknown")

# Mappa board_id -> (LED_PIN_NAME, SENSOR_PIN_NAME)
PINMAP = {
    # ESP32
    "seeed_xiao_esp32c6": ("D9",  "D2"),
    "makergo_esp32c3_supermini": ("IO6", "IO2"),

    # RP2040 / RP2350 (famiglia Pico)
    "raspberry_pi_pico":   ("GP16", "GP26_A0"),
    "raspberry_pi_pico_w": ("GP16", "GP26_A0"),
    "raspberry_pi_pico2_w":("GP16", "GP26_A0"),
}

if BOARD_ID not in PINMAP:
    raise RuntimeError("Board non supportata: " + BOARD_ID)

_led_name, _sensor_name = PINMAP[BOARD_ID]

LED_PIN = getattr(board, _led_name)
SENSOR_PIN = getattr(board, _sensor_name)

CPU_NAME = BOARD_ID  # per debug/log

def debug_print():
    print("BOARD_ID:", BOARD_ID)
    print("LED_PIN:", _led_name)
    print("SENSOR_PIN:", _sensor_name)
