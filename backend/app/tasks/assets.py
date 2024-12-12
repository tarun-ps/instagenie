import json
from utils.assets import download_lottie_animation, download_pexels_image_assets, download_pexels_video_assets, download_screen_assets
from celery import Celery
from settings import REDIS_BROKER_URL
celery_app = Celery(__name__, broker=REDIS_BROKER_URL)

@celery_app.task
def download_assets_task(project_id: str):
    num_screens = len(json.load(open(f"user_audio_data/{project_id}/script.json", "r"))["script_for_timestamp"])
    for i in range(0, num_screens):
        download_screen_assets(project_id, i)
        download_lottie_animation_task.delay(project_id, i)
        download_pexels_video_assets_task.delay(project_id, i)
        download_pexels_image_assets_task.delay(project_id, i)

@celery_app.task
def download_lottie_animation_task(project_id: str, screen_id: int):
    download_lottie_animation(project_id, screen_id)
    with open(f"user_audio_data/{project_id}/screen{screen_id}/animation/done", "w") as f:
        f.write("done")

@celery_app.task
def download_pexels_video_assets_task(project_id: str, screen_id: int):
    download_pexels_video_assets(project_id, screen_id)
    with open(f"user_audio_data/{project_id}/screen{screen_id}/video/done", "w") as f:
        f.write("done")

@celery_app.task
def download_pexels_image_assets_task(project_id: str, screen_id: int):
    download_pexels_image_assets(project_id, screen_id)
    with open(f"user_audio_data/{project_id}/screen{screen_id}/image/done", "w") as f:
        f.write("done")
