import os
import urllib.request
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# إنشاء المجلدات
os.makedirs("videos", exist_ok=True)
os.makedirs("music", exist_ok=True)
os.makedirs("output", exist_ok=True)

# تحميل ملفات تجريبية إذا كانت المجلدات فارغة
def download_assets():
    v_url = "https://github.com/selimb/mini-video/raw/main/video1.mp4"
    m_url = "https://github.com/selimb/mini-video/raw/main/music.mp3"
    if not os.listdir("videos"):
        print("Downloading sample video...")
        urllib.request.urlretrieve(v_url, "videos/video1.mp4")
    if not os.listdir("music"):
        print("Downloading sample music...")
        urllib.request.urlretrieve(m_url, "music/sample.mp3")

download_assets()

# معالجة الفيديو
video_files = [os.path.join("videos", f) for f in os.listdir("videos") if f.endswith(".mp4")]
clips = [VideoFileClip(f).resize(width=720) for f in video_files]
final_video = concatenate_videoclips(clips, method="compose")

# إضافة الصوت
music_files = [os.path.join("music", f) for f in os.listdir("music") if f.endswith(".mp3")]
if music_files:
    audio = AudioFileClip(music_files[0]).set_duration(final_video.duration)
    final_video = final_video.set_audio(audio)

# حفظ النتيجة
output_path = f"output/final_video_{datetime.now().strftime('%Y%m%d')}.mp4"
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
print(f"✅ Success! Saved to {output_path}")
