"""
Stock Price Pipeline Entry Point.

Workflow:
- Initiate ETL pipeline.
"""

import asyncio
from src.pipeline.etl_pipeline import StockETLPipeline
from src.utils.config import STOCK_SYMBOLS

async def main():
    tasks = []
    for symbol in STOCK_SYMBOLS:    
        pipeline = StockETLPipeline(symbol)
        tasks.append(pipeline.run())
    await asyncio.gather(*tasks)
   
if __name__ == '__main__':
    asyncio.run(main())