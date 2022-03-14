from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="RAISE Content API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"]
)


class ContentData(BaseModel):
    id: str
    content: str


@app.get("/contents/{content_id}", response_model=ContentData)
async def create_event(content_id):
    content = f"<div><p>This is content for ID {content_id}</p>" \
        "<p>Math: \\( \\frac{1}{2} \\)</p></div>"
    data = ContentData(id=content_id, content=content)
    return data
