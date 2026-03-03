# main.py
from moviepy.editor import ColorClip
import os
from datetime import datetime

# إنشاء مجلد output إذا لم يكن موجود
os.makedirs("output", exist_ok=True)

# توليد اسم فيديو فريد بالوقت والتاريخ
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
video_filename = f"test_{timestamp}.mp4"
output_path = os.path.join("output", video_filename)

# إنشاء الفيديو (فيديو أحمر، 5 ثواني، 720x1280)
print(f"Creating video: {video_filename}")
clip = ColorClip(size=(720, 1280), color=(255, 0, 0))
clip = clip.set_duration(5)

# حفظ الفيديو
clip.write_videofile(output_path, fps=24)
print(f"✅ Video created at {output_path}")
