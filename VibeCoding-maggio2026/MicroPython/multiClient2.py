import sys
from micropython import const
import asyncio
import aioble
import bluetooth
import random
import struct

# UUID per il servizio e la caratteristica di temperatura
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# Intervallo di pubblicità (ms)
_ADV_INTERVAL_MS = 250_000

# Lista per gestire più connessioni attive
active_connections = []

# Registro del servizio GATT
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True)
aioble.register_services(temp_service)

# Helper per codificare la temperatura (sint16, centesimi di grado)
def _encode_temperature(temp_deg_c):
    return struct.pack("<h", int(temp_deg_c))

# Simula la lettura di un sensore di temperatura
async def sensor_task(connection):
    t = 10
    delta = 1
    while True:
        # Scrivi la temperatura e invia un aggiornamento al dispositivo connesso
        temp_characteristic.write(_encode_temperature(t), send_update=True)
        t += random.uniform(0, delta)
        
        if t > 35:
            delta = -1
        if t < 20:
            delta = 1
        
        print(f"Temperature sent to {connection.device}: {t}°C")
        await asyncio.sleep_ms(1000)

# Gestisci la connessione di un dispositivo
async def handle_connection(connection):
    print(f"Connected to {connection.device}")
    active_connections.append(connection)
    
    # Avvia il task per inviare letture di temperatura
    asyncio.create_task(sensor_task(connection))
    
    try:
        # Mantieni la connessione attiva
        await connection.disconnected(timeout_ms=None)
    except asyncio.TimeoutError:
        print(f"Connection with {connection.device} timed out.")
    finally:
        active_connections.remove(connection)
        print(f"Disconnected from {connection.device}")

# Pubblica continuamente e gestisci le connessioni in arrivo
async def peripheral_task():
    while True:
        # Inizia la pubblicità BLE per i dispositivi in cerca di connessione
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="RP2035 BLE FLRTemp",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            # Quando un dispositivo si connette, gestisci la connessione
            await handle_connection(connection)

# Funzione principale che esegue le due attività in parallelo
async def main():
    # Avvia le attività asincrone
    t1 = asyncio.create_task(peripheral_task())  # Task per la pubblicità BLE e gestione delle connessioni
    await t1

# Avvia la funzione principale
asyncio.run(main())
