"""
Stock Price Pipeline Entry Point.

Workflow:
- Initiate ETL pipeline.
"""

from src.pipeline.etl_pipeline import StockETLPipeline
from src.utils.config import STOCK_SYMBOLS

def main():
    for symbol in STOCK_SYMBOLS:
        try:
            pipeline = StockETLPipeline(symbol)
            pipeline.run()
        except Exception as e:
            raise
   
if __name__ == '__main__':
    main()  