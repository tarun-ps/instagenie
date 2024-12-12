import colorsys
import json
import os
import pandas as pd
from utils.audio import audio_project_assets_status

def get_all_data_projects():
    ret = []
    for project_id in os.listdir("user_data"):
        domain = get_data_project_domain(project_id)
        ret.append({"id": project_id, "domain": domain})
    return ret

def get_data_project_domain(project_id: str):
    metadata = json.load(open(f"user_data/{project_id}/metadata.json"))
    return metadata["preliminary_analyse"]["domain"]

# def get_data_project_data(project_id: str):
#     metadata = json.load(open(f"user_data/{project_id}/metadata.json"))
#     files = os.listdir(f"user_data/{project_id}/output")
#     videos = [file for file in files if file.endswith(".mp4")]
#     ret = {}
#     ret["id"] = project_id
#     ret["domain"] = metadata["preliminary_analyse"]["domain"]
#     questions = metadata["questions"]["questions"]
#     ret_questions = []
#     for i, question in enumerate(questions):
#         if f"output_{i}.mp4" in videos:
#             ret_questions.append({"question": question, "video": f"{project_id}/video/{i}", "status": "ready"})
#         else:
#             ret_questions.append({"question": question, "video": None, "status": "processing"})
#     ret["questions"] = ret_questions
#     return ret


def cleanup_folders():
    os.system("rm -rf output/*")
    os.system("rm -rf code/*")
    os.system("rm -rf frames/*")
    os.system("rm -rf data/transformed_*.csv")


def generate_color_swatches(rgb_color):
    """
    Generate Light Vibrant, Vibrant, Dark Vibrant, Light Muted, Muted, Dark Muted swatches.
    :param rgb_color: Tuple of RGB values (R, G, B), each between 0-255.
    :return: Dictionary with swatch names and corresponding RGB colors.
    """
    # Normalize RGB to [0, 1]
    r, g, b = [x / 255.0 for x in rgb_color]

    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # Define swatches with lightness and saturation adjustments
    swatches = {
        "light_vibrant": colorsys.hls_to_rgb(h, min(l + 0.3, 1.0), min(s + 0.3, 1.0)),
        "vibrant": colorsys.hls_to_rgb(h, l, min(s + 0.4, 1.0)),
        "dark_vibrant": colorsys.hls_to_rgb(h, max(l - 0.3, 0.0), min(s + 0.4, 1.0)),
        "light_muted": colorsys.hls_to_rgb(h, min(l + 0.3, 1.0), max(s - 0.4, 0.0)),
        "muted": colorsys.hls_to_rgb(h, l, max(s - 0.4, 0.0)),
        "dark_muted": colorsys.hls_to_rgb(h, max(l - 0.3, 0.0), max(s - 0.4, 0.0)),
    }

    # Convert back to RGB [0, 255]
    swatches = {name: tuple(int(x * 255) for x in rgb) for name, rgb in swatches.items()}

    return swatches


def download_file(url: str, path: str="temp_image.png"):
    import requests
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)
    return path


def extract_dominant_color(image_path: str):
    import extcolors
    colors, pixel_count = extcolors.extract_from_path(image_path)
    return colors[0][0]

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_project_folder(project_id: str):
    os.makedirs(f"user_data/{project_id}", exist_ok=True)
    os.makedirs(f"user_data/{project_id}/code", exist_ok=True)
    os.makedirs(f"user_data/{project_id}/frames", exist_ok=True)
    os.makedirs(f"user_data/{project_id}/output", exist_ok=True)

def get_completed_data_projects():
    completed_projects = []
    for project_id in os.listdir("user_data"):
        if os.path.exists(f"user_data/{project_id}/job.json"):
            completed_projects.append(project_id)
    ret = []
    for project_id in completed_projects:
        with open(f"user_data/{project_id}/job.json", "r") as f:
            job = json.load(f)
            if not job.get("job"):
                continue
        with open(f"user_data/{project_id}/metadata.json", "r") as f:
            metadata = json.load(f)
        ret.append({"id": project_id, "status": "completed", "job": job.get("job"), "domain": metadata["preliminary_analyse"]["domain"]})
    return ret

def get_completed_audio_projects():
    completed_projects = []
    for project_id in os.listdir("user_audio_data"):
        if os.path.exists(f"user_audio_data/{project_id}/selected_assets.json"):
            completed_projects.append(project_id)
    ret = []
    for project_id in completed_projects:
        with open(f"user_audio_data/{project_id}/selected_assets.json", "r") as f:
            selected_assets = json.load(f)
            if len(selected_assets.get("assets")) == 0:
                continue
        with open(f"user_audio_data/{project_id}/script.json", "r") as f:
            script = json.load(f)
        ret.append({"id": project_id, "status": "completed", "script": script, "selected_assets": selected_assets})
    return ret

def get_incomplete_audio_projects():
    incomplete_projects = []
    for project_id in os.listdir("user_audio_data"):
        if not os.path.isdir(f"user_audio_data/{project_id}"):
            continue
        if not os.path.exists(f"user_audio_data/{project_id}/job.json"):
            incomplete_projects.append(project_id)
    ret = []
    for project_id in incomplete_projects:
        if os.path.exists(f"user_audio_data/{project_id}/script.json"):
            with open(f"user_audio_data/{project_id}/script.json", "r") as f:
                script = json.load(f)
            ret.append({"id": project_id, "status": "incomplete", "script": script})
    return ret

