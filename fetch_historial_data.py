import logging
import os
from datetime import datetime

from constants.stocks_symbols import stocks_list
from loggers import logger
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel


# --- Loading .env files ---
load_dotenv()


# ---- Class Fyers ----
class fyersHistorial:

    # ----      ----
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")

        # --- Reading Access Token ---
        with open(r"F:\fyers_prices\access_token.txt", mode="r") as f:
            self.access_token = f.read().strip()


    # ---- Fetch Historical Data Func ----
    def fetch_historical_feed(self, symbol: str, resolution: str, date_format: str, range_from: str, range_to: str):
        """Fetches Historial Feeds"""

        try:
            fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=self.access_token, log_path="")
            response = fyers.history(data={
                "symbol": symbol, "resolution": resolution,
                "date_format": "1",
                "range_from": range_from,
                "range_to": range_to,
                "cont_flag": "1" })

            print(response)

        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fyers_obj = fyersHistorial()
    for sym in stocks_list:
        fyers_obj.fetch_historical_feed(symbol=sym, resolution="D", date_format="0",
                                    range_from="2026-04-21", range_to="2026-04-22")