# YahooScraper
## Español

Extrae las noticias, sumario y estadísticas que ofrece [Yahoo](https://finance.yahoo.com/) para una lista de tickers concretos de empresas.

Para ejecutar el script es necesario importar las siguientes librerías que aparecen en el fichero `requirements.txt`:
```
beautifulsoup4==4.8.1
builtwith==1.3.3
certifi==2019.9.11
chardet==3.0.4
future==0.18.2
idna==2.8
lxml==4.4.1
nltk==3.4.5
numpy==1.17.3
pandas==0.25.3
python-dateutil==2.8.1
python-whois==0.7.2
pytz==2019.3
requests==2.22.0
six==1.12.0
soupsieve==1.9.5
unicode==2.7
urllib3==1.25.6
wincertstore==0.2
```
Pueden instalarse fácilmente utilizando:
```shell script
pip install -r requirements.txt
```

El script se debe ejecutar de la siguiente manera:
```
python main.py
or
python main.py custom_tickers.csv
```

Donde **custom_tickers.csv** es un csv sin cabecera (con ";" como delimitador) donde la primera columna son los tickers 
que se desean scrapear. En el caso de ejecutarlo sin parámetros se descargará la información de las top 30 empresas del 
ibex35 (a día 3 de noviembre de 2019) utilizando el fichero `ibex35.csv` presente en este repositorio.

Se generaran tres ficheros csv en la carpeta `csv`. 
```
yahoo_news.csv
yahoo_statistics.csv
yahoo_summaries.csv
```
