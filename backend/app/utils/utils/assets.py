import json
import os
import requests
from utils.audio import audio_project_assets_status
from utils.helpers import download_file, extract_dominant_color, generate_color_swatches, hex_to_rgb
from utils.s3 import upload_file_to_s3
from settings import ASSET_DOWNLOAD_LIMIT, PEXELS_API_KEY
import magic


def get_mime_type(file_path):
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)


def get_lottie_animation_for_text(text: str):
    query = "+".join(text.split(" "))
    url = f"https://lottiefiles.com/api/search/get-animations?query={query}&type=free&aep=false&sort=popular&page=1&lang=en"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_gcl_au=1.1.1366997735.1732537834; use-thorvg-player-in-homepage=true; enable-homepage-redesign-jan-2024=true; hubspotutk=a46f473f1ea76224915c11aa0c1daa93; __hssrc=1; __eventn_id=ur3hputxc8; growthbook-identifier=cOZCvrjcmxgW1HEg3pfofcqcr8FkkqcNqpNWz4ZR4tIFpezBBVQMGGiC3NO6wT9fE0RvfCeM51xOjYxN7nYLx9pj3C3QPYR4SaOW; ory_kratos_session=MTczMjU0NDY3N3x4WUZFZmRkVWRHLVNob0hXQzFZQUhBalFxS05uMlV4dlJEbTE4S2pCTVNhNS1sWG9zdDFlU3VXcnltTkFwLWVYMlZwdzQ3UnJfOUpIV0Y2WmR0TmVPSksxX19Galp6dVBOWk5zOG52OTJfRW9yZFZldUJVbVQtWnVFejFaVjY5UmM0TmF3M2hqRjU4c2huOE1RWklNc0tYckdhY0hZT2JEVEU0MlVLRmczWkMzX21uRXZXeHhpbXZQeEpsZy1vRlF0X1o2eDY3MVpGeDcwZnVobU1IT2JzT2U3UVh0MDEtdTBzY2hBVGdZNkRVWnVRNldLNUJleldHUGpfSHdVanVOVmdyOG1veV83eDBYbzNjcnZJcWxYdz09fBhJ-KrDHmkO_MHW7pJJVdcSKFmuD2z_3wKvKQqfZRj3; WZRK_G=9662cdc5c0c7444c82e59b337150e094; __eventn_id_usr=%7B%22id%22%3A%229d49f53c-60e8-44b8-8957-ea19abb45f2c%22%2C%22segments%22%3A%5B%22Developer%22%5D%7D; AMP_37255789cb=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMjZUWXY2a01OUmpsaGVCalk1ZE9oMDQlMjIlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMjU0NDkyOTQ4NyUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MzI1NDQ2ODE3NDUlMkMlMjJ1c2VySWQlMjIlM0ElMjI5ZDQ5ZjUzYy02MGU4LTQ0YjgtODk1Ny1lYTE5YWJiNDVmMmMlMjIlN0Q=; _hjSessionUser_1557131=eyJpZCI6ImE1OTY0NGFhLWU2MDUtNTYwNi1hZjA1LTA4YjVhMDk5NDkzMSIsImNyZWF0ZWQiOjE3MzI1NDQ5MzEzNzIsImV4aXN0aW5nIjpmYWxzZX0=; AMP_MKTG_0542f178cb=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmFwcC5sb3R0aWVmaWxlcy5jb20lMkYlMjIlMkMlMjJyZWZlcnJpbmdfZG9tYWluJTIyJTNBJTIyYXBwLmxvdHRpZWZpbGVzLmNvbSUyMiU3RA==; AMP_0542f178cb=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMjI1OGJmNmMwLTdjY2EtNDEwZC04N2Y1LTQ0YmRlZTI1ZTk1NSUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzMyNTQ0OTQ0OTMyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTczMjU0NDkyOTQ3NiUyQyUyMnVzZXJJZCUyMiUzQSUyMjlkNDlmNTNjLTYwZTgtNDRiOC04OTU3LWVhMTlhYmI0NWYyYyUyMiU3RA==; _ga_74MMQ9KR8E=GS1.1.1732544931.1.1.1732544950.41.0.0; lottiefiles_cookie_consent=true; _gid=GA1.2.1485223686.1733483096; amp_9ddfd8=4_dz6ys70sVfGmwuG_JtAE...1iedqhmm7.1iedqj4ld.e.0.e; AMP_MKTG_anykey=JTdCJTIydXRtX21lZGl1bSUyMiUzQSUyMnBsdWdpbi1jYW52YSUyMiUyQyUyMnJlZmVycmVyJTIyJTNBJTIyaHR0cHMlM0ElMkYlMkZ3d3cuY2FudmEuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5jYW52YS5jb20lMjIlN0Q=; AMP_anykey=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0M2VhNjdiZS1kZDZiLTQ0YTktOTEzYi0zMzdjYTc5OGE2N2UlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI5ZDQ5ZjUzYy02MGU4LTQ0YjgtODk1Ny1lYTE5YWJiNDVmMmMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMzNDg0MDUwNjk1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMzQ4NDA1MDk3NCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; __hstc=35243198.a46f473f1ea76224915c11aa0c1daa93.1732537833967.1733483096059.1733486821472.5; amp_372557=6TYv6kMNRjlheBjY5dOh04.OWQ0OWY1M2MtNjBlOC00NGI4LTg5NTctZWExOWFiYjQ1ZjJj..1iedtrfhq.1iedufvp3.17.a.1h; _ga_RRK9MW2TP2=GS1.1.1733486795.7.1.1733489335.59.0.0; _ga=GA1.2.1690241260.1732537834; __hssc=35243198.7.1733486821472; AMP_92dd3459e9=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJjMTM4NGViMy00YmEwLTQzNDUtYjRkZi0yOGZiM2M3ZjVhOGYlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI5ZDQ5ZjUzYy02MGU4LTQ0YjgtODk1Ny1lYTE5YWJiNDVmMmMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMzNDg2ODE0MjgyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMzQ4OTQ0OTkwMyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTY3JTdE',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': f'https://lottiefiles.com/search?category=animations&q={query}&type=free',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
    
