import json
import random
import string
import base64
import hashlib
import pandas as pd
import requests
import urllib.parse
from settings import CANVA_REDIRECT_URL
from schemas.core import GenerateScriptResponse
import numpy as np
from settings import CANVA_BASIC_AUTH

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def get_canva_connect_url():
    redirect_url = urllib.parse.quote_plus(CANVA_REDIRECT_URL)
    code_verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=96))
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    url = f"https://www.canva.com/api/oauth/authorize?code_challenge_method=s256&response_type=code&client_id=OC-AZOGi6NcDf8k&redirect_uri={redirect_url}&scope=app:read%20app:write%20design:content:read%20design:meta:read%20design:content:write%20design:permission:read%20design:permission:write%20folder:read%20folder:write%20folder:permission:read%20folder:permission:write%20asset:read%20asset:write%20comment:read%20comment:write%20brandtemplate:meta:read%20brandtemplate:content:read%20profile:read&code_challenge={code_challenge}"
    code_challenge_url = url
    with open("data/canva_connect_url.json", "w") as f:
        json.dump({"code_challenge": code_challenge, 
                   "code_challenge_url": code_challenge_url,
                   "code_verifier": code_verifier}, f)
    return code_challenge_url

def get_tokens_from_code(code: str):
    with open("data/canva_connect_url.json", "r") as f:
        data = json.load(f)
    headers = {
        "Authorization": f"Basic {CANVA_BASIC_AUTH}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    code_verifier = data["code_verifier"]
    data = {
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": CANVA_REDIRECT_URL,
    }

    response = requests.post("https://api.canva.com/rest/v1/oauth/token",
        headers=headers,
        data=data
    )
    print(response.json())
    with open("data/canva_tokens.json", "w") as f:
        json.dump(response.json(), f)
    return response.json()

def get_canva_job_status(project_id: str):
    with open("data/canva_tokens.json", "r") as f:
        data = json.load(f)
    with open(f"user_data/{project_id}/design.json", "r") as f:
        job_id = json.load(f)["job"]["id"]
    headers = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    response = requests.get(f"https://api.canva.com/rest/v1/autofills/{job_id}", headers=headers)
    json.dump(response.json(), open(f"user_data/{project_id}/job_temp.json", "w"))
    return response.json()

def get_canva_export_job_status(project_id: str):
    with open("data/canva_tokens.json", "r") as f:
        data = json.load(f)
    with open(f"user_data/{project_id}/export_job.json", "r") as f:
        export_job = json.load(f)
    headers = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    response = requests.get(f"https://api.canva.com/rest/v1/exports/{export_job['job']['id']}",
        headers=headers
    )
    json.dump(response.json(), open(f"user_data/{project_id}/export_job_intermediate.json", "w"))
    return response.json()

def create_canva_export_job(project_id: str):
    with open("data/canva_tokens.json", "r") as f:
        data = json.load(f)
    headers = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    with open(f"user_data/{project_id}/job.json", "r") as f:
        job = json.load(f)
    design_id = job["job"]["result"]["design"]["id"]
    req = {
        "design_id": design_id,
        "format": {"type": "mp4", "quality": "vertical_480p"},
    }
    response = requests.post(f"https://api.canva.com/rest/v1/exports", headers=headers, json=req)
    json.dump(response.json(), open(f"user_data/{project_id}/export_job.json", "w"))
    return response.json()

def create_canva_autofill_job(project_id: str):
    with open(f"user_data/{project_id}/design.json", "r") as f:
        design = json.load(f)
    import requests
    job_id = design["job"]["id"]
    url = f"https://api.canva.com/rest/v1/autofills/{job_id}"
    with open("data/canva_tokens.json", "r") as f:
        canva_tokens = json.load(f)
    access_token = canva_tokens["access_token"]
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.json()
    with open(f"user_data/{project_id}/job.json", "w") as f:
        json.dump(res, f)


def generate_design(project_id: str):
    url = "https://api.canva.com/rest/v1/autofills"
    script = json.load(open(f"user_data/{project_id}/user_submitted_script.json", "r"))["editted_script"]
    graph_element = json.load(open(f"user_data/{project_id}/user_submitted_graph.json", "r"))
    #{"x_axis": "characters", "selected_columns": ["words"], "chart_type": "pie"}
    script = GenerateScriptResponse.model_validate(script)
    df = pd.read_csv(f"user_data/{project_id}/transformed_1.csv")
    modified_df = df[[graph_element["x_axis"]] + graph_element["selected_columns"]]
    modified_df.to_csv(f"user_data/{project_id}/modified_df.csv", index=False)
    chart_data = {}
    chart_data["rows"] = []
    chart_data["rows"].append({"cells": []})
    for column in modified_df.columns:
        chart_data["rows"][0]["cells"].append({"type": "string", "value": column})
    #iterate through the rows of the dataframe and add them to the chart data
    for index, row in modified_df.iterrows():
        chart_data["rows"].append({"cells": []})
        for i, column in enumerate(modified_df.columns):
            cell = row[column]
            if modified_df.dtypes[column] == "object":
                chart_data["rows"][-1]["cells"].append({"type": "string", "value": cell})
            else:
                chart_data["rows"][-1]["cells"].append({"type": "number", "value": cell})
    print(chart_data)
    if graph_element["chart_type"] == "pie":
        design_template_id = "DAGYNKM51_I"
    elif graph_element["chart_type"] == "bar":
        design_template_id = "DAGY0M6qBqY"
    elif graph_element["chart_type"] == "line":
        design_template_id = "DAGY0FMsx_c"
    payload = json.dumps({
    "brand_template_id": design_template_id,
    "data": {
        "hookText": {
        "type": "text",
        "text": script.screen_1.text
        },
        "problemText": {
        "type": "text",
        "text": script.screen_2.text
        },
        "insightText": {
        "type": "text",
        "text": script.screen_3.text
        },
        "tipBodyText": {
        "type": "text",
        "text": script.screen_4.text
        },
        "ctaText": {
        "type": "text",
        "text": script.screen_5.text
        },
        "chartData": {
        "type": "chart",
        "chart_data": chart_data
        }
    }
    }, cls=NumpyEncoder)
    with open("data/canva_tokens.json") as f:
        data = json.load(f)
    access_token = data["access_token"]
    headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json.dump(response.json(), open(f"user_data/{project_id}/design.json", "w"))
    return response.json()


def refresh_canva_token():
    with open("data/canva_tokens.json", "r") as f:
        data = json.load(f)
    headers = {
        "Authorization": f"Basic {CANVA_BASIC_AUTH}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
        "scope": "app:read app:write design:content:read design:meta:read design:content:write design:permission:read design:permission:write folder:read folder:write folder:permission:read folder:permission:write asset:read asset:write comment:read comment:write brandtemplate:meta:read brandtemplate:content:read profile:read"
    }

    response = requests.post("https://api.canva.com/rest/v1/oauth/token",
        headers=headers,
        data=data
    )
    print(response.json())
    with open("data/canva_tokens.json", "w") as f:
        json.dump(response.json(), f)
    return response.json()