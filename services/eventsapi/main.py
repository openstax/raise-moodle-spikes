from typing import Literal, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from kafka import KafkaProducer
import aioboto3
import uuid
import os


EVENTS_S3_BUCKET = os.getenv("EVENTS_S3_BUCKET")
EVENTS_S3_PREFIX = os.getenv("EVENTS_S3_PREFIX")
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")

KAFKA_SERVER = "kafka:29092"

app = FastAPI(
    title="RAISE Spikes API"
)

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS"
)
if CORS_ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class LessonContentPageViewedEvent(BaseModel):
    eventname: Literal['moodle_lesson_content_page_viewed']
    username: str
    timestamp: int
    course_name: str
    lesson_name: str
    page_title: str


class UserGradedEvent(BaseModel):
    eventname: Literal['moodle_user_graded']
    username: str
    timestamp: int
    course_name: str
    lesson_name: str
    grade: str


class ContentLoadedEvent(BaseModel):
    eventname: Literal['content_loaded']
    user_id: str
    content_id: str
    timestamp: int


Event = Union[
    LessonContentPageViewedEvent,
    UserGradedEvent,
    ContentLoadedEvent
]

@app.post("/events", status_code=201)
async def create_event(event: Event):
    # Depending on settings, store data to S3 or just log
    if EVENTS_S3_BUCKET and EVENTS_S3_PREFIX:
        session = aioboto3.Session()
        async with session.resource("s3") as s3:
            bucket = await s3.Bucket(EVENTS_S3_BUCKET)
            await bucket.put_object(
                Key=f"{EVENTS_S3_PREFIX}/{uuid.uuid4()}.json",
                Body=event.json()
            )
    else:
        print(f"Received event: {event.json()}")

    if KAFKA_BROKERS:
        producer = KafkaProducer( bootstrap_servers=KAFKA_SERVER)
        producer.send(event.eventname, event.json().encode('utf-8'))
        producer.close()
