from bs4 import BeautifulSoup
from requests import get, Timeout
import time


def get_soup(url: str) -> BeautifulSoup:
    """Get soup from url."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    """Do get request to API and return response."""
    try:
        req = get(url, headers=headers, timeout=60)
    except Timeout:
        raise Exception("Timeout exceeded while getting soup.")

    if req.status_code == 200:
        return BeautifulSoup(req.text, "html.parser")
    else:
        raise Exception("APIError (status code: {})".format(req.status_code))


def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    # Get current weather data
    current = soup.find("div", {"class": "current-weather-card"})
    weather["current"]["Time"] = current.find("p", class_="sub").text
    weather["current"]["Temp"] = remove_special_chars(
        current.find("div", {"class": "display-temp"}).text
    )
    weather["current"]["Phrase"] = remove_special_chars(
        current.find("div", {"class": "phrase"}).text
    )
    for item in current.find("div", {"class": "current-weather-details"}).find_all(
        "div", class_="detail-item"
    ):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather["current"][
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)

    # Get day and night weather data
    for card in soup.find_all("div", {"class": "half-day-card"}):
        if "day" in card.find("h2").text.lower():
            weather_ = weather["day"]
        else:
            weather_ = weather["night"]

        weather_["Date"] = card.find("span", class_="short-date").text.strip()
        weather_["Temp"] = remove_special_chars(
            card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°"
        )
        weather_["Phrase"] = remove_special_chars(
            card.find("div", {"class": "phrase"}).text.strip()
        )

        for item in card.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            weather_[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)

    # get forecast data
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = {}

        date = wr.find("h2", {"class": "date"})
        forecast["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div", {"class": "temp"})
        forecast["Temp"] = {
            "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
        }
        forecast["Precipitation"] = remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        )
        for item in card.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            forecast[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
        weather["forecast"].append(forecast)

    return weather


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()

# @AmarnathCJD