def get_pexels_video_for_query(query: str):
    query = "+".join(query.split(" "))
    headers = {
    'Authorization': PEXELS_API_KEY
    }
    payload = {}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&page=1"
    response = requests.request("GET", url, headers=headers)
    return response.json()

def get_pexels_image_for_query(query: str):
    query = "+".join(query.split(" "))
    headers = {
    'Authorization': PEXELS_API_KEY
    }
    payload = {}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&page=1"
    response = requests.request("GET", url, headers=headers)
    return response.json()


def find_pexel_video_link(project_id: str, screen: int, index: int):
    pexel_response = json.load(open(f"user_audio_data/{project_id}/screen{screen}/video/search_query.json", "r"))
    videos = pexel_response["videos"][index]
    min_resolution = float("inf")
    min_video = None
    for video in videos["video_files"]:
        if video["width"] * video["height"] < min_resolution:
            min_resolution = video["width"] * video["height"]
            min_video = video
    thumbnail = videos["image"].split("?")[0] + "?auto=compress&cs=tinysrgb&fit=crop&h=128&w=128"
    min_video["thumbnailUrl"] = thumbnail
    return min_video

def find_pexel_image_link(project_id: str, screen: int, index: int):
    pexel_response = json.load(open(f"user_audio_data/{project_id}/screen{screen}/image/search_query.json", "r"))
    if not pexel_response or not pexel_response.get("photos") or len(pexel_response["photos"]) < index:
        return None
    images = pexel_response["photos"][index]
    ret = {}
    if "src" in images and "portrait" in images["src"]:
        ret["dataUrl"] = images["src"]["portrait"]
        ret["width"] = int(ret["dataUrl"].split("w=")[1].split("&")[0])
        ret["height"] = int(ret["dataUrl"].split("h=")[1].split("&")[0])
    else:
        ret["dataUrl"] = images["src"]["original"]
        ret["width"] = images["width"]
        ret["height"] = images["height"]
    ret["avg_color"] = images["avg_color"]
    #get url path from the url
    # url is of format https://images.pexels.com/videos/853794/free-video-853794.jpg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200
    #replace h and w with 640
    thumbnail = images["src"]["tiny"].split("?")[0] + "?auto=compress&cs=tinysrgb&fit=crop&h=128&w=128"
    ret["thumbnailUrl"] = thumbnail
    ret["mimeType"] = "image/jpeg"
    return ret


def get_screen_selected_assets(project_id: str, screen_id: int):
    selected_assets = json.load(open(f"user_audio_data/{project_id}/selected_assets.json", "r"))
    scripts = json.load(open(f"user_audio_data/{project_id}/script.json", "r"))
    asset = None
    if selected_assets.get("assets") and len(selected_assets["assets"]) > screen_id:
        asset = selected_assets["assets"][screen_id]
    if scripts and scripts.get("script_for_timestamp") and len(scripts["script_for_timestamp"]) > screen_id:
        screen_script = scripts["script_for_timestamp"][screen_id]
    return {"assets": asset, "script": screen_script, "screen_id": screen_id, "id": project_id}

