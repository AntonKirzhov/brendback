#from openai import OpenAI

#client = OpenAI(api_key="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")
gigachat_token = ""
expire_time = 0
import speech_recognition as sr
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import aiomysql
import asyncio
import shutil
import uuid
import os
import time
import requests
import datetime
import librosa
import json
import argparse
import os
import json
import random
import cv2
import numpy as np
from matplotlib import cm
from scipy.io import wavfile
from imageai.Classification import ImageClassification
from stable_diffusion_engine import StableDiffusionEngine
from diffusers import LMSDiscreteScheduler, PNDMScheduler
from openvino.runtime import Core
from gtts import gTTS
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from transformers import MarianMTModel, MarianTokenizer
from typing import Sequence

connection = None
cursor = None
app = FastAPI()
r = sr.Recognizer()
scheduler = PNDMScheduler(
    beta_start=0.00085,
    beta_end=0.012,
    beta_schedule="scaled_linear",
    skip_prk_steps = True,
    tensor_format="np"
)
engine = StableDiffusionEngine(
    model="bes-dev/stable-diffusion-v1-4-openvino",
    scheduler=scheduler,
    tokenizer="openai/clip-vit-large-patch14",
    device="CPU"
)
scale_intervals = ['A','a','B','C','c','D','d','E','F','f','G','g']
scales = ['AEOLIAN', 'BLUES', 'PHYRIGIAN', 'CHROMATIC', 'DORIAN', 'HARMONIC_MINOR', 'LYDIAN', 'MAJOR', 'MELODIC_MINOR', 'MINOR', 'MIXOLYDIAN', 'NATURAL_MINOR', 'PENTATONIC']
execution_path = os.getcwd()
prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth"))
prediction.loadModel()

class Translator:
    def __init__(self, source_lang: str, dest_lang: str) -> None:
        self.model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{dest_lang}'
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        
    def translate(self, texts: Sequence[str]) -> Sequence[str]:
        tokens = self.tokenizer(list(texts), return_tensors="pt", padding=True)
        translate_tokens = self.model.generate(**tokens)
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translate_tokens]

translator = Translator('ru', 'en')

