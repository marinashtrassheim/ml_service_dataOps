from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from sqlalchemy_utils import database_exists, create_database

# Подключение к БД
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ml_user:ml_pass@postgres:5432/ml_db")

# Создаем базу данных, если её нет
if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    print(f"Database created: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель для логирования предсказаний
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    input_data = Column(String)
    prediction = Column(Float)
    model_version = Column(String, default="v1.0.0")
    processing_time_ms = Column(Float)


# Создаем таблицы
Base.metadata.create_all(bind=engine)
print("Tables created successfully")