import csv
import logging
import os
from src.auxiliar import preprocess_text
from src.scrapers import YahooScraper
import pandas as pd


def init_logging():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    init_logging()
    df = pd.read_csv(os.path.join("..", "csv", "ibex35.csv"), delimiter=";", header=None)
    ibex35 = list(df[0])
    yahoo_scraper = YahooScraper()
    yahoo_scraper.scrape(ibex35 )