def download_screen_assets(project_id: str, screen_id: int):
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}"):
        os.makedirs(f"user_audio_data/{project_id}/screen{screen_id}")
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/animation"):
        os.makedirs(f"user_audio_data/{project_id}/screen{screen_id}/animation")
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/video"):
        os.makedirs(f"user_audio_data/{project_id}/screen{screen_id}/video")
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/image"):
        os.makedirs(f"user_audio_data/{project_id}/screen{screen_id}/image")
    script = json.load(open(f"user_audio_data/{project_id}/script.json", "r"))
    screen = script["script_for_timestamp"][screen_id]
    if len(screen["lottie_animations"]) > 0:
        try:
            data = get_lottie_animation_for_text(screen["lottie_animations"][0])
            with open(f"user_audio_data/{project_id}/screen{screen_id}/animation/search_query.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(e)
            pass
    if len(screen["stock_video_search_queries"]) > 0:
        try:
            data = get_pexels_video_for_query(screen["stock_video_search_queries"][0])
            with open(f"user_audio_data/{project_id}/screen{screen_id}/video/search_query.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(e)
            pass
    if len(screen["stock_imagery_search_queries"]) > 0:
        try:
            data = get_pexels_image_for_query(screen["stock_imagery_search_queries"][0])
            with open(f"user_audio_data/{project_id}/screen{screen_id}/image/search_query.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(e)
            pass


def download_lottie_animation(project_id: str, screen_id: int):
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/animation/search_query.json"):
        return
    lottie_data = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/animation/search_query.json", "r"))
    dump = []
    if lottie_data and lottie_data.get("data") and lottie_data["data"].get("data") and len(lottie_data["data"]["data"]) > 0:
        l = lottie_data["data"]["data"]
        for i, el in enumerate(l):
            if i >= ASSET_DOWNLOAD_LIMIT:
                break
            lottie_data_response = {}
            swatches = {}
            if el.get("imageSource"):
                imageExt = el["imageSource"].split(".")[-1].split("?")[0]
                imagePath = f"user_audio_data/{project_id}/screen{screen_id}/animation/image_{i}.{imageExt}"
                download_file(el["imageSource"], imagePath)
                imageMimeType = get_mime_type(imagePath)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/animation/image_{i}.{imageExt}", 
                                  imagePath,
                                  imageMimeType)
                swatches = generate_color_swatches(extract_dominant_color(f"user_audio_data/{project_id}/screen{screen_id}/animation/image_{i}.{imageExt}"))
                lottie_data_response["thumbnail"]= {"type": "image", "path": f"{project_id}/screen{screen_id}/animation/image_{i}.png", 
                                             "metadata": {"screen": screen_id, "asset": i, "is_thumbnail": True,
                                                          "width": 640, "height": 640, "mimeType": imageMimeType},
                                             "swatches": swatches}
            if el.get("videoSource"):
                videoPath = f"user_audio_data/{project_id}/screen{screen_id}/animation/video_{i}.mp4"
                download_file(el["videoSource"], videoPath)
                videoMimeType = get_mime_type(videoPath)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/animation/video_{i}.mp4", 
                                  videoPath,
                                  videoMimeType)
                lottie_data_response["asset"] = {"type": "video", "path": f"{project_id}/screen{screen_id}/animation/video_{i}.mp4", 
                                             "metadata": {"screen": screen_id, "asset": i, "is_thumbnail": False,
                                                          "width": 640, "height": 640, "mimeType": videoMimeType},
                                             "swatches": swatches}
            dump.append(lottie_data_response)
    json.dump(dump, open(f"user_audio_data/{project_id}/screen{screen_id}/animation/data_response.json", "w"))
    return


def download_pexels_video_assets(project_id: str, screen_id: int):
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/video/search_query.json"):
        return
    data = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/video/search_query.json", "r"))
    dump = []
    if len(data["videos"]) > 0:
        for i, el in enumerate(data["videos"]):
            if i >= ASSET_DOWNLOAD_LIMIT:
                break
            response = {}
            if el.get("video_files"):
                video = find_pexel_video_link(project_id, screen_id, i)
                ext = video["thumbnailUrl"].split(".")[-1].split("?")[0]
                videoPath = f"user_audio_data/{project_id}/screen{screen_id}/video/video_{i}.mp4"
                thumbnailPath = f"user_audio_data/{project_id}/screen{screen_id}/video/video_thumbnail_{i}.{ext}"
                download_file(video["link"], videoPath)
                download_file(video["thumbnailUrl"], thumbnailPath)
                videoMimeType = get_mime_type(videoPath)
                thumbnailMimeType = get_mime_type(thumbnailPath)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/video/video_{i}.mp4", 
                                  videoPath,
                                  videoMimeType)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/video/video_thumbnail_{i}.{ext}", 
                                  thumbnailPath,
                                  thumbnailMimeType)
                swatches = generate_color_swatches(extract_dominant_color(f"user_audio_data/{project_id}/screen{screen_id}/video/video_thumbnail_{i}.{ext}"))
                response = {"thumbnail": {}}
                response["thumbnail"]["type"] = "video"
                response["thumbnail"]["path"] = f"{project_id}/screen{screen_id}/video/video_thumbnail_{i}.{ext}"
                response["thumbnail"]["metadata"] = {"screen": screen_id, "asset": i, "is_thumbnail": True,
                                          "width": 128, "height": 128, "mimeType": thumbnailMimeType}
                response["thumbnail"]["swatches"] = swatches
                response["asset"] = {}
                response["asset"]["type"] = "video"
                response["asset"]["path"] = f"{project_id}/screen{screen_id}/video/video_{i}.mp4"
                response["asset"]["metadata"] = {"screen": screen_id, "asset": i, "is_thumbnail": False,
                                          "width": video["width"], "height": video["height"], "mimeType": videoMimeType}
                response["asset"]["swatches"] = swatches
                dump.append(response)
    json.dump(dump, open(f"user_audio_data/{project_id}/screen{screen_id}/video/data_response.json", "w"))
    return

