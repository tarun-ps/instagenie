import json
import string
from fastapi.responses import JSONResponse
import uvicorn
from utils.audio import get_audio_project_status
from tasks.audio import get_audio_task_data, process_audio, process_transcript
from utils.assets import get_screen_assets, get_screen_selected_assets
from utils.canva import get_canva_connect_url, get_tokens_from_code
from utils.s3 import upload_file_to_s3
from tasks.csv import process_csv, process_csv_step0, process_csv_step1, process_csv_step2, \
    process_csv_step3, process_csv_step3_with_data, process_csv_step4
from utils.helpers import get_all_data_projects, get_audio_project_assets_status, get_completed_audio_projects, get_completed_data_projects, get_data_project_current_step, get_data_project_step0_data, \
    get_data_project_step0_status, get_data_project_step1_data, get_data_project_step1_status, get_data_project_step2_data, \
    get_data_project_step2_status, get_data_project_step3_data, get_data_project_step3_status, get_data_project_step4_data, get_data_project_step4_status, \
    get_incomplete_audio_projects, get_incomplete_data_projects
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Path, UploadFile
import uuid
import os
import logging
import pandas as pd

logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = fastapi.FastAPI()
origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies and authentication
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

#POST API call to take either a csv file as a FormData or a json with a variable called text as input and process it

# @app.post("/texttask")
# async def submit_text(data: dict):
#     csv_file_id = str(uuid.uuid4())
#     logger.info(f"In server: Processing text for task {csv_file_id}")
#     return JSONResponse(content=process_text(data.get("text"), csv_file_id))

# @app.post("/task")
# async def submit_csv(csv_file: UploadFile):
#     #get the csv file from the request
#     csv_file_id = str(uuid.uuid4())``
#     logger.info(f"In server: Processing csv for task {csv_file_id}")
#     os.makedirs(f"user_data/{csv_file_id}", exist_ok=True)
#     csv_file = await csv_file.read()
#     with open(f"user_data/{csv_file_id}/raw.csv", "wb") as f:
#         f.write(csv_file)
#     return JSONResponse(content=process(csv_file_id))

@app.post("/project")
async def create_project(csv_file: UploadFile):
    csv_file_id = str(uuid.uuid4())
    logger.info(f"In server: Processing csv for project {csv_file_id}")
    os.makedirs(f"user_data/{csv_file_id}", exist_ok=True)
    if csv_file:
        csv_file = await csv_file.read()
        with open(f"user_data/{csv_file_id}/raw.csv", "wb") as f:
            f.write(csv_file)
        process_csv(csv_file_id)
        return JSONResponse(content={"id": csv_file_id, "status": "success"})
    else:
        return JSONResponse(content={"id": csv_file_id, "status": "error"})

@app.get("/project/{project_id}/status")
async def get_current_step(project_id: str):
    return JSONResponse(content=get_data_project_current_step(project_id))

@app.get("/project/{project_id}/step0")
async def get_step0(project_id: str):
    return JSONResponse(content=get_data_project_step0_data(project_id))
    # if os.path.exists(f"user_data/{project_id}/metadata.json"):
    #     with open(f"user_data/{project_id}/metadata.json", "r") as f:
    #         metadata = json.load(f)
    #     df = pd.read_csv(f"user_data/{project_id}/raw.csv")
    #     #replace all nans with None
    #     df = df.fillna(0)
    #     return {"id": project_id, "status": "success", "domain": metadata["preliminary_analyse"]["domain"], 
    #                 "raw_csv": df.head(10).to_dict()}
    # else:
    #     return JSONResponse(content={"id": project_id, "status": "processing"})

@app.get("/project/{project_id}/step0/status")
async def get_step0_status(project_id: str):
    return JSONResponse(content=get_data_project_step0_status(project_id))

@app.get("/project/{project_id}/step1/status")
async def get_step1_status(project_id: str):
    return JSONResponse(content=get_data_project_step1_status(project_id))

@app.get("/project/{project_id}/step2/status")
async def get_step2_status(project_id: str):
    return JSONResponse(content=get_data_project_step2_status(project_id))

@app.get("/project/{project_id}/step3/status")
async def get_step3_status(project_id: str):
    return JSONResponse(content=get_data_project_step3_status(project_id))

@app.get("/project/{project_id}/step4/status")
async def get_step4_status(project_id: str):
    return JSONResponse(content=get_data_project_step4_status(project_id))

@app.post("/project/{project_id}/step1/regenerate")
async def step1regenerate(project_id: str):
    if os.path.exists(f"user_data/{project_id}/metadata.json"):
        data = json.load(open(f"user_data/{project_id}/metadata.json", "r"))
        data["questions"] = []
        with open(f"user_data/{project_id}/metadata.json", "w") as f:
            json.dump(data, f)
    return JSONResponse(content=process_csv_step0(project_id))


@app.post("/project/{project_id}/step3/regenerate")
async def step3regenerate(project_id: str):
    return JSONResponse(content=process_csv_step2(project_id))

