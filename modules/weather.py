from requests import get, Timeout as ReqOut
from .decoder import get_soup, parse_weather_to_json
from .errors import Timeout, InvalidCityError, APIError
from termcolor import colored
from datetime import datetime


def get_weather_data(city: str) -> dict:
    """Get weather data from API."""
    try:
        city = get_city_name(city)
        weather_link, city, country_code = format_weather_link(city)
        _currw = get_soup(weather_link)
        _castw = get_soup(
            weather_link.replace("current-weather", "daily-weather-forecast")
        )
        return parse_weather_to_json(_currw, _castw), city, country_code
    except Exception as e:
        return {"error": str(e)}, "", ""


def get_city_name(city: str) -> str:
    """Get matching city name from API."""

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    params = {"query": city, "language": "en-us"}

    """Do get request to API and return response."""
    try:
        req = get(
            "https://www.accuweather.com/web-api/autocomplete",
            params=params,
            headers=headers,
            timeout=60,
        )
    except ReqOut:
        raise Timeout

    if req.status_code == 200:
        if len(req.json()) == 0:
            raise InvalidCityError("Invalid city name, try re-checking the spelling.")
        if len(req.json()) == 1:
            return req.json()[0]
        print(colored("Multiple cities found, please select one.", "yellow"))
        num_index = 0
        for city in req.json():
            num_index += 1
            print(
                colored(
                    "[{}] {} ({}, {})".format(
                        num_index,
                        city.get("localizedName", ""),
                        city.get("administrativeArea", {}).get("localizedName", ""),
                        city.get("country", {}).get("localizedName", ""),
                    ),
                    "cyan",
                )
            )
        while True:
            try:
                index = int(input(colored("Select City: ", "yellow")))
                if index < 1 or index > num_index:
                    raise ValueError
                return req.json()[index - 1]
            except ValueError:
                print(colored("Invalid index, try again.", "red"))

    else:
        raise APIError("APIError (status code: {})".format(req.status_code))


def format_weather_link(data) -> str:
    """Format weather link from The JSONData."""
    try:
        country_code = data.get("country", {}).get("id", "").lower()
        city_name = data.get("localizedName", "").lower().replace(" ", "-")
        city_key = data.get("key", "")
    except AttributeError:
        return (
            "Failed to get city data, Make sure you have entered the correct city name."
        )

    return (
        "https://www.accuweather.com/{}/{}/{}/{}/current-weather/{}".format(
            "en",
            country_code,
            city_name,
            city_key,
            city_key,
        ),
        city_name,
        country_code,
    )


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(
        colored(
            f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    print(
        colored(
            f" - RealFeel Sun: {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f" - Wind: {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Dew Point: {data.get('current', {}).get('Dew point', 'N/A')} | Humidity: {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f" - Visibility: {data.get('current', {}).get('Visibility', 'N/A')} | Pressure: {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling: {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f" - Temp: {data.get('day', {}).get('Temp', 'N/A')} | Feels: {data.get('day', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    print(
        colored(
            f" - UV Index: {data.get('day', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('day', {}).get('Wind', 'N/A')} | Gusts: {data.get('day', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {data.get('day', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('day', {}).get('Rain', 'N/A')} | Thunder: {data.get('day', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f" - Temp: {data.get('night', {}).get('Temp', 'N/A')} | Feels: {data.get('night', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    print(
        colored(
            f" - UV Index: {data.get('night', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('night', {}).get('Wind', 'N/A')} | Gusts: {data.get('night', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {data.get('night', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('night', {}).get('Rain', 'N/A')} | Thunder: {data.get('night', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
        )
    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )


# @AmarnathCJD