def download_pexels_image_assets(project_id: str, screen_id: int):
    if not os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/image/search_query.json"):
        return
    data = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/image/search_query.json", "r"))
    dump = []
    if len(data["photos"]) > 0:
        for i, el in enumerate(data["photos"]):
            if i >= ASSET_DOWNLOAD_LIMIT:
                break
            res = {}
            if el.get("src"):
                image = find_pexel_image_link(project_id, screen_id, i)
                dataExt = image["dataUrl"].split(".")[-1].split("?")[0]
                thumbnailExt = image["thumbnailUrl"].split(".")[-1].split("?")[0]
                imagePath = f"user_audio_data/{project_id}/screen{screen_id}/image/image_{i}.{dataExt}"
                thumbnailPath = f"user_audio_data/{project_id}/screen{screen_id}/image/image_thumbnail_{i}.{thumbnailExt}"
                download_file(image["dataUrl"], imagePath)
                download_file(image["thumbnailUrl"], thumbnailPath)
                imageMimeType = get_mime_type(imagePath)
                thumbnailMimeType = get_mime_type(thumbnailPath)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/image/image_{i}.{dataExt}", 
                                  imagePath,
                                  imageMimeType)
                upload_file_to_s3(f"{project_id}/screen{screen_id}/image/image_thumbnail_{i}.{thumbnailExt}", 
                                  thumbnailPath,
                                  thumbnailMimeType)
                swatches = generate_color_swatches(hex_to_rgb(image["avg_color"]))
                res["thumbnail"] = {"type": "image", "path": f"{project_id}/screen{screen_id}/image/image_thumbnail_{i}.{thumbnailExt}", 
                                    "metadata": {"screen": screen_id, "asset": i, "is_thumbnail": True,
                                          "width": 128, "height": 128, "mimeType": thumbnailMimeType},
                                    "swatches": swatches}
                res["asset"]  = {"type": "image", "path": f"{project_id}/screen{screen_id}/image/image_{i}.{dataExt}", 
                                    "metadata": {"screen": screen_id, "asset": i, "is_thumbnail": False,
                                          "width": image["width"], "height": image["height"], "mimeType": imageMimeType},
                                    "swatches": swatches}
                dump.append(res)
    json.dump(dump, open(f"user_audio_data/{project_id}/screen{screen_id}/image/data_response.json", "w"))
    return

def get_screen_assets(project_id: str, screen_id: int):
    num_screens, done_screens = audio_project_assets_status(project_id)
    if screen_id not in done_screens:
        return {"status": "processing", "num_screens": num_screens, "done_screens": done_screens}
    script = json.load(open(f"user_audio_data/{project_id}/script.json", "r"))
    ret = {}
    ret["script"] = script["script_for_timestamp"][screen_id]
    ret["assets"] = { "lottie": [], "video": [], "image": []}
    if os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/animation/data_response.json"):
        lottie_assets = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/animation/data_response.json", "r"))
        ret["assets"]["lottie"] = lottie_assets
    if os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/video/data_response.json"):
        pexel_video_assets = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/video/data_response.json", "r"))
        ret["assets"]["video"] = pexel_video_assets
    if os.path.exists(f"user_audio_data/{project_id}/screen{screen_id}/image/data_response.json"):
        pexel_image_assets = json.load(open(f"user_audio_data/{project_id}/screen{screen_id}/image/data_response.json", "r"))
        ret["assets"]["image"] = pexel_image_assets
    return ret
