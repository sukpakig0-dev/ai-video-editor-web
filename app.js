const BACKEND = "https://ai-video-editor-web-3.onrender.com/video";

async function startProcess() {
  const file = document.getElementById("videoFile").files[0];
  const duration = document.getElementById("duration").value;

  if (!file) return alert("ভিডিও সিলেক্ট করো");

  setStatus("Uploading...");
  updateProgress(10);

  let formData = new FormData();
  formData.append("file", file);

  // Upload
  let res = await fetch(`${BACKEND}/upload`, { method: "POST", body: formData });
  let data = await res.json();

  setStatus("Processing...");
  updateProgress(40);

  // Process
  await fetch(`${BACKEND}/process?job_id=${data.job_id}&clip_duration=${duration}`, { method: "POST" });

  updateProgress(80);
  setStatus("Finalizing video...");

  const videoRes = await fetch(`${BACKEND}/download?job_id=${data.job_id}`);
  const videoData = await videoRes.json();

  const video = document.getElementById("resultVideo");
  video.src = videoData.video_url;
  video.load();

  const downloadBtn = document.getElementById("downloadBtn");
  downloadBtn.href = videoData.video_url;
  downloadBtn.style.display = "block";

  updateProgress(100);
  setStatus("✅ Done!");
}

function updateProgress(percent) {
  document.getElementById("progress").style.width = percent + "%";
}

function setStatus(text) {
  document.getElementById("status").innerText = text;
}
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
