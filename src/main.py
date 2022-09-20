import json
import machine
import network
import rp2
import secrets
import time
import urequests


wlan = network.WLAN(network.STA_IF)
rtc = machine.RTC()
led = machine.Pin("LED", machine.Pin.OUT)
HOUR = 60 * 60


def get_offset() -> int:
    """
        Gets the timezone offset for currently hardcoded timezone.
        This should handle daylight savings fluxes
    """
    print("Attempting to get current time offset")
    try:
        response = urequests.get(
            "http://worldtimeapi.org/api/timezone/Australia/Sydney").json()

        print(f"API response was: {json.dumps(response)}")

        return int(response['raw_offset'])
    except OSError as e:
        print(json.dumps(e))
        time.sleep(10)
        main()


def check_daytime() -> void:
    """
        Compares local time to the currently advertised
        sunrise and set times for geographic Sydney.

        Considers it to be post sunrise the minute of sunrise and
        sunset the minute of sunset.

        The below is horrendous code. Maybe I should have just looked harder for an API that returns true/false for daytime queries?
    """
    offset = get_offset()
    print("Attempting to check sunrise status")
    try:
        response = urequests.get(
            "https://api.sunrise-sunset.org/json?lat=-33.868820&lng=151.209290").json()

        print(f"API response was: {json.dumps(response)}")

        raw_utc_sunrise = response['results']['sunrise']
        raw_utc_sunset = response['results']['sunset']
        sunrise_hour = abs(((12 if "PM" in raw_utc_sunrise else 0) + int(raw_utc_sunrise.split(":")[0])) +
                           int(offset / HOUR)) % 24

        sunset_hour = abs(((12 if "PM" in raw_utc_sunset else 0) + int(raw_utc_sunrise.split(":")[0])) +
                          int(offset / HOUR)) % 24
        sunrise_minute = int(raw_utc_sunrise.split(":")[1])
        sunset_minute = int(raw_utc_sunset.split(":")[1])

        current_time = rtc.datetime()
        hour = current_time[4]
        minute = current_time[5]

        post_sunrise = ((hour > sunrise_hour) or (
            hour == sunrise_hour and minute > sunrise_minute))

        pre_sunset = ((hour < sunset_hour) or (
            hour == sunset_hour and minute < sunset_minute))

        return post_sunrise and pre_sunset

    except OSError as e:
        print(json.dumps(e))
        time.sleep(10)
        main()


def setup() -> void:
    print("Attempting to setup RPi Pico")
    rp2.country('AU')

    wlan.active(True)

    wlan.connect(secrets.SSID, secrets.PSK)

    while not wlan.isconnected() and wlan.status() >= 0:
        time.sleep(1)


def main() -> void:
    led.on()
    setup()

    while True:
        is_daytime = check_daytime()
        print(f"Is daytime: {is_daytime}")
        print("Sleeping for 5 minutes")
        time.sleep(600)


if __name__ == "__main__":
    main()
