import os
import requests
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from datetime import datetime

# ===== إعداد NewsAPI =====
API_KEY = "YOUR_NEWSAPI_KEY"
URL = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={API_KEY}"

# مجلد الإخراج
os.makedirs("output", exist_ok=True)

# مسار ملف الموسيقى (يمكنك وضع mp3 في المشروع)
music_path = "background.mp3"  # ضع ملف الموسيقى هنا
logo_path = "logo.png"          # ضع شعار قناتك هنا (شفاف أفضل)

# جلب الأخبار
response = requests.get(URL)
articles = response.json().get("articles", [])

short_clips = []   # فيديوهات قصيرة
long_clips = []    # فيديو طويل

for idx, article in enumerate(articles, start=1):
    title = article.get("title", "No Title")
    image_url = article.get("urlToImage")

    # تنزيل الصورة
    image_path = f"temp_{idx}.jpg"
    if image_url:
        try:
            img_data = requests.get(image_url, timeout=10).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
        except:
            image_path = None

    # إعداد النص
    txt_clip = TextClip(title, fontsize=40, color='white', size=(720, 1280), method="caption").set_duration(5)

    # إعداد الصورة أو خلفية سوداء
    if image_path and os.path.exists(image_path):
        img_clip = ImageClip(image_path).set_duration(5).resize((720,1280))
    else:
        img_clip = TextClip("", fontsize=1, size=(720,1280), color="black").set_duration(5)

    # إضافة شعار القناة في الزاوية العليا اليمنى
    if os.path.exists(logo_path):
        logo_clip = ImageClip(logo_path).set_duration(5).resize(width=100).set_position(("right","top"))
        video_clip = CompositeVideoClip([img_clip, txt_clip.set_position(("center","bottom")), logo_clip])
    else:
        video_clip = CompositeVideoClip([img_clip, txt_clip.set_position(("center","bottom"))])

    long_clips.append(video_clip)
    if idx <= 6:  # أول 6 أخبار لفيديو Shorts
        short_clips.append(video_clip)

# ---- إضافة الموسيقى ----
audio_clip = AudioFileClip(music_path) if os.path.exists(music_path) else None

# ---- إنشاء فيديو Shorts ----
if short_clips:
    short_video = concatenate_videoclips(short_clips)
    if audio_clip:
        short_video = short_video.set_audio(audio_clip.subclip(0, short_video.duration))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_output = f"output/usa_trends_shorts_{timestamp}.mp4"
    short_video.write_videofile(short_output, fps=24, codec="libx264")
    print(f"✅ Shorts video created: {short_output}")

# ---- إنشاء فيديو طويل ----
if long_clips:
    long_video = concatenate_videoclips(long_clips)
    if audio_clip:
        long_video = long_video.set_audio(audio_clip.subclip(0, long_video.duration))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    long_output = f"output/usa_trends_long_{timestamp}.mp4"
    long_video.write_videofile(long_output, fps=24, codec="libx264")
    print(f"✅ Long video created: {long_output}")
