# from typing import Annotated
from fastapi import *
from fastapi import staticfiles
from fastapi.responses import FileResponse
import os
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
import uuid 


app = FastAPI(
    # title='Project NOA',
    # description='video upload download server',
    # openapi_url='/api/openapi.json'
)
# @app.get("sys")
# def create_api(app: FastAPI):
#     @app.get(app.root_path + "/openapi.json")
#     def custom_swagger_ui_html():
#         return app.openapi()

# create_api()

# @app.get("/doca", include_in_schema=False)
# async def custom_swagger_ui_html(req: Request):
#     root_path = req.scope.get("root_path", "").rstrip("/")
#     openapi_url = root_path + app.openapi_url
#     return get_swagger_ui_html(
#         openapi_url=openapi_url,
#         title="API",
    # )

@app.post("/upload_video")
async def upload_video(file: UploadFile):
    UPLOAD_DIR = "./video"
    content = await file.read()
    filename = f"{str(uuid.uuid4())}.mp4"
    # filename = "video.mp4"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content) 
    return {"filename": filename}

@app.get("/download/video/{video_id}")
async def download_video(file: FileResponse, video_id: str): 
    return FileResponse(f'./video/{video_id}.mp4')

@app.get('/process/{video_id}')
async def process_video(video_id: str):
    os.system('echo is working')
    return "waiting progress"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
