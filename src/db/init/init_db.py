from src.db.engine import engine
from sqlalchemy import text
from src.utils.logger import get_logger
from src.utils.config import BASE_DIR

def init_db():
    """
    Initialize database tables.
    """
    logger = get_logger('init_db')

    with open('src/db/init/create_table.sql') as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))

    logger.info('Tables created in Database successfully.')

if __name__ == '__main__':
    init_db()