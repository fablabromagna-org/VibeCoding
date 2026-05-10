import time
import board

# Usiamo gli ingressi e le uscite digitali
from digitalio import DigitalInOut, Direction, Pull

# LED
led = DigitalInOut(board.GP19)
led.direction = Direction.OUTPUT

# Buzzer
import pwmio
buzzer = pwmio.PWMOut(board.GP18, frequency=800, duty_cycle=0)

# Switch
switch = DigitalInOut(board.GP17)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# Usiamo gli ingressi analogici
from analogio import AnalogIn

# Potenziometro
posizione = AnalogIn(board.A0)

# Luce
luxmetro = AnalogIn(board.A1)

# Rumore
fonometro = AnalogIn(board.A2)

# Sensori DHT11 e DHT22 per temp e umidità
import adafruit_dht
dht = adafruit_dht.DHT11(board.GP16)

# Display
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
displayio.release_displays()

# I2C Bus
import busio
i2c = busio.I2C( scl=board.GP7, sda=board.GP6 )
display_bus = displayio.I2CDisplay( i2c, device_address=0x3C )
display = adafruit_displayio_ssd1306.SSD1306( display_bus, width=128, height=64 )

# Display 7 segmenti
import TM1637
sevenSeg_CLK = board.GP20
sevenSeg_DIO = board.GP21
sevenSeg = TM1637.TM1637(sevenSeg_CLK, sevenSeg_DIO)
sevenSeg.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
time.sleep(2)

def get_voltage(pin):
    return (pin.value * 30) / 65536

def Stampa( p, l, s, t, h ):
    # Make the display context
    #text_group = displayio.Group(max_size=10)
    text_group = displayio.Group()

    altezza_riga = 11
    posizione_y = 3

    # Draw a label
    text = "Environment sensor"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    text = "Pos:  {:.2f}".format( p )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    text = "Lux:  {:.2f}".format( l )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    text = "Snd:  {:.2f}".format( s )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    text = "Temp: {:.2f}".format( t )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    text = "Humi: {:.2f}".format( h )
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=posizione_y)
    text_group.append(text_area)
    posizione_y = posizione_y + altezza_riga

    display.show(text_group)


velocitaLettura = 0
velocitaVisualizza = 0

t = 0
h = 0
p = 0
l = 0
s = 0

while True:

    if switch.value:
        led.value = True
        buzzer.duty_cycle = 65535 // 2  # On 50%
    else:
        led.value = False
        buzzer.duty_cycle = 0

    time.sleep(0.01)  # debounce delay

    velocitaLettura = velocitaLettura + 1
    if velocitaLettura > 100:
        velocitaLettura = 0
        # legge temperatura e umidità ogni secondo
        t = dht.temperature
        h = dht.humidity

    p = get_voltage( posizione )
    l = get_voltage( luxmetro )
    s = get_voltage( fonometro )

    velocitaVisualizza = velocitaVisualizza + 1
    if velocitaVisualizza > 1:
        velocitaVisualizza = 0
        print(
            #"Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format( temperature_f, temperature_c, humidity )
            "({:.3f}, {:.3f}, {:.3f}, {:.1f}, {})".format( p, l, s , t, h )
        )
        Stampa( p, l, s, t, h )
        
        # Indagare su come faccia a sapere l'ora!!! :-()
        tempo = time.localtime()
        sevenSeg.numbers(tempo.tm_hour, tempo.tm_min)
        #time.sleep(60-(t.tm_sec%60))


