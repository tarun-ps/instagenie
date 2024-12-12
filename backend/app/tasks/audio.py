import math
import os
from tasks.assets import download_assets_task
from utils.elevenlabs import generate_audio_for_script
from utils.openai import generate_script_for_transcript
from settings import CDN_URL, REDIS_BROKER_URL

import json
from pydub import AudioSegment
from celery import Celery

celery_app = Celery(__name__, broker=REDIS_BROKER_URL)

def transform_audio_file(input_file_path: str, output_file_path: str, length_in_seconds: int):
    audio = AudioSegment.from_file(input_file_path, format="mp3")
    input_length = len(audio)/1000
    if input_length > length_in_seconds:
        speed = input_length / length_in_seconds
        print(f"Input audio is longer than {length_in_seconds} seconds. Speeding up. Speed: {speed}")
        os.system(f"ffmpeg -i {input_file_path} -filter:a \"atempo={speed}\" {output_file_path} -y")
    else:
        temp_path = "temp.mp3"
        os.remove(temp_path)
        padding_length = int((length_in_seconds - input_length) * 1000 / 2) 
        print(f"Input audio is shorter than {length_in_seconds} seconds. Slowing down. Padding length: {padding_length}, input length: {input_length} seconds output length: {length_in_seconds} seconds")
        os.system(f"ffmpeg -i {input_file_path} -af \"adelay={padding_length}|{padding_length}\" {temp_path} -y")
        os.system(f"ffmpeg -i {temp_path} -af \"apad=pad_dur={padding_length/1000}\" -t {length_in_seconds} {output_file_path} -y")
    return


def combine_audio_files(project_id: str):
    os.system(f"cp user_data/file_list.txt user_data/{project_id}/file_list.txt")
    os.system(f"ffmpeg -f concat -safe 0 -i user_data/{project_id}/file_list.txt -c copy user_data/{project_id}/output.mp3 -y")
    return

def add_background_music(input_file_path: str, project_id: str, bg_music_index: int):
    os.system(f"ffmpeg -i {input_file_path} -i data/bg_music_{bg_music_index}.mp3 -filter_complex \"[0:a]volume=1.0[a0];[1:a]volume=0.3[a1];[a0][a1]amix=inputs=2:duration=longest:dropout_transition=2\" user_data/{project_id}/final.mp3 -y")
    return

def process_audio(project_id: str):
    process_audio_task.delay(project_id)
    return {"status": "processing", "id": project_id}

@celery_app.task
def process_audio_task(project_id: str):
    import whisper
    whisper_model = whisper.load_model("base.en")
    filepath = f"user_audio_data/{project_id}/raw.mp3"
    result = whisper_model.transcribe(filepath)
    json.dump(result, open(f"user_audio_data/{project_id}/transcript.json", "w"))
    generate_script_for_project(project_id)
    download_assets_task.delay(project_id)

def generate_script_for_project(project_id: str):
    transcript = json.load(open(f"user_audio_data/{project_id}/transcript.json", "r"))
    text = transcript["text"]
    sentences = []
    length = math.ceil(transcript["segments"][-1]["end"])
    j = 0
    for i in range(0, length, 5):
        o = {}
        o["start"] = i
        o["end"] = i+5
        o["text"] = ""
        while True:
            try:
                if i+5 > transcript["segments"][j]["end"]:
                    o["text"] += transcript["segments"][j]["text"]
                    j += 1
                else:
                    break
            except:
                break
        sentences.append(o)
    print(sentences)
    f = {"text": text, "segments": sentences}
    json.dump(f, open(f"user_audio_data/{project_id}/segmented_transcript.json", "w"))
    script = generate_script_for_transcript(f)
    json.dump(script.to_dict(), open(f"user_audio_data/{project_id}/script.json", "w"))
    return


def process_transcript(project_id: str):
    script_text = open(f"user_audio_data/{project_id}/raw.txt", "r").read()
    generate_audio_for_script(script_text, f"user_audio_data/{project_id}/raw.mp3", "", "")
    return {"status": "completed", "id": project_id, }

def get_audio_task_data(project_id: str):
    audio_url = CDN_URL + f"user_audio_data/{project_id}/raw.mp3"
    if not os.path.exists(f"user_audio_data/{project_id}/transcript.json"):
        return {"status": "incomplete"}
    transcript = json.load(open(f"user_audio_data/{project_id}/transcript.json", "r"))
    script = json.load(open(f"user_audio_data/{project_id}/script.json", "r"))
    if os.path.exists(f"user_audio_data/{project_id}/selected_assets.json"):
        selected_assets = json.load(open(f"user_audio_data/{project_id}/selected_assets.json", "r"))
    else:
        selected_assets = []
    ret = {}
    ret["audio_url"] = audio_url
    ret["transcript"] = transcript["text"]
    ret["script"] = script
    ret["selected_assets"] = selected_assets
    return {"status": "completed", "data": ret}

def add_audio_to_video(project_id: str):
    os.system(f"ffmpeg -i user_data/{project_id}/export.mp4 -i user_data/{project_id}/final.mp3 -c:v copy -c:a aac -strict experimental user_data/{project_id}/final_output.mp4 -y")

