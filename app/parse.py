import csv

import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass, fields, astuple

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


QUOTE_FIELDS = [field.name for field in fields(Quote)]


def parse_single_quote(quote_soup: BeautifulSoup) -> Quote:
    return Quote(
        text=quote_soup.select_one(".text").text,
        author=quote_soup.select_one(".author").text,
        tags=quote_soup.select(".keywords")[0]["content"].split(",")
    )


def get_home_quotes() -> [Quote]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    quotes = soup.select(".quote")

    return [parse_single_quote(quote_soup) for quote_soup in quotes]


def main(output_csv_path: str) -> None:
    quotes = get_home_quotes()
    with open(output_csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(QUOTE_FIELDS)
        writer.writerows([astuple(quote) for quote in quotes])


if __name__ == "__main__":
    main("quotes.csv")
