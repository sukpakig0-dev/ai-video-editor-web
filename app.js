const BACKEND = "https://ai-video-editor-web-3.onrender.com/video";

async function startProcess() {
  const file = document.getElementById("videoFile").files[0];
  const duration = document.getElementById("duration").value;

  if (!file) {
    alert("ভিডিও সিলেক্ট করো");
    return;
  }

  setStatus("Uploading...");
  updateProgress(10);

  let formData = new FormData();
  formData.append("file", file);

  // Upload
  let res = await fetch(`${BACKEND}/upload`, {
    method: "POST",
    body: formData
  });
  let data = await res.json();

  setStatus("Processing (AI working)...");
  updateProgress(40);

  // Process
  await fetch(`${BACKEND}/process?job_id=${data.job_id}&clip_duration=${duration}`, {
    method: "POST"
  });

  updateProgress(80);
  setStatus("Finalizing video...");

  const videoUrl = `${BACKEND}/download?job_id=${data.job_id}`;

  const video = document.getElementById("resultVideo");
  video.src = videoUrl;
  video.load();

  const downloadBtn = document.getElementById("downloadBtn");
  downloadBtn.href = videoUrl;
  downloadBtn.style.display = "block";

  updateProgress(100);
  setStatus("✅ Done! Video ready");
}

function updateProgress(percent) {
  document.getElementById("progress").style.width = percent + "%";
}

function setStatus(text) {
  document.getElementById("status").innerText = text;
}
