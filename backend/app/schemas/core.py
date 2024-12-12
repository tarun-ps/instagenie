from enum import Enum
from pydantic import BaseModel

class GraphType(Enum):
    LINE = "line"
    HORIZONTAL_LINE = "horizontal_line"
    STACKED_LINE = "stacked_line"
    BAR = "bar"
    STACKED_BAR = "stacked_bar"
    HORIZONTAL_BAR = "horizontal_bar"
    PIE = "pie"
    DONUT = "donut"

class PreliminaryAnalyseResponse(BaseModel):
    domain: str
    columns: list[str]
    def to_dict(self):
        return self.model_dump()

class GenerateQuestionsResponse(BaseModel):
    questions: list[str]
    def to_dict(self):
        return self.model_dump()

class PickGraphTypeResponse(BaseModel):
    graph_type: GraphType
    reason: str
    def to_dict(self):
        return self.model_dump()

class GenerateCodeResponse(BaseModel):
    code: str
    def to_dict(self):
        return self.model_dump()
    
class ExtractCSVFromTextResponse(BaseModel):
    csv: str
    title: str
    
class Screen1Response(BaseModel):
    text: str
    voice_over: str
    #visual: str

class Screen2Response(BaseModel):
    text: str
    voice_over: str
   # visual: str

class Screen3Response(BaseModel):
    text: str
    visual: str
    voice_over: str
class Screen4Response(BaseModel):
    text: str
    voice_over: str
    #visual: str

class Screen5Response(BaseModel):
    text: str
    cta: str
    voice_over: str
    #visual: str

class GenerateScriptResponse(BaseModel):
    screen_1: Screen1Response
    screen_2: Screen2Response
    screen_3: Screen3Response
    screen_4: Screen4Response
    screen_5: Screen5Response
    def to_dict(self):
        return self.model_dump()

class ScriptForTimestamp(BaseModel):
    start_time: int
    end_time: int
    b_roll: str
    stock_imagery_search_queries: list[str]
    stock_video_search_queries: list[str]
    lottie_animations: list[str]
    lists: list[str]
    statistics: list[str]
    locations: list[str]
    emphasized_text: str
    text: str
    def to_dict(self):
        return self.model_dump()
    

class GenerateScriptForTranscriptResponse(BaseModel):
    script_for_timestamp: list[ScriptForTimestamp]
    def to_dict(self):
        return self.model_dump()
