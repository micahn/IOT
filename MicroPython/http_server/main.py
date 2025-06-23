import network
import machine
import time
import server
from credstore import SSID, Password

led = machine.Pin('LED', machine.Pin.OUT)

def connect_wifi(timeout: int = 20, max_retries: int = 3) -> bool:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    retries = 0
    while retries < max_retries:
        print(f"Attempting to connect to Wi-Fi (Attempt {retries + 1}/{max_retries})")
        
        c = 0
        wlan.connect(SSID, Password)
        while not wlan.isconnected() and wlan.status() >= 0 and c < timeout:
            led.toggle()
            time.sleep(1)
            c += 1
        if wlan.isconnected():
            led.on()
            timer = machine.Timer(-1)
            timer.init(period=10000, mode=machine.Timer.ONE_SHOT, callback=lambda t: led.off())
            print(f"Connected to Wi-Fi: {wlan.ifconfig()}")
            return True
        print(f"Connection failed, status: {wlan.status()}")
        for _ in range(20):
            led.toggle()
            time.sleep(0.25)
        led.off()
        retries += 1
        time.sleep(2 ** retries)
    print("Max retries exceeded, could not connect")
    return False,

def run():
    print("Starting main.py...")
    while True:
        try:
            if connect_wifi():
                print("Starting server...")
                server.run()
            else:
                print("Wi-Fi connection failed, retrying in 5 seconds...")
                time.sleep(5)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Run loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    run()
