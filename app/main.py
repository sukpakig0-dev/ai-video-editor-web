from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = {}

@app.get("/")
def root():
    return {"status": "Backend is running"}

# Upload API
@app.post("/video/upload")
async def upload_video(file: UploadFile):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"filename": file.filename, "status": "uploaded"}
    # Dummy storage, file not really saved
    return {"job_id": job_id}

# Process API
@app.post("/video/process")
async def process_video(job_id: str, clip_duration: int = 30):
    if job_id in jobs:
        jobs[job_id]["status"] = "processed"
        jobs[job_id]["clip_duration"] = clip_duration
    return {"status": "done"}

# Download API
@app.get("/video/download")
async def download_video(job_id: str):
    if job_id in jobs:
        # dummy video url (placeholder)
        return {"video_url": "https://www.w3schools.com/html/mov_bbb.mp4"}
    return {"error": "job not found"}
