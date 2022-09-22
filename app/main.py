import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile

import whisper

model = whisper.load_model("base")

app = FastAPI()



@app.post("/transcribe")
async def file(file: UploadFile = File(...)):
    file_name = os.getcwd() + "/app/uploads/" + file.filename.replace(" ", "-")
    with open(file_name, 'wb+') as f:
        f.write(file.file.read())
        f.close()
    result = model.transcribe(file_name)
    return {"filename": file.filename, "transcription": result["text"]}

app.mount("/", StaticFiles(directory="app/static", html = True), name="static")

