import os.path
from io import StringIO

import requests
import pandas as pd
from loggers import logger



# ---- Class Daily Reports ----
class DailyReportsService:

    # ---- Class Variables ----
    symbol_list = []
    host = "https://nsearchives.nseindia.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0: Win64; x64',
        'referer': 'https://nsearchives.nseindia.com/'
    }

    # ---- Default Constructor ----
    def __init__(self, timeout: int=6):
        self.response = requests.head(url=self.host, headers=self.headers)
        self.cookies = self.response.cookies
        self.timeout = timeout
        self.filename = "ind_nifty500list.csv"
        self.url = {
            'Nse_50_stocks': '{host}content/indices/'
        }


    # ---- Fetch Nifty 50 Stock CSV Func ----
    def fetch_nifty_50_stocks_list(self, store_file: bool=True) -> pd.DataFrame | None:
        """Fetch NIFTY 50 Stocks List"""

        # https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv
        try:

            final_url = f"{self.url.get('Nse_50_stocks').format(host=self.host)}{self.filename}"
            logger.info(f"URL: {final_url}")
            response = requests.get(url=final_url, headers=self.headers, cookies=self.cookies, timeout=self.timeout)
            if response.status_code == 200:
                if store_file:
                    df = pd.read_csv(StringIO(response.text))
                    full_path = os.path.join('nse_dataset', self.filename)
                    df.to_csv(full_path)
                    logger.info(f"Csv stored @ {full_path} !")
                else:
                    return pd.read_csv(StringIO(response.text))
            else:
                return None

        except requests.exceptions.HTTPError as h:
            logger.info(f"exception occurred http error: {h}")
            return None

        except requests.exceptions.Timeout as t:
            logger.indo(f"exception occurred request timeout: {t}")
            return None

        except requests.exceptions.RequestException as e:
            logger.info(f"exception occurred while downloading nifty 50 stocks: {e}")
            return None

    # ----- Fetch Nifty 50 Stock Symbol Func -----
    def fetch_stocks_symbols(self) -> list | None:
        """Fetch Stock Symbols"""

        try:
            file_path = os.path.join('nse_dataset', self.filename)

            # ----- File Check -----
            if not os.path.exists(file_path):
                logger.warning(f"{self.filename} is not present at: {file_path} !")
                return None

            df = pd.read_csv(file_path, skiprows=[1])
            for index, row in df.iterrows():
                self.symbol_list.append(f"NSE:{row['Symbol']}-EQ")

            return self.symbol_list
        except Exception as e:
            logger.info(f"exception occurred while fetching stocks symbols from csv: {e} !")
            return None




if __name__ == '__main__':
    dr = DailyReportsService()
    # dr.fetch_nifty_50_stocks_list()
    stocks_list = dr.fetch_stocks_symbols()
    print(stocks_list)