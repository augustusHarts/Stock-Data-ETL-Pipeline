"""
Stock Price Ingestion Logic.

Responsibilities:
- Fetch stock price data (JSON) from external sources.
- Saving data in raw (JSON) and structured (CSV) format.
"""

import requests
import json
from datetime import datetime
import time
from src.utils.config import RAW_DATA_DIR, API_TIMEOUT, YAHOO_RANGE, YAHOO_INTERVAL 
from src.utils.logger import get_logger

class StockFetcher:
    """
    Handles Ingestion raw equity price data from APIs.
    """

    BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart'

    def __init__(self, symbol:str):
        self.symbol = symbol
        self.logger = get_logger(self.__class__.__name__)

    def fetch_data(self) -> dict:
        """
        Fetch raw stock price data from external APIs.

        Returns:
        --------
        dict
            Raw API response in JSON format.
        """

        url = f'{self.BASE_URL}/{self.symbol}'
        params = {
            'range': YAHOO_RANGE,
            'interval': YAHOO_INTERVAL
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        retries = 3
        base_backoff = 2

        self.logger.info(f'Calling Yahoo Finance API for {self.symbol}')
        
        for attempt in range(1, retries+1):
            try:
                response = requests.get(
                    url, 
                    params=params, 
                    timeout=API_TIMEOUT,
                    headers=headers
                )

                if response.status_code == 429:
                    raise requests.RequestException('Rate limit exceeded (429)')
                
                response.raise_for_status()
                data = response.json()

                if 'chart' not in data or data['chart'].get('error') is not None:
                    raise ValueError('Invalid response from Yahoo Finance')
                
                self.logger.info(f'Successfully fetched data for {self.symbol}')
                return data
            
            except requests.exceptions.RequestException as e:
                self.logger.exception(f'API request failed')
                
                if attempt < retries:
                    sleep_time = base_backoff ** attempt
                    self.logger.info(f'Retrying in {sleep_time} seconds...')
                    time.sleep(sleep_time)
                else:
                    self.logger.error(('Max reties exceeded'))
                    raise

            except ValueError as e:
                self.logger.error(f'Data Validation failed: {e}')
                raise
        
    def save_raw_data(self,data):
        """
        Persist raw stock price data in JSON format.

        Parameters:
        -----------
        data: dict
            Raw API response containing stock price data.
        """

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = RAW_DATA_DIR / f'{self.symbol}_{timestamp}.json'

        self.logger.info(f'Saving raw data to {file_path}')
        
        with open(file_path,'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_csv(self, df):
        """
        Persist structured stock price data in CSV format.

        Parameters:
        -----------
        df: pd.DataFrame
            OHLCV stock price data to be saved. 
        """

        file_path = RAW_DATA_DIR / f'{self.symbol}.csv'
        self.logger.info(f'Saving parsed csv to {file_path}')

        df.to_csv(file_path, index=False)

