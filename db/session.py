from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from core.settings import settings

DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'u_cup_2023',
    'port': 3306,
}

# mejorar esto !
database_url = f"mysql://{DATABASE['user']}@{DATABASE['host']}/{DATABASE['database']}"
engine = create_engine(database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
