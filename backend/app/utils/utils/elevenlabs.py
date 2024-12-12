from settings import NOELLA_VOICE_ID, TARUN_VOICE_ID, ELEVEN_LABS_VOICE_ID, ELEVEN_LABS_MODEL, ELEVEN_LABS_API_KEY, KIRAN_VOICE_ID, SHIVANI_VOICE_ID
from elevenlabs import ElevenLabs, VoiceSettings

eleven_labs_client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

def generate_audio_for_script(script: str, file_path: str, prev_text: str = "", next_text: str = ""):
    audio = eleven_labs_client.text_to_speech.convert(voice_id=NOELLA_VOICE_ID, model_id=ELEVEN_LABS_MODEL, 
                                                      text=script, previous_text=prev_text, next_text=next_text,
                                                      voice_settings=VoiceSettings(stability=0.56, similarity_boost=0.6,
                                                        style=0.5, use_speaker_boost=True))
    with open(file_path, "wb") as file:
        for chunk in audio:
            if chunk:
                file.write(chunk)
    return