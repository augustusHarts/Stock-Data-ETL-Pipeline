"""
Handles loading stock price data into a PostgreSQL database.

Responsibilities:
- Maintain database connection
- Upsert stock metadata
- Insert daily OHLCV and derived features
"""

from src.utils.logger import get_logger
import pandas as pd
from sqlalchemy import text
from src.db.engine import engine

class PostgresLoader:
    """
    Connect and stock price data into PostgreSQL database.
    """

    def __init__(self, db_url: str):
        """
        Initialize PostgreSQL connection.

        Parameters:
        -----------
        db_url: str
            SQLAlchemy-compatible PostgreSQL connection URL.
        """

        self.engine = engine
        self.logger = get_logger(self.__class__.__name__)


    def upsert_stock(self, symbol: str) -> int:
        """
        Insert stock symbol if it does not exists and return its stock_id.

        Parameters:
        -----------
        symbol: str
            Stock ticker symbol.

        Returns:
        --------
        int
            Primary key (stock_id) from stocks table.
        """

        query = """
        INSERT INTO stocks (symbol) 
        VALUES (:symbol) 
        ON CONFLICT (symbol) DO NOTHING;
        """

        select_query = """
        SELECT stock_id 
        FROM stocks 
        where symbol = :symbol;
        """

        with self.engine.begin() as conn:
            conn.execute(text(query), {'symbol':symbol})
            result = conn.execute(text(select_query), {'symbol':symbol}).fetchone()
        
        return result[0]

    def load_daily_prices(self, df: pd.DataFrame, stock_id: int):
        """
        Update SQL server with OHLCV and features for stock price data.
        Use PostgreSQL UPSERT to avoid duplication of data.

        Parameters:
        -----------
        df: pd.DataFrame
            Cleaned and feature-engineered stock price data.
        
        stock_id: int
            foreign key referencing the stocks table.
        """

        df = df.copy()
        df['stock_id'] = stock_id

        df = df[
            [
                "stock_id", 'date', 'open', 'high', 'low', 'close', 'volume', 
                'daily_return', 'log_return', 'volatility_20d', 'ma_20d', 'ma_50d' 
            ]
        ]

        df = df.drop_duplicates(subset=['stock_id','date'])
        records = df.to_dict(orient='records')

        upsert_query = text ("""
            INSERT INTO daily_prices (
                stock_id, date, open, high, low, close, volume,
                daily_return, log_return, volatility_20d, ma_20d, ma_50d
            )
            VALUES (
                :stock_id, :date, :open, :high, :low, :close, :volume,
                :daily_return, :log_return, :volatility_20d, :ma_20d, :ma_50d
            )
            ON CONFLICT (stock_id, date)
            DO UPDATE SET 
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume,
                daily_return = EXCLUDED.daily_return,
                log_return = EXCLUDED.log_return,
                volatility_20d = EXCLUDED.volatility_20d,
                ma_20d = EXCLUDED.ma_20d, 
                ma_50d = EXCLUDED.ma_50d;
        """)

        with self.engine.begin() as conn:
            conn.execute(upsert_query, records)

        self.logger.info(f'Loaded {len(df)} rows into daily_prices')

    def get_last_date(self, stock_id):
        query = text("""
            SELECT MAX(date) FROM daily_prices WHERE stock_id = :sid
        """)

        with self.engine.begin() as conn:
            result = conn.execute(query, {'sid': stock_id}).fetchone()
        return result[0]
        