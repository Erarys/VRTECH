from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from dotenv import load_dotenv
load_dotenv()


DATABASE_URL  = "postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{NAME}".format(
    HOST=os.getenv("DB_HOST"),
    PORT=os.getenv("DB_PORT"),
    USER=os.getenv("DB_USER"),
    PASS=os.getenv("DB_PASS"),
    NAME=os.getenv("DB_NAME")
)


engine = create_engine(DATABASE_URL)

factory_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()