import logging
import os
import argparse
from src.scrapers import YahooScraper
import pandas as pd


def init_logging():
    logging.basicConfig(level=logging.DEBUG)

def parse_arguments():
    parser = argparse.ArgumentParser(description='YahooScraper')
    parser.add_argument('input_tickers', type=str, nargs='?',
                        help='Archivo con los tickers a scrapear', default=os.path.join("..", "csv", "ibex35.csv"))
    return parser.parse_args()


if __name__ == "__main__":
    init_logging()
    args = parse_arguments()
    df = pd.read_csv(os.path.join("..", "csv", args.input_tickers), delimiter=";", header=None)
    tickers = list(df[0])
    yahoo_scraper = YahooScraper()
    yahoo_scraper.scrape(tickers)



