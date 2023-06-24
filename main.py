from termcolor import colored
from datetime import datetime
from modules.weather import get_weather_data, fmt_cli_resp
import sys


def start_program(city):
    """Start the CLI program."""
    print(
        colored(
            "WindCatcher V1.0 By @AmarnathCJD #FastestCoderFirst #GithubCopilot",
            "red",
            attrs=["bold"],
        )
    )
    print(colored("-" * 35, "magenta", attrs=["bold"]))
    if city is None:
        city = input(colored("Enter City Name: ", "yellow", attrs=["bold"]))
    else:
        print(colored(f"City Name: {city}", "yellow", attrs=["bold"]))
    start_time = datetime.now()
    weather_data, city, country_code = get_weather_data(city)
    if "error" in weather_data:
        print(colored(f"Error: {weather_data['error']}", "red"))
    else:
        fmt_cli_resp(weather_data, city, country_code, start_time)


if __name__ == "__main__":
    # Check if user has entered city name as a flag
    flags = ["-c", "--city"]
    if len(sys.argv) > 1:
        if sys.argv[1] in flags:
            city = sys.argv[2]
        else:
            print(colored("Warning: Invalid Flag!!", "yellow"))
            city = None
    else:
        city = None

    # If city is None, then ask user to enter city name
    start_program(city)

# Project: WindCatcher
# Author: github.com/AmarnathCJD
# Date: 2023-06-24

# Note: AccuWeather Website is used to get the weather data.
# modules used: requests, bs4, termcolor
