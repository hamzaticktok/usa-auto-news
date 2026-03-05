import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx

# إعدادات المسارات - ثابتة لضمان عدم حدوث خطأ
video_folder = "videos"
music_folder = "music"
output_folder = "output"
today = datetime.now().strftime("%Y-%m-%d")

os.makedirs(output_folder, exist_ok=True)

# التأكد من وجود ملفات
video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")]
if not video_files:
    print("❌ No videos found!")
    exit(1)

print(f"✅ Found {len(video_files)} videos. Processing...")

clips = []
for file in video_files:
    clip = VideoFileClip(file).resize(width=720) # توحيد الحجم
    clips.append(clip)

final_long = concatenate_videoclips(clips, method="compose")

# إضافة الموسيقى
music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]
if music_files:
    audio = AudioFileClip(random.choice(music_files))
    if audio.duration < final_long.duration:
        audio = afx.audio_loop(audio, duration=final_long.duration)
    else:
        audio = audio.subclip(0, final_long.duration)
    final_long = final_long.set_audio(audio)

# حفظ الفيديو الطويل
long_path = os.path.join(output_folder, f"video_long_{today}.mp4")
final_long.write_videofile(long_path, codec="libx264", audio_codec="aac", fps=24)

# حفظ فيديو Shorts (أول 59 ثانية)
short_duration = min(59, final_long.duration)
final_short = final_long.subclip(0, short_duration)
short_path = os.path.join(output_folder, f"video_shorts_{today}.mp4")
final_short.write_videofile(short_path, codec="libx264", audio_codec="aac", fps=24)

# إغلاق الملفات لتحرير الذاكرة
for clip in clips: clip.close()
final_long.close()
final_short.close()
print("🎉 Done! Videos saved in output folder.")
