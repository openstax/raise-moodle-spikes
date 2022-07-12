from typing import Literal, Union
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import aioboto3
import uuid
import os
import logging
logging.basicConfig(level=logging.DEBUG)


EVENTS_S3_BUCKET = os.getenv("EVENTS_S3_BUCKET")
EVENTS_S3_PREFIX = os.getenv("EVENTS_S3_PREFIX")
KAFKA_LISTENER = os.getenv("KAFKA_ADVERTISED_LISTENERS")

KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "eventsapi"

app = FastAPI(
    title="RAISE Spikes API"
)

class LessonContentPageViewedEvent(BaseModel):
    eventname: Literal['\\mod_lesson\\event\\content_page_viewed']
    username: str
    timestamp: int
    course_name: str
    lesson_name: str
    page_title: str


class UserGradedEvent(BaseModel):
    eventname: Literal['\\core\\event\\user_graded']
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

    #ignoring case where I need to check kafka env variable for now. 
    
    producer = KafkaProducer( bootstrap_servers=KAFKA_SERVER, api_version=(2, 0, 2))
    producer.send(KAFKA_TOPIC, b'Some message')

    producer.close()
