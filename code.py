import board
import time
import wifi
import ssl
import adafruit_requests
import socketpool
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

status_red = (255, 0, 0, 0.5)
status_green = (0, 255, 0, 0.5)
status_yellow = (255, 255, 0, 0.5)
status_magenta = (128, 0, 255, 0.5)
status_off = (0, 0, 0, 0)
aio_connected = False

if board.board_id == 'unexpectedmaker_feathers2':
    import adafruit_dotstar
    addr_led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)
    addr_led[0] = status_magenta
    from analogio import AnalogIn
    light_sensor = AnalogIn(board.AMB)
elif board.board_id == 'adafruit_feather_esp32s2':
    import neopixel
    addr_led = neopixel.NeoPixel(board.NEOPIXEL, 100)
    addr_led[0] = status_magenta

# Sensor initialization
import adafruit_tmp117
i2c = board.I2C()  # uses board.SCL and board.SDA
tmp117 = adafruit_tmp117.TMP117(i2c)

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

while True:
    while not wifi.radio.ap_info:
        print("Connecting to Wi-Fi")
        for network in network_keys:
            try:
                print("Trying:", network, end=': ')
                wifi.radio.connect(network, network_keys[network])
                addr_led[0] = status_yellow
                print("Connected!")
                break
            except:
                print("Unable to connect.")
        time.sleep(5)

    # import ipaddress
    # wifi.radio.ping(ipaddress.ip_address("8.8.8.8"))

    if not aio_connected:
        # Initialize an Adafruit IO HTTP API object
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        io = IO_HTTP(secrets["aio_username"], secrets["aio_key"], requests)
        print("Connecting to Adafruit IO", end='...')
        try:
            temperature_feed = io.get_feed(secrets["aio_feed"])
            aio_connected = True
            addr_led[0] = status_green
            print("Connected!")
            # break
        except:
            aio_connected = False
            print("Failed! Waiting...")
            # raise
            time.sleep(10)
    if aio_connected:
        temperature = tmp117.temperature
        print("T:", temperature, end=' ... ')
        try:
            addr_led[0] = status_off
            io.send_data(temperature_feed["key"], temperature)
            addr_led[0] = status_green
            print("Sent!")
        except:
            addr_led[0] = status_yellow
            print("Failed! Waiting...")
            time.sleep(20)
        time.sleep(10)
