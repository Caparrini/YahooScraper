import csv
import logging
import os
import time

import requests
from bs4 import BeautifulSoup
import src.auxiliar


class BaseScraper:
    def __init__(self):
        self.url = ""

    def download(self, url, user_agent="wswp", num_retries=2):
        logging.info("Downloading: {}".format(url))
        headers = {'User-agent': user_agent}
        try:
            res = requests.get(url, headers)
        except requests.exceptions.RequestException as e:
            logging.error("Download error: {}".format(e))
            res = None
        return res


class YahooScraper(BaseScraper):
    def __init__(self):
        self.url_ticker = "https://finance.yahoo.com/quote/{}?p={}"
        self.base_url = "https://finance.yahoo.com"

    def __scrap_statistics(self, soup):
        tds = soup.find_all("td")
        keys = []
        values = []
        for i in range(len(tds)):
            if i % 2 == 0:
                keys.append(tds[i].find("span").text)
            else:
                values.append(tds[i].text)
        if len(keys) != len(values):
            logging.error("No se pueden generar estadisticas, distinto numero de key y values.")
            estadisticas = None
        else:
            estadisticas = dict(zip(keys, values))

        return estadisticas

    def __find_news_urls(self, soup):
        full_div_a = soup.find_all("a")
        news_urls = [n["href"] for n in full_div_a if n.find("u") is not None]
        return news_urls

    def __scrap_new(self, soup):
        logging.info("Scrap de una noticia...")
        my_new = {"date": soup.find("time").text}
        paragraph = True
        p_labeled = soup.find_all("p")
        i = 0
        new_text = []
        while paragraph and i < len(p_labeled):
            try:
                new_text.append(src.auxiliar.preprocess_text(p_labeled[i]["content"].replace(";", ",")))
            except:
                paragraph = False
            i += 1
        #my_new["text"] = unicodedata.normalize("NFKD", BeautifulSoup(" ".join(new_text), "html.parser").get_text())
        my_new["text"] = " ".join(new_text)
        return my_new

    def __scrap_news(self, soup):
        new_urls = self.__find_news_urls(soup)
        news = []
        for u in new_urls:
            full_url = self.base_url + u
            res_new = self.download(full_url)
            soup_new = BeautifulSoup(res_new.content, "html.parser")
            my_new = self.__scrap_new(soup_new)
            my_new["url"] = full_url
            news.append(my_new)
            time.sleep(4)
        return news

    def results2csv(self, scrap_result):
        tickers = scrap_result.keys()
        header_news = ["ticker", "date", "url", "content"]
        header_stats = ["ticker"]
        header_summary = ["ticker"]
        with open(os.path.join("..", "csv", "yahoo_news.csv"), 'w', newline='') as news_csv, \
                open(os.path.join("..", "csv", "yahoo_summaries.csv"), 'w', newline='') as summaries_csv, \
                open(os.path.join("..", "csv", "yahoo_statistics.csv"), 'w', newline='') as stats_csv:
            news_writer = csv.writer(news_csv, delimiter=";")
            news_writer.writerow(header_news)
            summaries_writer = csv.writer(summaries_csv, delimiter=";")
            stats_writer = csv.writer(stats_csv, delimiter=";")
            stats_keys = []
            summaries_keys = []
            i = 0
            for ticker in tickers:
                # News
                news = scrap_result[ticker]["news"]
                for n in news:
                    date = n["date"]
                    url = n["url"]
                    content = n["text"]
                    try:
                        news_writer.writerow([ticker, date, url, content])
                    except:
                        logging.info("Error escribiendo linea de noticias")
                # Stats
                # En la primera pasada crear la cabecera
                if i == 0:
                    my_summaries = scrap_result[ticker]["summary"]
                    summaries_keys = [k for k in my_summaries.keys()]
                    header_summary.extend(summaries_keys)
                    summaries_writer.writerow(header_summary)
                try:
                    my_summaries = scrap_result[ticker]["summary"]
                    summaries_writer.writerow([ticker] + [my_summaries[key] for key in summaries_keys])
                except:
                    logging.error("Error escribiendo linea de sumarios")
                # Summary
                # En la primera pasada crear la cabecera
                if i == 0:
                    my_stats = scrap_result[ticker]["stats"]
                    stats_keys = [k for k in my_stats.keys()]
                    header_stats.extend(stats_keys)
                    stats_writer.writerow(header_stats)
                try:
                    my_stats = scrap_result[ticker]["stats"]
                    stats_writer.writerow([ticker] + [my_stats[key] for key in stats_keys])
                except:
                    logging.error("Error escribiendo linea de estadisticas")
                i += 1
        logging.info("Escritura de csvs terminada")

    def scrape_tickers(self, tickers):
        logging.info("Se va a extraer información de los siguientes tickers: {}".format(tickers))
        scrap_results = {}
        for t in tickers:
            self.url = self.url_ticker.format(t, t)
            res = self.download(self.url)
            soup = BeautifulSoup(res.content, "html.parser")
            logging.info("Extraemos los datos de Summary")
            summary_scraped = self.__scrap_statistics(soup)
            logging.info("Extraemos los datos de noticias")
            news_scraped = self.__scrap_news(soup)
            logging.info("Extraemos las estadisticas")
            url_stats = self.url_ticker.format(t + "/key-statistics", t)
            res_stats = self.download(url_stats)
            soup_stats = BeautifulSoup(res_stats.content, "html.parser")
            stats_scraped = self.__scrap_statistics(soup_stats)
            scrap_results[t] = {"summary": summary_scraped, "stats": stats_scraped, "news": news_scraped}
            time.sleep(4)
        return scrap_results

    def scrape(self, tickers):
        logging.info("Inicio de scrap")
        scrap_result = self.scrape_tickers(tickers)
        logging.info("Scrap terminado, escribiendo ficheros")
        self.results2csv(scrap_result)
        logging.info("Ficheros terminados")