@app.post("/project/{project_id}/step4/regenerate")
async def step4regenerate(project_id: str):
    return JSONResponse(content=process_csv_step3(project_id))

@app.get("/project/{project_id}/step1")
async def get_step1(project_id: str):
    return JSONResponse(content=get_data_project_step1_data(project_id))

@app.get("/project/{project_id}/step2")
async def get_step2(project_id: str):
    return JSONResponse(content=get_data_project_step2_data(project_id))

@app.get("/project/{project_id}/step3")
async def get_step3(project_id: str):
    return JSONResponse(content=get_data_project_step3_data(project_id))

@app.get("/project/{project_id}/step4")
async def get_step4(project_id: str):
    return JSONResponse(content=get_data_project_step4_data(project_id))

@app.post("/project/{project_id}/step1/proceed")
async def step1_proceed(project_id: str = Path(...), data: dict = Body(...)):
    return JSONResponse(content=process_csv_step1(project_id, data.get("question")))

@app.post("/project/{project_id}/step2/proceed")
async def step2_proceed(project_id: str, data: dict):
    return JSONResponse(content=process_csv_step2(project_id, data))

@app.post("/project/{project_id}/step3/proceed")
async def step3_proceed(project_id: str, data: dict):
    return JSONResponse(content=process_csv_step3_with_data(project_id, data))

@app.post("/project/{project_id}/step4/proceed")
async def step4_proceed(project_id: str):
    return JSONResponse(content=process_csv_step4(project_id))

# @app.get("/projects/{project_id}/video/{video_id}")
# async def video(project_id: str, video_id: str):
#     return FileResponse(f"user_data/{project_id}/output/output_{video_id}.mp4")

@app.get("/projects")
async def projects():
    projects = get_all_data_projects()
    return JSONResponse(content=projects)

# @app.get("/projects/{project_id}")
# async def project(project_id: str):
#     return JSONResponse(content=get_data_project_data(project_id))

@app.get("/canva-connect")
async def canva_connect():
    return JSONResponse(content={"url": get_canva_connect_url()})

@app.post("/canva-token")
async def canva_token(data: dict):
    return JSONResponse(content=get_tokens_from_code(data.get("code")))

@app.get("/projects/completed")
async def completed_projects():
    return JSONResponse(content=get_completed_data_projects())

@app.get("/projects/incomplete")
async def incomplete_projects():
    return JSONResponse(content=get_incomplete_data_projects())

# @app.get("/test")
# async def test():
#     # with open("data/script_for_transcript.json", "r") as f:
#     #     script = json.load(f)
#     # ret = []
#     # for i, screen in enumerate(script["script_for_timestamp"]):
#     #     screen = ScriptForTimestamp.parse_obj(screen)
#     #     el = screen.to_dict()
#     #     print(f"Screen {i}: {screen}")
#     #     if len(screen.stock_imagery_search_queries) > 0:
#     #         data = json.load(open(f"data/screen_{i}_pexels_images.json", "r"))
#     #         links = [i["src"]["small"] for i in data["photos"]]
#     #         el["stock_imagery_links"] = links
#     #     if len(screen.stock_video_search_queries) > 0:
#     #         data = json.load(open(f"data/screen_{i}_pexels_videos.json", "r"))
#     #         links = [i["video_files"][0]["link"] for i in data["videos"]]
#     #         el["stock_video_links"] = links
#     #     if len(screen.lottie_animations) > 0:
#     #         data = json.load(open(f"data/screen{i}_lottie.json", "r"))
#     #         links = [el["videoSource"] for el in data["data"]["data"]]
#     #         el["lottie_animation_links"] = links
#     #     ret.append(el)
#     ret = json.load(open("data/response_with_swatches.json", "r"))
        
#     return JSONResponse(content=ret)

# @app.post("/submit_assets")
# async def submit_assets(data: dict):
#     print(data)
#     with open("data/selected_assets.json", "w") as f:
#         json.dump(data, f)
#     return JSONResponse(content={"status": "success"})

# @app.get("/screen/{screen_id}/assets")
# async def get_asset(screen_id: int):
#     data = json.load(open("data/downloaded_assets.json", "r"))
#     screen_data = data[screen_id]
#     ret = {}
#     ret["type"] = screen_data["type"]
#     ret["path"] = screen_data["path"]
#     if screen_data["type"] == "image":
#         ret["metadata"] = screen_data["image_metadata"]
#         ret["object"] = None
#         with open(screen_data["path"], "rb") as f:
#             ret["object"] = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
#     if screen_data["type"] == "video":
#         ret["metadata"] = screen_data["video_metadata"]
#         ret["object"] = None
#         with open(screen_data["path"], "rb") as f:
#             ret["object"] = f"data:video/mp4;base64,{base64.b64encode(f.read()).decode('utf-8')}"
#     if screen_data["type"] == "lottie":
#         ret["metadata"] = screen_data["metadata"]
#         ret["object"] = None
#         with open(screen_data["path"], "rb") as f:
#             ret["object"] = f"data:video/mp4;base64,{base64.b64encode(f.read()).decode('utf-8')}"
#     return JSONResponse(content=ret)

