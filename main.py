import os
import random
import requests
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips,
    AudioFileClip, vfx
)
from datetime import datetime

# NewsAPI
API_KEY = "YOUR_NEWSAPI_KEY"
URL = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={API_KEY}"

# إعداد مجلد الإخراج
os.makedirs("output", exist_ok=True)

# موسيقى الخلفية
music_folder = "music"
music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]
music_path = random.choice(music_files) if music_files else None

# شعار القناة
logo_path = "logo.png"

# ألوان النصوص
colors = ["white", "yellow", "cyan", "lime", "magenta"]

# جلب الأخبار
response = requests.get(URL)
articles = response.json().get("articles", [])
print(f"📰 Total articles fetched: {len(articles)}")
print(f"🎵 Using music: {music_path}")
print(f"📷 Logo exists: {os.path.exists(logo_path)}")

short_clips = []
long_clips = []

for idx, article in enumerate(articles, start=1):
    title = article.get("title", "No Title")
    image_url = article.get("urlToImage")

    image_path = f"temp_{idx}.jpg"
    if image_url:
        try:
            img_data = requests.get(image_url, timeout=10).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
        except:
            image_path = None

    color = random.choice(colors)
    txt_clip = TextClip(title, fontsize=40, color=color, size=(720,1280), method="caption").set_duration(5)
    txt_clip = txt_clip.crossfadein(0.5).crossfadeout(0.5)

    if image_path and os.path.exists(image_path):
        img_clip = ImageClip(image_path).set_duration(5).resize((720,1280)).fx(vfx.fadein,0.5).fx(vfx.fadeout,0.5)
    else:
        img_clip = TextClip("", fontsize=1, size=(720,1280), color="black").set_duration(5)

    if os.path.exists(logo_path):
        logo_clip = ImageClip(logo_path).set_duration(5).resize(width=100).set_position(("right","top"))
        video_clip = CompositeVideoClip([img_clip, txt_clip.set_position(("center","bottom")), logo_clip])
    else:
        video_clip = CompositeVideoClip([img_clip, txt_clip.set_position(("center","bottom"))])

    long_clips.append(video_clip)
    if idx <= 6:
        short_clips.append(video_clip)

audio_clip = AudioFileClip(music_path) if music_path else None
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Shorts
if short_clips:
    short_video = concatenate_videoclips(short_clips, method="compose")
    if audio_clip:
        short_video = short_video.set_audio(audio_clip.subclip(0, short_video.duration))
    short_output = f"output/usa_trends_shorts_{timestamp}.mp4"
    short_video.write_videofile(short_output, fps=24, codec="libx264")
    print(f"✅ Shorts video created: {short_output}")
    print(f"   - Duration: {short_video.duration:.2f} s")
    print(f"   - Articles: {len(short_clips)}")
    print(f"   - File size: {os.path.getsize(short_output)/1024/1024:.2f} MB")

# Long Video
if long_clips:
    long_video = concatenate_videoclips(long_clips, method="compose")
    if audio_clip:
        long_video = long_video.set_audio(audio_clip.subclip(0,long_video.duration))
    long_output = f"output/usa_trends_long_{timestamp}.mp4"
    long_video.write_videofile(long_output, fps=24, codec="libx264")
    print(f"✅ Long video created: {long_output}")
    print(f"   - Duration: {long_video.duration:.2f} s")
    print(f"   - Articles: {len(long_clips)}")
    print(f"   - File size: {os.path.getsize(long_output)/1024/1024:.2f} MB")