def get_incomplete_data_projects():
    incomplete_projects = []
    for project_id in os.listdir("user_data"):
        if not os.path.isdir(f"user_data/{project_id}"):
            continue
        if not os.path.exists(f"user_data/{project_id}/job.json"):
            incomplete_projects.append(project_id)
    ret = []
    for project_id in incomplete_projects:
        if os.path.exists(f"user_data/{project_id}/metadata.json"):
            with open(f"user_data/{project_id}/metadata.json", "r") as f:
                metadata = json.load(f)
            ret.append({"id": project_id, "status": "incomplete", "metadata": metadata})
    return ret

def get_data_project_step0_status(project_id: str):
    if os.path.exists(f"user_data/{project_id}/metadata.json"):
        return {"id": project_id, "status": "success"}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step1_status(project_id: str):
    if os.path.exists(f"user_data/{project_id}/metadata.json"):
        with open(f"user_data/{project_id}/metadata.json", "r") as f:
            metadata = json.load(f)
        if metadata.get("questions") and len(metadata["questions"]["questions"]) > 0:
            return {"id": project_id, "status": "success"}
        else:
            return {"id": project_id, "status": "error"}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step2_status(project_id: str):
    if os.path.exists(f"user_data/{project_id}/transformed_1.csv"):
        return {"id": project_id, "status": "success"}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step3_status(project_id: str):
    if os.path.exists(f"user_data/{project_id}/script.json"):
        return {"id": project_id, "status": "success"}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step4_status(project_id: str):
    if os.path.exists(f"user_data/{project_id}/final_output.json"):
        return {"id": project_id, "status": "success"}
    else:
        return {"id": project_id, "status": "error"}

# def get_data_project_step5_status(project_id: str):
#     if os.path.exists(f"user_data/{project_id}/design.json"):
#         return {"id": project_id, "status": "success"}
#     else:
#         return {"id": project_id, "status": "error"}

# def get_data_project_step6_status(project_id: str):
#     pass

def get_audio_project_creation_status(project_id: str):
    pass

def get_audio_project_assets_status(project_id: str):
    num_screens, done_screens = audio_project_assets_status(project_id)
    if len(done_screens) == num_screens:
        return {"status": "success", "num_screens": num_screens, "done_screens": done_screens}
    else:
        return {"status": "processing", "num_screens": num_screens, "done_screens": done_screens}

def get_audio_project_assets_status_for_screen(project_id: str, screen_id: str):
    pass

def get_data_project_step0_data(project_id: str):
    if os.path.exists(f"user_data/{project_id}/metadata.json"):
        with open(f"user_data/{project_id}/metadata.json", "r") as f:
            metadata = json.load(f)
            df = pd.read_csv(f"user_data/{project_id}/raw.csv")
            #replace all nans with None
            df = df.fillna(0)
            return {"id": project_id, "status": "success", "domain": metadata["preliminary_analyse"]["domain"],
                    "raw_csv": df.head(10).to_dict()}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step1_data(project_id: str):
    if os.path.exists(f"user_data/{project_id}/metadata.json"):
        with open(f"user_data/{project_id}/metadata.json", "r") as f:
            metadata = json.load(f)
            if metadata.get("questions") and len(metadata["questions"]["questions"]) > 0:
                return {"id": project_id, "status": "success", "questions": metadata["questions"]["questions"]}
            else:
                return {"id": project_id, "status": "error"}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step2_data(project_id: str):
    if os.path.exists(f"user_data/{project_id}/transformed_1.csv"):
        df = pd.read_csv(f"user_data/{project_id}/transformed_1.csv")
        df = df.fillna('')
        return {"id": project_id, "status": "success", "transformed_csv": df.to_dict()}
    else:
        return {"id": project_id, "status": "error"}
    
def get_data_project_step3_data(project_id: str):
    if os.path.exists(f"user_data/{project_id}/script.json"):
        with open(f"user_data/{project_id}/script.json", "r") as f:
            script = json.load(f)
        return {"id": project_id, "status": "success", "script": script}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step4_data(project_id: str):
    if os.path.exists(f"user_data/{project_id}/final_output.json"):
        with open(f"user_data/{project_id}/final_output.json", "rb") as f:
            final_output = json.load(f)
        return {"id": project_id, "status": "success", "results": final_output}
    else:
        return {"id": project_id, "status": "error"}

def get_data_project_step5_data(project_id: str):
    pass

def get_data_project_step6_data(project_id: str):
    pass

def get_data_project_current_step(project_id: str):
    if os.path.exists(f"user_data/{project_id}/design.json"):
        return {"id": project_id, "status": "success", "step": 5}
    elif os.path.exists(f"user_data/{project_id}/job.json"):
        return {"id": project_id, "status": "success", "step": 4}
    elif os.path.exists(f"user_data/{project_id}/script.json") and os.path.exists(f"user_data/{project_id}/user_submitted_graph.json") :
        return {"id": project_id, "status": "success", "step": 3}
    elif os.path.exists(f"user_data/{project_id}/transformed_1.csv"):
        return {"id": project_id, "status": "success", "step": 2}
    elif os.path.exists(f"user_data/{project_id}/metadata.json"):
        return {"id": project_id, "status": "success", "step": 1}
    else:
        return {"id": project_id, "status": "error", "step": 0}
    
