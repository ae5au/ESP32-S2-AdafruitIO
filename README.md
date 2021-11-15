# FeatherS2-AdafruitIO
FeatherS2 posting to Adafruit IO via ESP32-S2 internal Wi-Fi.

The example is using a TMP117 temperature sensor connected to the Unexpected Maker [FeatherS2](https://feathers2.io/).  Should be trivial to port to any board using the ESP32-S2 such as the [Adafruit ESP32-S2 Feather](https://www.adafruit.com/product/5000) or to other sensors based on sample code and libraries for the specific sensor.

Allows for multiple Wi-Fi networks and will reconnect if Wi-Fi connection is lost. Note that it will connect in the order that the networks are placed in secrets.py and will only change to another network if the current connection fails.

Requires the following libraries from the [Bundle for CircuitPython 7.x](https://circuitpython.org/libraries):
- adafruit_bus_device
- adafruit_io
- adafruit_register
- adafruit_requests
- adafruit_tmp117

Usage:
1. Copy the necessary libraries to the 'lib' folder on CircuitPython board.
2. Create secrets.py file with your network and Adafruit IO credentials. Use secrets-example.py as a template. Place it on your CircuitPython board.
3. Add new feed on your Adafruit IO account and update secrets.py with key in "aio_feed".
4. Copy code.py to CircuitPython board.

Suggestions for improvement are appreciated!
