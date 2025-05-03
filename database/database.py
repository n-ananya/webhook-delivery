from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base




try:

    # Database URL: Replace with your MySQL credentials
    DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/webhook"

    # Create an SQLAlchemy engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Create a sessionmaker object to interact with the database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a base class for declarative models
    Base = declarative_base()


except Exception as e:
    raise e