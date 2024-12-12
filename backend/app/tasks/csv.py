from datetime import timedelta
import json
import logging

from utils.s3 import upload_file_to_s3
from utils.canva import create_canva_export_job, generate_design, get_canva_export_job_status, get_canva_job_status, refresh_canva_token
from settings import REDIS_BROKER_URL
from tasks.audio import add_audio_to_video, add_background_music, combine_audio_files, transform_audio_file
from utils.elevenlabs import generate_audio_for_script
from schemas.core import PreliminaryAnalyseResponse
from utils.openai import generate_code, generate_questions, generate_script, preliminary_analyse
from utils.csv import eliminate_unimportant_columns
from utils.helpers import cleanup_folders, download_file
import pandas as pd
from celery import Celery

logger = logging.getLogger(__name__)

celery_app = Celery(__name__, broker=REDIS_BROKER_URL)

celery_app.conf.beat_scheduler = 'celery.beat.PersistentScheduler'
celery_app.conf.beat_schedule_filename = 'celerybeat-schedule'  # File to store the schedule

# Define default settings for tasks
celery_app.conf.update(
    result_backend=REDIS_BROKER_URL,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

celery_app.conf.beat_schedule = {
    'refresh-canva-token-every-241-minutes': {
        'task': 'tasks.csv.refresh_canva_token_task',
        'schedule': 241 * 60,  # Run every 241 minutes
        'args': ()         # Arguments for the task
    },
}

@celery_app.task
def process_csv(project_id: str):
    csv_file_path = f"user_data/{project_id}/raw.csv"
    logger.info(f"In main: Processing csv for task {project_id}")
    cleanup_folders()
    preliminary_analyse_res = preliminary_analyse(csv_file_path)
    eliminate_unimportant_columns(csv_file_path, f"user_data/{project_id}/transformed.csv", preliminary_analyse_res.columns)
    generate_questions_res = generate_questions(preliminary_analyse_res.domain, 
                                                preliminary_analyse_res.columns, 
                                                f"user_data/{project_id}/transformed.csv")
    metadata = {
        "preliminary_analyse": preliminary_analyse_res.to_dict(),
        "questions": generate_questions_res.to_dict(),
    }
    with open(f"user_data/{project_id}/metadata.json", "w") as f:
        json.dump(metadata, f)
    return {"id": project_id, "status": "processing", "domain": preliminary_analyse_res.domain, "questions": generate_questions_res.to_dict()}



def generate_code_and_csv_for_question(project_id: str, question: str):
    with open(f"user_data/{project_id}/metadata.json", "r") as f:
        metadata = json.load(f)
    print(metadata)
    print("Generating code")
    preliminary_analyse_res = PreliminaryAnalyseResponse.model_validate(metadata["preliminary_analyse"])
    try:
        generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                            preliminary_analyse_res.columns, question, 
                                            f"user_data/{project_id}/transformed.csv", f"user_data/{project_id}/code_1.py", 
                                            f"user_data/{project_id}/transformed_1.csv")
        retry = 0
        while retry < 3:
            try:
                exec(generate_code_res.code)
                break
            except Exception as e:
                retry += 1
                print(e)
                print("Retrying")
                generate_code_res = generate_code(preliminary_analyse_res.domain, 
                                        preliminary_analyse_res.columns, question, 
                                        f"user_data/{project_id}/transformed.csv", f"user_data/{project_id}/code_1.py", 
                                        f"user_data/{project_id}/transformed_1.csv")
    except Exception as e:
        print(e)
    transformed_csv = pd.read_csv(f"user_data/{project_id}/transformed_1.csv")
    return transformed_csv.to_dict()


def process_csv_step0(project_id: str):
    logger.info(f"In main: Generating questions for task {project_id}")
    process_csv_step0_task.delay(project_id)
    return {"id": project_id, "status": "processing"}


@celery_app.task
def process_csv_step0_task(project_id: str):
    logger.info(f"In task: Generating questions for task {project_id}")
    with open(f"user_data/{project_id}/metadata.json", "r") as f:
        metadata = json.load(f)
    res = generate_questions(metadata["preliminary_analyse"]["domain"], metadata["preliminary_analyse"]["columns"], f"user_data/{project_id}/transformed.csv")
    metadata["questions"] = res.to_dict()
    with open(f"user_data/{project_id}/metadata.json", "w") as f:
        json.dump(metadata, f)
    return {"id": project_id, "status": "success"}

def process_csv_step1(project_id: str, question: str):
    logger.info(f"In main: Processing csv for task {project_id}")
    logger.info(question)
    with open(f"user_data/{project_id}/metadata.json", "r") as f:
        metadata = json.load(f)
    metadata["chosen_question"] = question
    with open(f"user_data/{project_id}/metadata.json", "w") as f:
        json.dump(metadata, f)
    process_csv_step1_task.delay(project_id)
    return {"id": project_id, "status": "success"}

@celery_app.task
def process_csv_step1_task(project_id: str):
    logger.info(f"In task: Processing csv for task {project_id}")
    with open(f"user_data/{project_id}/metadata.json", "r") as f:
        metadata = json.load(f)
    print(metadata)
    transformed_csv = generate_code_and_csv_for_question(project_id, metadata["chosen_question"])
    return {"id": project_id, "status": "success"}

