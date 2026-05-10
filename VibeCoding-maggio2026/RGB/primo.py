import time
import board
import analogio
import neopixel

# ingresso analogico: potenziometro
pot = analogio.AnalogIn(board.IO2)

# strip di LED WS2812
NUM_LED = 8
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, pixel_order=neopixel.RGB, auto_write=True)
pixels.brightness = 0.5

while True:
    # valore del potenziometro
    # in teoria 0 - 65536, in pratica 0, 64000
    valore = pot.value

    # convertiamo il valore in numero di LED accesi (0 - 8)
    
    # alcuni sistemi utili allo scopo
    
    #proporzione
    #led_accesi = valore * num_led // 64000  
    
    # scaling (ma se cambia il numero di led, non va bene)
    #led_accesi = valore // 8000            
    
    # normalizzazione rispetto al numero di led
    #led_accesi = valore // (64000/num_led)
    
    # proporzione ma con scaling del valore
    led_accesi = (valore // 1000) * NUM_LED // 64
   
    print( led_accesi)
    
    # ok, ci siamo...
    # prima spegniamo tutti i LED
    pixels.fill((0, 0, 0))

    # poi accendiamo i LED uno alla volta
    for i in range(led_accesi):
        pixels[i] = (0, 50, 0)   # verde
    
    pixels.show()
    time.sleep(0.5)
