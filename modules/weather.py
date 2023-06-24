from requests import get, Timeout as ReqOut
from .decoder import ACCU_API_KEY, fetch_full_weather_data
from .errors import Timeout, InvalidCityError, APIError
from termcolor import colored
from datetime import datetime


def get_weather_data(city: str) -> dict:
    """Get weather data from API."""
    try:
        city, timetaken = get_city_name(city)
        fmt_cli_resp(fetch_full_weather_data(city.get("Key", "")), city.get(
            "LocalizedName", ""), city.get("Country", {}).get("LocalizedName", ""), datetime.now() - timetaken)
        return {}
    except Exception as e:
        return {"error": str(e)}


def get_city_name(city: str) -> str:
    """Get matching city name from API."""

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    params = {"q": city, "language": "en-us",
              "apikey": ACCU_API_KEY, "details": True}

    """Do get request to API and return response."""
    req_time = datetime.now()
    try:
        req = get(
            "https://api.accuweather.com/locations/v1/cities/autocomplete",
            params=params,
            headers=headers,
            timeout=10,
        )
    except ReqOut:
        raise Timeout("Timeout (10s)") from None
    
    req_end_time = datetime.now()

    if req.status_code == 200:
        if len(req.json()) == 0:
            raise InvalidCityError(
                "Invalid city name, try re-checking the spelling.")
        if len(req.json()) == 1:
            return req.json()[0], req_end_time - req_time
        print(colored("Multiple cities found, please select one.", "yellow"))
        num_index = 0
        for city in req.json():
            num_index += 1
            print(
                colored(
                    "[{}] {} ({}, {})".format(
                        num_index,
                        city.get("LocalizedName", ""),
                        city.get("AdministrativeArea", {}).get(
                            "LocalizedName", ""),
                        city.get("Country", {}).get("LocalizedName", ""),
                    ),
                    "cyan",
                )
            )
        while True:
            try:
                index = int(input(colored("Select City: ", "yellow")))
                if index < 1 or index > num_index:
                    raise ValueError
                return req.json()[index - 1], req_end_time - req_time
            except ValueError:
                print(colored("Invalid index, try again.", "red"))

    else:
        raise APIError("APIError (status code: {})".format(req.status_code))


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
            f" - Temp: {data.get('current', {}).get('Temp', 'N/A')} | Fahrenheit: {int(float(data.get('current', {}).get('Temp', '0°C').split('°')[0]))*9/5+32}°F | Kelvin: {int(float(data.get('current', {}).get('Temp', '0°C').split('°')[0]))+273.15}K",
            "magenta",
        )
    )
    print(
        colored(
            f" - {data.get('current', {}).get('Time', 'N/A')} | Raining: {data.get('current', {}).get('raining', 'False')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
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

    print(colored("\n[*] Temperature Variations", "red", attrs=["bold"]))
    print(
        colored(
            f" - Past 24 Hours: {data.get('current', {}).get('24hV', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Past 12 Hours: {data.get('current', {}).get('12hV', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Past 06 Hours: {data.get('current', {}).get('6hV', 'N/A')}",
            "green",
        )
    )

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    i = -2
    for v in range(5):
        i += 1
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
                + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | AIQ: {forecast[i+1].get('AIQ', 'N/A')}",
                "yellow",
            )
        )
        print(
            colored(
                " " * 3
                + f"- UV Index: {forecast[i+1].get('Max UV Index', 'N/A')} | Snow: {forecast[i+1].get('Snow', 'N/A')} | Ice: {forecast[i+1].get('Ice', 'N/A')}",
                "blue",
            )
        )
        print(
            colored(
                " " * 3
                + f"- SunRise: {forecast[i+1].get('SunRise', 'N/A')} | SunSet: {forecast[i+1].get('SunSet', 'N/A')}",
                "cyan",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Moon: {forecast[i+1].get('Moon', '')} | Rise: {forecast[i+1].get('Moon rise', 'N/A')} | Set: {forecast[i+1].get('Moon set', 'N/A')}",
                "light_red",
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
