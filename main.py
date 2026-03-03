# main.py
from moviepy.editor import ColorClip
import os
from datetime import datetime

# عدد الفيديوهات التي تريد توليدها في كل تشغيل
NUM_VIDEOS = 3  # يمكنك تغييره لأي عدد

# إنشاء مجلد output إذا لم يكن موجودًا
os.makedirs("output", exist_ok=True)

# ملف لوغ لتسجيل الفيديوهات
log_file = os.path.join("output", "video_log.txt")
with open(log_file, "a") as log:

    for i in range(1, NUM_VIDEOS + 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"video_{timestamp}_{i}.mp4"
        output_path = os.path.join("output", video_filename)

        print(f"Creating video {i}/{NUM_VIDEOS}: {video_filename}")

        # إنشاء فيديو أحمر 5 ثواني، 720x1280
        clip = ColorClip(size=(720, 1280), color=(255, 0, 0))
        clip = clip.set_duration(5)

        # حفظ الفيديو
        clip.write_videofile(output_path, fps=24)

        # تسجيل المعلومات في لوغ
        file_size_mb = os.path.getsize(output_path) / (1024*1024)
        log.write(f"{datetime.now()} | {video_filename} | Duration: 5s | Size: {file_size_mb:.2f} MB\n")

        print(f"✅ Video created: {video_filename}, Size: {file_size_mb:.2f} MB")
