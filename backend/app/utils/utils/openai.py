from openai import OpenAI
from schemas.core import GenerateCodeResponse, GenerateQuestionsResponse, GenerateScriptForTranscriptResponse, GenerateScriptResponse, GraphType, PickGraphTypeResponse, PreliminaryAnalyseResponse
from settings import GENERATE_CODE_SYSTEM_PROMPT, GENERATE_CODE_USER_PROMPT, GENERATE_QUESTIONS_SYSTEM_PROMPT, GENERATE_QUESTIONS_USER_PROMPT, OPENAI_GPT4_O_MODEL, PICK_GRAPH_TYPE_SYSTEM_PROMPT, PICK_GRAPH_TYPE_USER_PROMPT, PRELIMINARY_ANALYSE_SYSTEM_PROMPT, PRELIMINARY_ANALYSE_USER_PROMPT, SCRIPT_GENERATION_SYSTEM_PROMPT, SCRIPT_GENERATION_TEMPLATE, SCRIPT_SYSTEM_PROMPT, SCRIPT_USER_PROMPT
import pandas as pd
import json

client = OpenAI()

def preliminary_analyse(file_path: str) -> PreliminaryAnalyseResponse:
    df = pd.read_csv(file_path)
    data_summary = df.head().to_string()
    data_description = df.describe().to_string()
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=PreliminaryAnalyseResponse,
        messages=[
            {"role": "system", "content": PRELIMINARY_ANALYSE_SYSTEM_PROMPT},
            {"role": "user", "content": PRELIMINARY_ANALYSE_USER_PROMPT.format(data_summary, data_description)},
        ],
    )
    return PreliminaryAnalyseResponse.parse_obj(json.loads(completion.choices[0].message.content))

def generate_questions(domain: str, columns: list[str], file_path: str) -> GenerateQuestionsResponse:
    df = pd.read_csv(file_path)
    data_description = df.describe().to_string()
    data_summary = df.head().to_string()
    print(data_description)
    print(data_summary)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateQuestionsResponse,
        messages=[
            {"role": "system", "content": GENERATE_QUESTIONS_SYSTEM_PROMPT},
            {"role": "user", "content": GENERATE_QUESTIONS_USER_PROMPT.format(domain, ",".join(columns), data_description, data_summary)},
        ],
    )
    return GenerateQuestionsResponse.parse_obj(json.loads(completion.choices[0].message.content))


def generate_code(domain: str, columns: list[str], question: str, 
                  file_path: str, output_file_path: str, output_data_file_path: str) -> GenerateCodeResponse:
    print(domain, columns, question, file_path, output_file_path, output_data_file_path)
    df = pd.read_csv(file_path)
    data_description = df.describe().to_string()
    data_sample = df.head().to_string()
    user_prompt = GENERATE_CODE_USER_PROMPT.format(domain=domain, 
                                                   columns=", ".join(columns), 
                                                   question=question, 
                                                   data_description=data_description, 
                                                   data_sample=data_sample,
                                                   output_path=output_data_file_path,
                                                   input_path=file_path)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateCodeResponse,
        messages=[
            {"role": "system", "content": GENERATE_CODE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    code_response = GenerateCodeResponse.parse_obj(json.loads(completion.choices[0].message.content))
    print(code_response)
    with open(output_file_path, "w") as f:
        f.write(code_response.code)
    return code_response

def pick_graph_type(question: str, file_path: str) -> PickGraphTypeResponse:
    df = pd.read_csv(file_path)
    #format df into a string
    data_description = df.to_string()
    chart_types = "\n".join([chart_type.value for chart_type in GraphType])
    user_prompt = PICK_GRAPH_TYPE_USER_PROMPT.format(question=question, \
                                                      data=data_description, \
                                                      chart_types=chart_types)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=PickGraphTypeResponse,
        messages=[
            {"role": "system", "content": PICK_GRAPH_TYPE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return PickGraphTypeResponse.parse_obj(json.loads(completion.choices[0].message.content))

# def extract_csv_from_text(text: str, project_id: str):
#     with open(f"user_data/{project_id}/raw.txt", "w") as file:
#         file.write(text)
#     completion = client.beta.chat.completions.parse(
#         model=OPENAI_GPT4_O_MODEL,
#         response_format=ExtractCSVFromTextResponse,
#         messages=[
#             {"role": "system", "content": EXTRACT_CSV_FROM_TEXT_SYSTEM_PROMPT},
#             {"role": "user", "content": text},
#         ],
#     )
#     ret = ExtractCSVFromTextResponse.parse_obj(json.loads(completion.choices[0].message.content))
#     with open(f"user_data/{project_id}/raw.csv", "w") as file:
#         file.write(ret.csv)
#     return ret




def generate_script(project_id: str, question: str, domain: str):
    topic = domain + ": " + question
    with open(f"user_data/{project_id}/transformed_1.csv", "r") as f:
        chart_data = f.read()
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateScriptResponse,
        messages=[
            {"role": "system", "content": SCRIPT_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": SCRIPT_GENERATION_TEMPLATE.format(topic=topic, chart_data=chart_data)},
        ],
    )
    ret = GenerateScriptResponse.parse_obj(json.loads(completion.choices[0].message.content))
    return ret


def generate_script_for_transcript(transcript: dict):
    script = ""
    added_segments = []
    for segment in transcript["segments"]:
        if segment["text"] == "":
            continue
        added_segments.append(segment["start"])
        script += f"[{segment['start']}-{segment['end']}] {segment['text']}\n"
    print(script)
    completion = client.beta.chat.completions.parse(
        model=OPENAI_GPT4_O_MODEL,
        response_format=GenerateScriptForTranscriptResponse,
        messages=[
            {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
            {"role": "user", "content": SCRIPT_USER_PROMPT.format(script=script)},
        ],
    )
    print(completion.choices[0].message.content)
    ret = GenerateScriptForTranscriptResponse.parse_obj(json.loads(completion.choices[0].message.content))
    for el in ret.script_for_timestamp:
        if int(el.start_time) in added_segments:
            el.text = transcript["segments"][int(el.start_time)//5]["text"]
    return ret