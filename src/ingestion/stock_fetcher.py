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
import asyncio
import aiohttp
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

    async def fetch_data(self,session) -> dict:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110'
        }
        retries = 3
        base_backoff = 2

        self.logger.info(f'Calling Yahoo Finance API for {self.symbol}')
        
        for attempt in range(1, retries+1):
            try:
                async with session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=API_TIMEOUT
                ) as response:

                    if response.status == 429:
                        raise Exception('Rate limit exceeded (429)')
                
                    response.raise_for_status()
                    data = await response.json()

                    if 'chart' not in data or data['chart'].get('error') is not None:
                        raise ValueError('Invalid response from Yahoo Finance')
                
                    self.logger.info(f'Successfully fetched data for {self.symbol}')
                    return data
            
            except aiohttp.ClientError as e:
                self.logger.error(f'API request failed')
                
                if attempt < retries:
                    self.logger.info(f'Retrying in {base_backoff ** attempt} seconds...')
                    await asyncio.sleep(base_backoff ** attempt)
                else:
                    self.logger.error(('Max reties exceeded'))
                    raise

            except ValueError as e:
                self.logger.error(f'Data Validation failed: {e}')
                raise

        raise RuntimeError("Failed to fetch data after retries")

    async def fetch_data_async(self) -> dict:
        async with aiohttp.ClientSession() as session:
            return await self.fetch_data(session)

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