async def check_gigachat_token():
    global gigachat_token
    global expire_time
    if int(time.time()) > expire_time:
        response = requests.request("POST", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth", headers={'Content-Type': 'application/x-www-form-urlencoded','RqUID': str(uuid.uuid4()),'Authorization': "Bearer NzRjZWFjY2YtNGUzNS00YjhmLWJlZjktNDg5ZGNhMjM1MTYzOjQyODZlOThlLTc1NWYtNDVkMy1hOWY2LTBjM2Q4NzE4NGRhOA=="}, data={'scope':"GIGACHAT_API_PERS"})
        if len(response.text) > 5:
            answer = json.loads(response.text)
            gigachat_token = answer['access_token']
            expire_time = int(answer['expires_at'])/1000

            print(gigachat_token)
            print(expire_time)

async def get_piano_notes():   
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs

async def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave

async def makeScale(whichOctave, whichKey, whichScale):
    note_freqs = await get_piano_notes()
    index = scale_intervals.index(whichKey)
    new_scale = scale_intervals[index:12] + scale_intervals[:index]
    if whichScale == 'AEOLIAN':
        scale = [0, 2, 3, 5, 7, 8, 10]
    elif whichScale == 'BLUES':
        scale = [0, 2, 3, 4, 5, 7, 9, 10, 11]
    elif whichScale == 'PHYRIGIAN':
        scale = [0, 1, 3, 5, 7, 8, 10]
    elif whichScale == 'CHROMATIC':
        scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    elif whichScale == 'DORIAN':
        scale = [0, 2, 3, 5, 7, 9, 10]
    elif whichScale == 'HARMONIC_MINOR':
        scale = [0, 2, 3, 5, 7, 8, 11]
    elif whichScale == 'LYDIAN':
        scale = [0, 2, 4, 6, 7, 9, 11]
    elif whichScale == 'MAJOR':
        scale = [0, 2, 4, 5, 7, 9, 11]
    elif whichScale == 'MELODIC_MINOR':
        scale = [0, 2, 3, 5, 7, 8, 9, 10, 11]
    elif whichScale == 'MINOR':    
        scale = [0, 2, 3, 5, 7, 8, 10]
    elif whichScale == 'MIXOLYDIAN':     
        scale = [0, 2, 4, 5, 7, 9, 10]
    elif whichScale == 'NATURAL_MINOR':   
        scale = [0, 2, 3, 5, 7, 8, 10]
    elif whichScale == 'PENTATONIC':    
        scale = [0, 2, 4, 7, 9]
    else:
        print('Invalid scale name')
    
    freqs = []
    for i in range(len(scale)):
        note = new_scale[scale[i]] + str(whichOctave)
        freqToAdd = note_freqs[note]
        freqs.append(freqToAdd)
    return freqs

def hue2freq(h,scale_freqs):
    thresholds = [26 , 52 , 78 , 104,  128 , 154 , 180]
    if (h <= thresholds[0]):
         note = scale_freqs[0]
    elif (h > thresholds[0]) & (h <= thresholds[1]):
        note = scale_freqs[1]
    elif (h > thresholds[1]) & (h <= thresholds[2]):
        note = scale_freqs[2]
    elif (h > thresholds[2]) & (h <= thresholds[3]):
        note = scale_freqs[3]
    elif (h > thresholds[3]) & (h <= thresholds[4]):    
        note = scale_freqs[4]
    elif (h > thresholds[4]) & (h <= thresholds[5]):
        note = scale_freqs[5]
    elif (h > thresholds[5]) & (h <= thresholds[6]):
        note = scale_freqs[6]
    else:
        note = scale_freqs[0]
    
    return note

async def img2music(img, scale = [220.00, 246.94 ,261.63, 293.66, 329.63, 349.23, 415.30],
              sr = 22050, T = 0.1, nPixels = 60, useOctaves = True, randomPixels = False,
              harmonize = 'U0'):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    height, width, depth = img.shape

    i=0 ; j=0 ; k=0
    hues = [] 
    if randomPixels == False:
        for val in range(nPixels):
                hue = abs(hsv[i][j][0])
                hues.append(hue)
                i+=1
                j+=1
    else:
        for val in range(nPixels):
            i = random.randint(0, height-1)
            j = random.randint(0, width-1)
            hue = abs(hsv[i][j][0])
            hues.append(hue)
             
    pixels_df = pd.DataFrame(hues, columns=['hues'])
    pixels_df['frequencies'] = pixels_df.apply(lambda row : hue2freq(row['hues'],scale), axis = 1) 
    frequencies = pixels_df['frequencies'].to_numpy()
    
    pixels_df['notes'] = pixels_df.apply(lambda row : librosa.hz_to_note(row['frequencies']), axis = 1)  
    
    pixels_df['midi_number'] = pixels_df.apply(lambda row : librosa.note_to_midi(row['notes']), axis = 1)  
    harmony_select = {'U0' : 1,
                      'ST' : 16/15,
                      'M2' : 9/8,
                      'm3' : 6/5,
                      'M3' : 5/4,
                      'P4' : 4/3,
                      'DT' : 45/32,
                      'P5' : 3/2,
                      'm6': 8/5,
                      'M6': 5/3,
                      'm7': 9/5,
                      'M7': 15/8,
                      'O8': 2
                     }
    harmony = np.array([])
    harmony_val = harmony_select[harmonize]  
    #song_freqs = np.array([]) #This array will contain the chosen frequencies used in our song :]
    song = np.array([])       #This array will contain the song signal
    octaves = np.array([0.5,1,2])#Go an octave below, same note, or go an octave above
    t = np.linspace(0, T, int(T*sr), endpoint=False) # time variable
    #Make a song with numpy array :]
    #nPixels = int(len(frequencies))#All pixels in image
    for k in range(nPixels):
        if useOctaves:
            octave = random.choice(octaves)
        else:
            octave = 1
        
        if randomPixels == False:
            val =  octave * frequencies[k]
        else:
            val = octave * random.choice(frequencies)
            
        #Make note and harmony note    
        note   = 0.5*np.sin(2*np.pi*val*t)
        h_note = 0.5*np.sin(2*np.pi*harmony_val*val*t)  
        
        #Place notes into corresponfing arrays
        song       = np.concatenate([song, note])
        harmony    = np.concatenate([harmony, h_note])                                     
        #song_freqs = np.concatenate([song_freqs, val])
                                               
    return song, pixels_df, harmony

@app.on_event("startup")
async def on_startup():
    global connection
    global cursor
    connection = await aiomysql.connect(host="localhost", port=3306, user="root", password="root", db="startsback", autocommit=True)
    cursor = await connection.cursor(aiomysql.DictCursor)
    await cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")
    print("Connected successfully!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://193.27.228.18", "http://193.27.228.19",
                   "http://193.27.228.20", "http://dev.brendboost.ru", "http://brendboost.ru",
                   "https://dev.brendboost.ru", "https://brendboost.ru", '*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello!"}

async def get_user_by_id(user_id: str):
    await connection.ping()
    query = await cursor.execute(f"SELECT `_id`, `selected_company` FROM `users` WHERE `_id` = '{user_id}'")
    result = await cursor.fetchall()
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=409, detail="Invalid user.")

@app.get("/make_request")
async def make_request(user_id: str = "", request_text: str = ""):
    await connection.ping()
    user = await get_user_by_id(user_id)
    await cursor.execute(f"SELECT * FROM `messages` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
    sql_messages = await cursor.fetchall()

    messages = []
    for message in sql_messages:
        messages.append({"role": message['role'], "content": message['content']})

    await check_gigachat_token()
    messages.append({"role": "user", "content": request_text})
    payload = json.dumps({
      "model": "GigaChat",
      "messages": messages,
      "temperature": 1,
      "top_p": 0.1,
      "n": 1,
      "stream": False,
      "max_tokens": 512,
      "repetition_penalty": 1,
      "update_interval": 0
    })
    response = requests.request("POST", "https://gigachat.devices.sberbank.ru/api/v1/chat/completions", headers={'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {gigachat_token}'}, data=payload)
    reply = json.loads(response.text)['choices'][0]['message']['content']
    t = json.loads(response.text)
    await cursor.execute(f"INSERT INTO `messages` (`user_id`, `content`, `role`, `company`) VALUES ('{user_id}', '{request_text}', 'user', '{user['selected_company']}'), ('{user_id}', '{reply}', 'assistant', '{user['selected_company']}')")
    await connection.commit()
    return {"message": reply}

@app.get("/clear_history")
async def clear_history(user_id: str = ""):
    await connection.ping()
    user = await get_user_by_id(user_id)
    await cursor.execute(f"DELETE FROM `messages` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
    await connection.commit()
    return {"status": True}

@app.get("/get_requests_history")
async def get_requests_history(user_id: str = ""):
    await connection.ping()
    user = await get_user_by_id(user_id)
    await cursor.execute(f"SELECT * FROM `messages` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
    messages = await cursor.fetchall()
    return {"messages": messages}

@app.get("/image_generate")
async def image_generate(request_text: str = ""):
    filename = int(time.time())
    parser = argparse.ArgumentParser()
    text = translator.translate([request_text])
    text = text[0]
    print(text)
    parser.add_argument("--seed", type=int, default=random.randint(0, 2**30), help="random seed for generating consistent images per prompt")
    parser.add_argument("--num-inference-steps", type=int, default=12, help="num inference steps")
    parser.add_argument("--guidance-scale", type=float, default=7.5, help="guidance scale")
    parser.add_argument("--eta", type=float, default=0.0, help="eta")
    parser.add_argument("--prompt", type=str, default=text, help="prompt")
    parser.add_argument("--params-from", type=str, required=False, help="Extract parameters from a previously generated image.")
    parser.add_argument("--init-image", type=str, default=None, help="path to initial image")
    parser.add_argument("--strength", type=float, default=0.5, help="how strong the initial image should be noised [0.0, 1.0]")
    parser.add_argument("--mask", type=str, default=None, help="mask of the region to inpaint on the initial image")
    parser.add_argument("--output", type=str, default=f"{filename}.png", help="output image name")
    args = parser.parse_args()
    np.random.seed(args.seed)
    image = engine(
        prompt=args.prompt,
        init_image=None if args.init_image is None else cv2.imread(args.init_image),
        mask=None if args.mask is None else cv2.imread(args.mask, 0),
        strength=args.strength,
        num_inference_steps=args.num_inference_steps,
        guidance_scale=args.guidance_scale,
        eta=args.eta
    )
    cv2.imwrite(args.output, image)
    
    return FileResponse(path=f"{filename}.png", filename=f"{filename}.png", media_type='multipart/form-data')#{"url": image_id}

@app.get("/audio_create")
async def audio_create(text: str = "", language: str = ""):
    filename = int(time.time())
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(f"{filename}.mp3")

    return FileResponse(path=f"{filename}.mp3", filename=f"{filename}.mp3", media_type='multipart/form-data')

@app.post("/audio_translate")
async def audio_translate(file: UploadFile):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    transcript = None
    with sr.AudioFile(file.filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        transcript = text
    os.remove(file.filename)
    return transcript

@app.post("/describe_image")
async def describe_image(file: UploadFile):
    filename = f"{int(time.time())}.jpg"
    try:
        contents = file.file.read()
        with open(filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"describe": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, filename), result_count=5)
    description = ""
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        decribe = f"{eachPrediction} : {eachProbability}%"
        description = f"{description}\n{decribe}"

    os.remove(filename)
    return {"describe": description}

@app.post("/generate_music")
async def generate_music(file: UploadFile, octave: str, key: str, scale: str):
    filename = f"{int(time.time())}.jpg"
    try:
        contents = file.file.read()
        with open(filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    input_file = cv2.imread(filename)
    os.remove(filename)

    file_scale = await makeScale(int(octave), key, scale)
    file_song, file_df, file_song_harmony  = await img2music(input_file, 
                                                        file_scale, 
                                                        T = 0.3,
                                                        randomPixels = True, 
                                                        useOctaves = True)
    filename = '{date:%Y-%m-%d_%H.%M.%S}.wav'.format(date=datetime.datetime.now())
    wavfile.write(filename, rate = 22050, data = file_song.astype(np.float32))
    return FileResponse(path=filename, filename=filename, media_type='multipart/form-data')

@app.get("/generate_post")
async def generate_post(media: str = "", post_description: str = ""):

    await check_gigachat_token()
    chat_log = [
        {"role": "system", "content": f"Ты профессиональный редактор и копирайтер для {media}."},
        {"role": "user", "content": f"Сгенерируй текст для поста по описанию: {post_description}."},
    ]
    payload = json.dumps({
      "model": "GigaChat",
      "messages": chat_log,
      "temperature": 1,
      "top_p": 0.1,
      "n": 1,
      "stream": False,
      "max_tokens": 512,
      "repetition_penalty": 1,
      "update_interval": 0
    })
    response = requests.request("POST", "https://gigachat.devices.sberbank.ru/api/v1/chat/completions", headers={'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {gigachat_token}'}, data=payload)
    reply = json.loads(response.text)['choices'][0]['message']['content']

    #response = client.chat.completions.create(model="gpt-3.5-turbo",messages=chat_log)

    #description = response.choices[0].message.content

    return {"post": reply}