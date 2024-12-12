import json
import os

def audio_project_assets_status(project_id: str):
    if not os.path.exists(f"user_audio_data/{project_id}/script.json"):
        return 100, []
    num_screens = len(json.load(open(f"user_audio_data/{project_id}/script.json", "r"))["script_for_timestamp"])
    done_screens = []
    animation_done = False
    video_done = False
    image_done = False
    for i in range(0, num_screens):
        if os.path.exists(f"user_audio_data/{project_id}/screen{i}"):
            if os.path.exists(f"user_audio_data/{project_id}/screen{i}/animation/done") or not os.path.exists(f"user_audio_data/{project_id}/screen{i}/animation/search_query.json"):
                animation_done = True
            if os.path.exists(f"user_audio_data/{project_id}/screen{i}/video/done") or not os.path.exists(f"user_audio_data/{project_id}/screen{i}/video/search_query.json"):
                video_done = True
            if os.path.exists(f"user_audio_data/{project_id}/screen{i}/image/done") or not os.path.exists(f"user_audio_data/{project_id}/screen{i}/image/search_query.json"):
                image_done = True
            if animation_done and video_done and image_done:
                done_screens.append(i)
    return num_screens, done_screens

def get_audio_project_status(project_id: str):
    if os.path.exists(f"user_audio_data/{project_id}/script.json"):
        return {"status": "success", "id": project_id}
    else:
        return {"status": "processing", "id": project_id}