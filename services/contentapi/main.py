from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="RAISE Content API"
)


class ContentData(BaseModel):
    id: str
    content: str


@app.get("/contents/{content_id}", response_model=ContentData)
async def create_event(content_id):
    content = f"<div><p>This is content for ID {content_id}</p></div>"
    data = ContentData(id=content_id, content=content)
    return data
