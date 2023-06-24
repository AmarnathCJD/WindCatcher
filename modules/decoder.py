from termcolor import colored as cl

from requests import get
import time

ACCU_API_KEY = "41b7800bfcb9447daa29f7aa40f2d1ec"

def fetch_full_weather_data(location: str) -> dict:
    _curr = get("https://api.accuweather.com/currentconditions/v1/{}".format(location), params={
        "apikey": ACCU_API_KEY,
        "details": True,
        "language": "en-us",
    },
        headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    },
        timeout=60)

    output = ""
    if _curr.status_code != 200:
        output += cl("Error: ", "red") + \
            "Invalid city name, try re-checking the spelling."
        return {"error": output}
    _curr = _curr.json()[0]

    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    weather["current"]["Time"] = time.strftime("%I:%M %p", time.strptime(
        _curr.get("LocalObservationDateTime", ""), "%Y-%m-%dT%H:%M:%S%z"))
    weather["current"]["raining"] = _curr.get("HasPrecipitation", False)
    weather["current"]["Temp"] = str(
        _curr.get("Temperature", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["Phrase"] = _curr.get("WeatherText", "")
    weather["current"]["Realfeel sun"] = str(
        _curr.get("RealFeelTemperature", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["Realfeel shade"] = str(_curr.get(
        "RealFeelTemperatureShade", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["Max uv index"] = str(
        _curr.get("UVIndex", "")) + " (" + _curr.get("UVIndexText", "") + ")"
    weather["current"]["Wind"] = str(_curr.get("Wind", {}).get("Speed", {}).get("Metric", {}).get(
        "Value", "")) + " km/h" + " " + _curr.get("Wind", {}).get("Direction", {}).get("Localized", "")
    weather["current"]["Wind gusts"] = str(_curr.get("WindGust", {}).get(
        "Speed", {}).get("Metric", {}).get("Value", "")) + " km/h"
    weather["current"]["Cloud cover"] = str(_curr.get("CloudCover", "")) + "%"
    weather["current"]["Dew point"] = str(
        _curr.get("DewPoint", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["Humidity"] = str(
        _curr.get("RelativeHumidity", "")) + "%"
    weather["current"]["Indoor humidity"] = str(
        _curr.get("IndoorRelativeHumidity", "")) + "%"
    weather["current"]["Visibility"] = str(
        _curr.get("Visibility", {}).get("Metric", {}).get("Value", "")) + " km"
    weather["current"]["Pressure"] = str(
        _curr.get("Pressure", {}).get("Metric", {}).get("Value", "")) + " mb"
    weather["current"]["Cloud ceiling"] = str(
        _curr.get("Ceiling", {}).get("Metric", {}).get("Value", "")) + " m"
    weather["current"]["24hV"] = str(_curr.get("TemperatureSummary", {}).get("Past24HourRange", {}).get("Maximum", {}).get("Metric", {}).get(
        "Value", "")) + "°C <---> " + str(_curr.get("TemperatureSummary", {}).get("Past24HourRange", {}).get("Minimum", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["12hV"] = str(_curr.get("TemperatureSummary", {}).get("Past12HourRange", {}).get("Maximum", {}).get("Metric", {}).get(
        "Value", "")) + "°C <---> " + str(_curr.get("TemperatureSummary", {}).get("Past12HourRange", {}).get("Minimum", {}).get("Metric", {}).get("Value", "")) + "°C"
    weather["current"]["6hV"] = str(_curr.get("TemperatureSummary", {}).get("Past6HourRange", {}).get("Maximum", {}).get("Metric", {}).get(
        "Value", "")) + "°C <---> " + str(_curr.get("TemperatureSummary", {}).get("Past6HourRange", {}).get("Minimum", {}).get("Metric", {}).get("Value", "")) + "°C"

    _fcast = get("https://api.accuweather.com/forecasts/v1/daily/5day/{}".format(location), params={
        "apikey": ACCU_API_KEY,
        "details": True,
        "metric": True,
        "language": "en-us",
    },
        headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    },
        timeout=60)

    if _fcast.status_code != 200:
        output += cl("Error: ", "red") + \
            "Invalid city name, try re-checking the spelling."
        return {"error": output}

    _fcast = _fcast.json()
    for day in _fcast["DailyForecasts"]:
        weather["forecast"].append({
            "Date": time.strftime("%d/%m/%Y", time.strptime(day.get("Date", ""), "%Y-%m-%dT%H:%M:%S%z")),
            "Temp": {
                "max": str(day.get("Temperature", {}).get("Maximum", {}).get("Value", "")) + "°C",
                "min": str(day.get("Temperature", {}).get("Minimum", {}).get("Value", "")) + "°C",
            },
            "Rain": str(day.get("Day", {}).get("RainProbability", "")) + "%",
            "Hours of Precipitation": str(day.get("Day", {}).get("HoursOfRain", "")),
            "Cloud Cover": str(day.get("Day", {}).get("CloudCover", "")) + "%",
            "Wind": str(day.get("Day", {}).get("Wind", {}).get("Speed", {}).get("Value", "")) + " km/h" + " " + day.get("Day", {}).get("Wind", {}).get("Direction", {}).get("Localized", ""),
            "Wind Gusts": str(day.get("Day", {}).get("WindGust", {}).get("Speed", {}).get("Value", "")) + " km/h",
            "Max UV Index": str(day.get("AirAndPollen", {})[-1].get("Value", "")) + " (" + day.get("AirAndPollen", {})[-1].get("Category", "") + ")",
            "Hours of Sun": str(day.get("Day", {}).get("HoursOfSun", "")),
            "Moon": day.get("Moon", {}).get("Phase", ""),
            "Moon rise": time.strftime("%I:%M %p", time.strptime(day.get("Moon", {}).get("Rise", ""), "%Y-%m-%dT%H:%M:%S%z")),
            "Moon set": time.strftime("%I:%M %p", time.strptime(day.get("Moon", {}).get("Set", ""), "%Y-%m-%dT%H:%M:%S%z")),
            "SunRise": time.strftime("%I:%M %p", time.strptime(day.get("Sun", {}).get("Rise", ""), "%Y-%m-%dT%H:%M:%S%z")),
            "SunSet": time.strftime("%I:%M %p", time.strptime(day.get("Sun", {}).get("Set", ""), "%Y-%m-%dT%H:%M:%S%z")),
            "AIQ": str(day.get("AirAndPollen", {})[0].get("Value", "")) + " (" + day.get("AirAndPollen", {})[0].get("Category", "") + ")",
            "Snow": str(day.get("Day", {}).get("Snow", {}).get("Value", "")) + " cm",
            "Ice": str(day.get("Day", {}).get("Ice", {}).get("Value", "")) + " mm",
        })

    return weather


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()

# @AmarnathCJD
