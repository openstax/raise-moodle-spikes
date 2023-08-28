from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union, Dict
from pathlib import Path
import json

DEFAULT_CONTENT_TEMPLATE = "<div><p>This is content for ID {}</p>" \
    "<p>Math: \\( \\frac{{1}}{{2}} \\)</p></div>"


HTML_DATA_PATH = "/content/html"
JSON_DATA_PATH = "/content/json"


app = FastAPI(
    title="RAISE Content API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"]
)


class ContentItem(BaseModel):
    variant: str
    html: str


class ContentData(BaseModel):
    id: str
    content: List[ContentItem]


ResponseModel = Union[
    ContentData,
    Dict[str, str],
]


def get_variants_json_from_uuid(html_directory, content_id):
    if not Path(f"{html_directory}/{content_id}.html").is_file():
        return None
    else:
        variant_list = []
        with open(f"{html_directory}/{content_id}.html") as f:
            file_content = f.read()
            variant_list.append({"variant": "main", "html": file_content})

        if Path(f'{html_directory}/{content_id}').is_dir():
            dir_path = Path(f"{html_directory}/{content_id}")
            for f_name in dir_path.iterdir():
                with open(dir_path / f"{f_name.name}") as variant_file:
                    variant_list.append(
                        {
                            "variant": f"{Path(f_name.name).stem}",
                            "html": variant_file.read()
                        }
                    )

        json_content = {
            "id": content_id,
            "content": variant_list
        }
        return json_content


@app.get("/contents/{version_id}/{content_id}.json",
         response_model=ResponseModel)
@app.get("/contents/{content_id}.json", response_model=ResponseModel)
async def get_content(content_id):
    if Path(f"{JSON_DATA_PATH}/{content_id}.json").is_file():
        with open(f"{JSON_DATA_PATH}/{content_id}.json") as f:
            file_content = json.load(f)
        return file_content
    data = get_variants_json_from_uuid(HTML_DATA_PATH, content_id)

    items = []
    if data is None:
        content = DEFAULT_CONTENT_TEMPLATE.format(content_id)
        items.append(ContentItem(variant='main', html=content))
    else:
        for variant_obj in data["content"]:
            name = variant_obj["variant"]
            html = variant_obj["html"]
            items.append(ContentItem(variant=name, html=html))
    package = ContentData(id=content_id, content=items)
    return package