# @app.get("/screen/{screen_id}/asset_object")
# async def get_asset_obj(screen_id: int):
#     ret = get_asset_object(screen_id)
#     ret["thumbnailUrl"] = "https://d3v7i4t2a934fu.cloudfront.net/screen_6.jpg"
#     ret["dataUrl"] = "https://d3v7i4t2a934fu.cloudfront.net/screen6_video.mp4"
#     ret["ref"] = "VAGYm1rNVsU"
#     ret["mimeType"] = "video/mp4"
#     ret["type"] = "video"
#     ret["text"] = "the idea of in-app purchases. So it's like small micro consumption moments, which then lead"
#     ret["highlight_words"] = "micro consumption moments funnel".split(" ")
#     ret["text_with_highlights"] = []
#     for word in ret["highlight_words"]:
#         index = ret["text"].find(word)
#         length = len(word)
#         ret["text_with_highlights"].append({"index": index, "length": length, "text": word})
#     return ret

@app.post("/audio_project")
async def audio_project(audio_file: UploadFile):
    logger.info(f"In server: Processing audio project")
    file = await audio_file.read()
    project_id = str(uuid.uuid4())
    os.makedirs(f"user_audio_data/{project_id}", exist_ok=True)
    with open(f"user_audio_data/{project_id}/raw.mp3", "wb") as f:
        f.write(file)
    upload_file_to_s3(f"user_audio_data/{project_id}/raw.mp3", f"user_audio_data/{project_id}/raw.mp3", "audio/mp3")
    return JSONResponse(content=process_audio(project_id))

@app.get("/audio_project/{project_id}")
async def audio_project_data(project_id: str):
    return get_audio_task_data(project_id)

@app.get("/audio_project/{project_id}/status")
async def audio_project_status(project_id: str):
    return JSONResponse(content=get_audio_project_status(project_id))

@app.post("/audio_project/{project_id}/assets")
async def audio_project_assets(project_id: str, data: dict):
    with open(f"user_audio_data/{project_id}/selected_assets.json", "w") as f:
        json.dump(data, f)
    return JSONResponse(content={"status": "success"})

@app.get("/audio_project/{project_id}/assets/status")
async def audio_project_download_assets_status(project_id: str):
    return JSONResponse(content= get_audio_project_assets_status(project_id))

@app.get("/audio_project/{project_id}/screen/{screen_id}/assets")
async def audio_project_assets(project_id: str, screen_id: int):
    return JSONResponse(content=get_screen_assets(project_id, screen_id))

@app.get("/audio_projects/completed")
async def completed_projects():
    return JSONResponse(content=get_completed_audio_projects())

@app.get("/audio_projects/incomplete")
async def incomplete_audio_projects():
    return JSONResponse(content=get_incomplete_audio_projects())

@app.post("/text_project")
async def text_project(data: dict):
    logger.info(f"In server: Processing text project")
    project_id = str(uuid.uuid4())
    os.makedirs(f"user_audio_data/{project_id}", exist_ok=True)
    with open(f"user_audio_data/{project_id}/raw.txt", "w") as f:
        f.write(data.get("text"))
    process_transcript(project_id)
    upload_file_to_s3(f"user_audio_data/{project_id}/raw.mp3", f"user_audio_data/{project_id}/raw.mp3", "audio/mp3")
    return JSONResponse(content=process_audio(project_id))

@app.get("/audio_project/{project_id}/screen/{screen_id}/selected_assets")
async def audio_project_screen_selected_assets(project_id: str, screen_id: int):
    data = get_screen_selected_assets(project_id, screen_id)
    text = data["script"]["text"]
    emphasized_text = data["script"]["emphasized_text"]
    retArray = []
    table = str.maketrans(dict.fromkeys(string.punctuation))
    emphasizedArray = emphasized_text.translate(table).lower().split(" ")
    for word in emphasizedArray:
        index = text.lower().find(word)
        length = len(word)
        retArray.append({"index": index, "length": length, "text": word})
    data["script"]["emphasized_text"] = retArray
    swatches = data["assets"]["details"]["thumbnail"]["swatches"]
    # data["assets"]["details"]["thumbnail"]["path"] = "85b2014a-76b6-4114-a002-cc16be75f90d/screen0/video/video_thumbnail_1_new.png"
    # data["assets"]["details"]["asset"]["path"] = "85b2014a-76b6-4114-a002-cc16be75f90d/screen0/video/video_1.mp4"
    # data["assets"]["type"] = "video"
    # data["assets"]["details"]["asset"]["type"] = "video"
    # data["assets"]["details"]["thumbnail"]["type"] = "video"
    for swatch in swatches.keys():
        el = swatches[swatch]
        data["assets"]["details"]["thumbnail"]["swatches"][swatch] = "#" + "{:02x}{:02x}{:02x}".format(el[0], el[1], el[2])
        data["assets"]["details"]["asset"]["swatches"][swatch] = "#" + "{:02x}{:02x}{:02x}".format(el[0], el[1], el[2])

    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

