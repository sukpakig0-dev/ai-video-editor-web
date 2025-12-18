from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid, os, shutil
import subprocess
import whisper

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

jobs = {}
model = whisper.load_model("base")  # Whisper model for transcription

@app.get("/")
def root():
    return {"status": "Backend is running"}

# Upload API
@app.post("/video/upload")
async def upload_video(file: UploadFile):
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    jobs[job_id] = {"input": file_path, "status": "uploaded"}
    return {"job_id": job_id}

# Process API
@app.post("/video/process")
async def process_video(job_id: str, clip_duration: int = Form(...)):
    if job_id not in jobs:
        return {"error": "Job not found"}

    input_file = jobs[job_id]["input"]
    output_file = os.path.join(OUTPUT_DIR, f"{job_id}_short.mp4")
    
    # Use FFmpeg to cut first `clip_duration` seconds (simple version)
    cmd = [
        "ffmpeg", "-i", input_file,
        "-t", str(clip_duration),
        "-vf", "scale=720:1280",  # vertical 9:16
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-y", output_file
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Whisper for Bangla subtitles
    result = model.transcribe(input_file, language="bn")  # Auto detect Bangla
    subtitle_file = os.path.join(OUTPUT_DIR, f"{job_id}.srt")
    with open(subtitle_file, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"]):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"]
            f.write(f"{i+1}\n")
            f.write(f"{start:.3f} --> {end:.3f}\n")
            f.write(text + "\n\n")

    jobs[job_id]["status"] = "processed"
    jobs[job_id]["output"] = output_file
    jobs[job_id]["subtitle"] = subtitle_file
    return {"status": "done"}

# Download API
@app.get("/video/download")
async def download_video(job_id: str):
    if job_id in jobs and "output" in jobs[job_id]:
        return FileResponse(jobs[job_id]["output"], media_type="video/mp4", filename=f"short_{job_id}.mp4")
    return {"error": "job not ready"}# Download API
@app.get("/video/download")
async def download_video(job_id: str):
    if job_id in jobs:
        # dummy video url (placeholder)
        return {"video_url": "https://www.w3schools.com/html/mov_bbb.mp4"}
    return {"error": "job not found"}
