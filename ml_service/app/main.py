from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import time
import json
import logging
import os
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_client import CONTENT_TYPE_LATEST
from app.database import SessionLocal, PredictionLog


# Настройка JSON-логирования
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_record)


# Настраиваем логгер
logger = logging.getLogger("ml_service")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Метрики Prometheus
PREDICT_COUNT = Counter('predictions_total', 'Total number of predictions')
PREDICT_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency in seconds')
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

# Создаем FastAPI приложение
app = FastAPI(title="Simple ML Service", version="1.0.0")


# Модель для запроса
class PredictRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float


# Модель для ответа
class PredictResponse(BaseModel):
    prediction: float
    model_version: str
    processing_time_ms: float


# модель
def dummy_model(feature1, feature2, feature3):
    return 0.5 * feature1 + 0.3 * feature2 + 0.2 * feature3


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "ML Service is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Эндпоинт для метрик Prometheus
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    start_time = time.time()
    PREDICT_COUNT.inc()  # увеличиваем счетчик

    try:
        # Логируем входной запрос
        logger.info(f"Prediction request: {request.dict()}")

        # Получаем предсказание от модели
        prediction = dummy_model(
            request.feature1,
            request.feature2,
            request.feature3
        )

        # Вычисляем время обработки
        processing_time = (time.time() - start_time) * 1000  # в миллисекундах

        # Записываем latency в гистограмму (в секундах)
        PREDICT_LATENCY.observe(time.time() - start_time)

        # Логируем результат
        logger.info(f"Prediction result: {prediction}, time: {processing_time:.2f}ms")

        # Сохраняем в базу данных
        try:
            db = SessionLocal()
            db_log = PredictionLog(
                input_data=json.dumps(request.dict()),
                prediction=prediction,
                model_version=MODEL_VERSION,
                processing_time_ms=processing_time
            )
            db.add(db_log)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Database logging failed: {e}")

        return PredictResponse(
            prediction=prediction,
            model_version=MODEL_VERSION,
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))