def process_csv_step2(project_id: str, data: dict):
    logger.info(f"In main: Processing step 2 for csv for task {project_id}")
    with open(f"user_data/{project_id}/user_submitted_graph.json", "w") as f:
        json.dump(data, f)
    process_csv_step2_task.delay(project_id)
    return {"id": project_id, "status": "success"}

@celery_app.task
def process_csv_step2_task(project_id: str):
    logger.info(f"In task: Processing step 2 for csv for task {project_id}")
    with open(f"user_data/{project_id}/metadata.json", "r") as f:
        metadata = json.load(f)
    script_res = generate_script(project_id, metadata["chosen_question"], metadata["preliminary_analyse"]["domain"])
    with open(f"user_data/{project_id}/script.json", "w") as f:
        json.dump(script_res.to_dict(), f)
    return {"id": project_id, "status": "success"}

def process_csv_step3(project_id: str):
    logger.info(f"In main: Processing step 3 for csv for task {project_id}")
    process_csv_step3_task.delay(project_id)
    return {"id": project_id, "status": "success"}

def process_csv_step3_with_data(project_id: str, data: dict):
    logger.info(f"In main: Processing step 3 for csv for task {project_id}")
    with open(f"user_data/{project_id}/user_submitted_script.json", "w") as f:
        json.dump(data, f)
    process_csv_step3_task.delay(project_id)
    return {"id": project_id, "status": "success"}

@celery_app.task
def process_csv_step3_task(project_id: str):
    logger.info(f"In task: Processing step 3 for csv for task {project_id}")
    script = json.load(open(f"user_data/{project_id}/user_submitted_script.json", "r"))["editted_script"]
    lengths = [5, 5, 10, 6, 4]
    for i in range(1, 6):
        previous_voice_over = script[f"screen_{i-1}"]["voice_over"] if i > 1 else ""
        next_voice_over = script[f"screen_{i+1}"]["voice_over"] if i < 5 else ""
        generate_audio_for_script(script[f"screen_{i}"]["voice_over"], 
                                f"user_data/{project_id}/audio_{i}.mp3", 
                                previous_voice_over, next_voice_over)
        transform_audio_file(f"user_data/{project_id}/audio_{i}.mp3", f"user_data/{project_id}/audio_{i}_transformed.mp3", lengths[i-1])
    combine_audio_files(project_id)
    add_background_music(f"user_data/{project_id}/output.mp3", project_id, 7)
    generate_design(project_id)
    check_canva_job_status.delay(project_id)
    return {"id": project_id, "status": "success"}

def process_csv_step4(project_id: str):
    logger.info(f"In main: Processing step 4 for csv for task {project_id}")
    process_csv_step4_task.delay(project_id)
    return {"id": project_id, "status": "success"}

@celery_app.task
def process_csv_step4_task(project_id: str):
    logger.info(f"In task: Processing step 4 for csv for task {project_id}")
    check_canva_job_status.delay(project_id)

@celery_app.task(bind=True, max_retries=3)
def check_canva_job_status(self, project_id: str):
    logger.info(f"In task: Checking canva job status for task {project_id}")
    res = get_canva_job_status(project_id)
    if res["job"]["status"] == "success":
        with open(f"user_data/{project_id}/job.json", "w") as f:
            json.dump(res, f)
        create_canva_export_job(project_id)
        check_canva_export_job_status.delay(project_id)
    else:
        with open(f"user_data/{project_id}/job_incomplete.json", "w") as f:
            json.dump(res, f)
        raise self.retry(countdown=5)

@celery_app.task(bind=True, max_retries=5)
def check_canva_export_job_status(self, project_id: str):
    logger.info(f"In task: Checking canva export job status for task {project_id}")
    res = get_canva_export_job_status(project_id)
    try:
        if res["job"]["status"] == "success":
            with open(f"user_data/{project_id}/export.json", "w") as f:
                json.dump(res, f)
            finalise_project.delay(project_id)
        else:
            raise Exception("Canva export job not completed")
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
    
@celery_app.task
def finalise_project(project_id: str):
    logger.info(f"In task: Finalising project {project_id}")
    with open(f"user_data/{project_id}/export.json", "r") as f:
        export = json.load(f)
    design_job = json.load(open(f"user_data/{project_id}/job.json", "r"))
    design = design_job["job"]["result"]["design"]
    download_file(export["job"]["urls"][0], f"user_data/{project_id}/export.mp4")
    add_audio_to_video(project_id)
    upload_file_to_s3(f"user_data/{project_id}/final_output.mp4", f"user_data/{project_id}/final_output.mp4", "video/mp4")
    upload_file_to_s3(f"user_data/{project_id}/final.mp3", f"user_data/{project_id}/final.mp3", "audio/mp3")
    #add background music and upload to s3
    final_outout = {
        "video_url": f"user_data/{project_id}/final_output.mp4",
        "audio_url": f"user_data/{project_id}/final.mp3",
        "canva_url": design["urls"]["edit_url"]
    }
    with open(f"user_data/{project_id}/final_output.json", "w") as f:
        json.dump(final_outout, f)
    return {"id": project_id, "status": "success"}

@celery_app.task
def refresh_canva_token_task():
    refresh_canva_token()