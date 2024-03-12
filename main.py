import os
from dotenv import load_dotenv
import requests
import json
import azure.cognitiveservices.speech as speech_sdk
load_dotenv("env/.env")
api_key = os.getenv('OPENAI_API_KEY')
ai_key = os.getenv('SPEECH_KEY')
ai_region = os.getenv('SPEECH_REGION')

def main():
    try:
        global speech_config
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        command = TranscribeCommand()
        gpt_response = call_gpt(command)
        SynthesizeSpeech(gpt_response)
        
    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ""
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print("Listening...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech_recognition_result.text
        return command
    else:
        print(speech_recognition_result.reason)
        if speech_recognition_result.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech_recognition_result.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
        raise Exception("Speech recognition failed")



def call_gpt(message):
    # Define the headers and data for HTTP request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        "model": "gpt-4-0125-preview",
        "messages": [{"role": "user", "content": message},
        {"role": "system", "content": "You are a voice assistant who responds to user voice input. Formulate your answers for voice responses, be concise but friendly. Try to keep your responses under 30 seconds."}],
        "temperature": 0.7,
        "max_tokens": 256
    }

    # Make the HTTP request 
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

    # Get the response JSON
    response_json = response.json()
    assistant_message = response_json['choices'][0]['message']['content']
    return assistant_message

def SynthesizeSpeech(message):
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    result = speech_synthesizer.speak_text_async(message).get()
    if result.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        raise Exception("Speech synthesis failed: {}".format(result.error_details))
    return result

if __name__ == "__main__":
    main()