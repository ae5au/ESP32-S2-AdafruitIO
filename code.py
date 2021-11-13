import board
import time
import adafruit_dotstar
import wifi
import ssl
import adafruit_requests
import socketpool
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
import adafruit_tmp117
from analogio import AnalogIn

i2c = board.I2C()  # uses board.SCL and board.SDA
tmp117 = adafruit_tmp117.TMP117(i2c)

status_red = (255, 0, 0, 0.5)
status_green = (0, 255, 0, 0.5)
status_yellow = (255, 255, 0, 0.5)
status_magenta = (128, 0, 255, 0.5)
status_off = (0, 0, 0, 0)
dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)
dotstar[0] = status_magenta

try:
    from secrets import secrets
except ImportError:
    print("Credentials are kept in secrets.py, please add them there!")
    raise

try:
    from secrets import network_keys
except ImportError:
    print("Wi-Fi network keys are kept in secrets.py, please add them there!")
    raise

print("Connecting to Wi-Fi")
for network in network_keys:
    try:
        print("Trying:", network, end=': ')
        wifi.radio.connect(network, network_keys[network])
        dotstar[0] = status_yellow
        print("Connected!")
        break
    except:
        print("Unable to connect.")

light_sensor = AnalogIn(board.AMB)

# import ipaddress
# wifi.radio.ping(ipaddress.ip_address("8.8.8.8"))

# Initialize an Adafruit IO HTTP API object
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
io = IO_HTTP(secrets["aio_username"], secrets["aio_key"], requests)
while True:
    print("Connecting to Adafruit IO", end='...')
    try:
        temperature_feed = io.get_feed(secrets["aio_feed"])
        dotstar[0] = status_green
        print("Connected!")
        break
    except:
        print("Failed! Waiting...")
        time.sleep(10)

while True:
    temperature = tmp117.temperature
    print("T:", temperature, "Light:", light_sensor.value, end=' ... ')
    try:
        dotstar[0] = status_off
        io.send_data(temperature_feed["key"], temperature)
        dotstar[0] = status_green
        print("Sent!")
    except:
        dotstar[0] = status_yellow
        print("Failed! Waiting...")
        time.sleep(20)
    time.sleep(10)
