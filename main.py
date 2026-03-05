import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx

# إعداد المجلدات
os.makedirs("videos", exist_ok=True)
os.makedirs("music", exist_ok=True)
os.makedirs("output", exist_ok=True)

# تحميل ملفات تجريبية إذا لم تكن موجودة (لضمان عدم فشل السكربت)
import urllib.request
if not os.listdir("videos"):
    print("Downloading sample video...")
    urllib.request.urlretrieve("https://github.com/selimb/mini-video/raw/main/video1.mp4", "videos/video1.mp4")
if not os.listdir("music"):
    print("Downloading sample music...")
    urllib.request.urlretrieve("https://github.com/selimb/mini-video/raw/main/music.mp3", "music/sample.mp3")

video_files = [os.path.join("videos", f) for f in os.listdir("videos") if f.endswith(".mp4")]
today = datetime.now().strftime("%Y-%m-%d")

print(f"Processing {len(video_files)} videos...")

clips = [VideoFileClip(f).resize(width=720) for f in video_files]
final_video = concatenate_videoclips(clips, method="compose")

# إضافة الصوت
music_files = [os.path.join("music", f) for f in os.listdir("music") if f.endswith(".mp3")]
if music_files:
    audio = AudioFileClip(music_files[0]).set_duration(final_video.duration)
    final_video = final_video.set_audio(audio)

# حفظ النتيجة
output_path = f"output/usa_trends_{today}.mp4"
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

print(f"✅ Video created: {output_path}")
