from sqlalchemy import create_engine, text, inspect
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
print(f'DATABASE_URL: {db_url[:60]}...')

db_url_clean = db_url.split('?')[0].replace('postgresql://', 'postgresql+psycopg2://')
print(f'Clean URL: {db_url_clean[:60]}...')

try:
    engine = create_engine(db_url_clean, connect_args={'sslmode': 'require'})
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f'Tables: {tables}')
    
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS task CASCADE'))
        conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
        conn.commit()
        print('Tables dropped!')
        
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f'Tables after drop: {tables}')
except Exception as e:
    print(f'Error: {e}')
