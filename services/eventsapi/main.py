from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import aioboto3
import uuid
import os

EVENTS_S3_BUCKET = os.getenv("EVENTS_S3_BUCKET")
EVENTS_S3_PREFIX = os.getenv("EVENTS_S3_PREFIX")

app = FastAPI(
    title="RAISE Spikes API"
)


class Event(BaseModel):
    username: str
    eventname: str
    timestamp: int
    course_name: str
    lesson_name: str
    page_title: Optional[str]
    grade: Optional[str]


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
