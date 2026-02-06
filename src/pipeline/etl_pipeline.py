"""
ETL Pipeline Logic.

Responsibilities:
- Fetch raw data from External APIs
- Parse OHLCV stock prices from raw JSON format
- Apply transformation and features to structures data
- Load the clean and featured data to PostgreSQL
"""

from src.utils.config import DATABASE_URL
from src.utils.logger import get_logger
from src.db.db_loader import PostgresLoader
from src.ingestion.stock_fetcher import StockFetcher
from src.ingestion.stock_parser import StockDataParser
from src.transformation.stock_transformer import StockTransformer
from sqlalchemy.exc import IntegrityError, OperationalError

class StockETLPipeline:
    """
    Docstring for StockETLPipeline
    """

    def __init__(self, symbol:str):
        """
        Init function to initialise all objects.

        Parameters:
        -----------
        symbol: str
            Stock Ticker Symbol.
        """
        
        self.symbol = symbol
        self.logger = get_logger(self.__class__.__name__)
        self.fetcher = StockFetcher(symbol)
        self.parser = StockDataParser(symbol)
        self.transformer = StockTransformer()
        self.loader = PostgresLoader(DATABASE_URL)

    def run(self) -> None:
        """
        Exceute the ETL pipeline from begining.
        """
        
        self.logger.info(f'Starting ETL pipeline for {self.symbol}')

        # Extract
        raw_data = self.fetcher.fetch_data()
        self.fetcher.save_raw_data(raw_data)

        # Parse
        df_raw = self.parser.parse(raw_data)
        self.fetcher.save_csv(df_raw)

        # Transform   
        df_clean = self.transformer.clean_data(df_raw)
        df_features = self.transformer.add_features(df_clean)
        
            
        # Load
        try:
            stock_id  = self.loader.upsert_stock(self.symbol)
            self.loader.load_daily_prices(df_features, stock_id)

        except OperationalError as e:
            self.logger.error(f'Database Connection Error: {e}')
            raise 
        
        except IntegrityError as e:
            self.logger.error(f'No Data Found: {e}')
            raise
        
        except Exception as err:
            self.logger.error(f'Unexpected Python Error: {err}', exc_info=True)
            raise

        # finally:
        #     if self.loader.

        self.logger.info(f'ETL pipeline completed for {self.symbol}')