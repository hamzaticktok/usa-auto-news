import os
import urllib.request
import zipfile

# ===============================
# إعداد المجلدات والملفات
# ===============================
repo_name = "usa-auto-news"
videos = {
    "video1.mp4": "https://github.com/selimb/mini-video/raw/main/video1.mp4",
    "video2.mp4": "https://github.com/selimb/mini-video/raw/main/video2.mp4"
}
music = {
    "sample.mp3": "https://github.com/selimb/mini-video/raw/main/music.mp3"
}
workflow_content = """name: Build Videos

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install moviepy imageio[ffmpeg]
    - name: Install FFmpeg
      run: sudo apt-get update && sudo apt-get install -y ffmpeg
    - name: Ensure folders
      run: |
        mkdir -p videos
        mkdir -p music
        mkdir -p output
    - name: Run script
      run: python3 your_script.py
    - name: Upload Artifacts
      uses: actions/upload-artifact@v4
      with:
        name: videos
        path: output/
"""

script_content = """import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx

video_folder = "videos"
music_folder = "music"
output_folder = "output"
today = datetime.now().strftime("%Y-%m-%d")
short_max_duration = 60

os.makedirs(output_folder, exist_ok=True)

video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")]
if not video_files:
    print("❌ No video files found in 'videos/' folder.")
    exit(1)

clips = []
for file in video_files:
    clip = VideoFileClip(file).resize(width=720)
    clips.append(clip)
final_long = concatenate_videoclips(clips, method="compose")

music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]
if music_files:
    audio = AudioFileClip(random.choice(music_files))
    if audio.duration < final_long.duration:
        audio = afx.audio_loop(audio, duration=final_long.duration)
    else:
        audio = audio.subclip(0, final_long.duration)
    final_long = final_long.set_audio(audio)

long_path = os.path.join(output_folder, f"usa_trends_long_{today}.mp4")
final_long.write_videofile(long_path, codec="libx264", audio_codec="aac", fps=24)

short_duration = min(short_max_duration, final_long.duration)
final_short = final_long.subclip(0, short_duration)
short_path = os.path.join(output_folder, f"usa_trends_shorts_{today}.mp4")
final_short.write_videofile(short_path, codec="libx264", audio_codec="aac", fps=24)

for clip in clips:
    clip.close()
final_long.close()
final_short.close()
if music_files:
    audio.close()
"""

# ===============================
# إنشاء المجلدات مؤقتًا
# ===============================
os.makedirs(f"{repo_name}/videos", exist_ok=True)
os.makedirs(f"{repo_name}/music", exist_ok=True)
os.makedirs(f"{repo_name}/.github/workflows", exist_ok=True)

# ===============================
# تحميل الفيديوهات والموسيقى
# ===============================
for name, url in videos.items():
    print(f"Downloading {name}...")
    urllib.request.urlretrieve(url, f"{repo_name}/videos/{name}")

for name, url in music.items():
    print(f"Downloading {name}...")
    urllib.request.urlretrieve(url, f"{repo_name}/music/{name}")

# ===============================
# إنشاء السكربت وworkflow
# ===============================
with open(f"{repo_name}/your_script.py", "w") as f:
    f.write(script_content)

with open(f"{repo_name}/.github/workflows/build_videos.yml", "w") as f:
    f.write(workflow_content)

# ===============================
# إنشاء ملف ZIP
# ===============================
zip_name = f"{repo_name}.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_name):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, repo_name))

print(f"✅ ZIP created: {zip_name}")
