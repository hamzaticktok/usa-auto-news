import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx

# ===============================
# SETTINGS
# ===============================
video_folder = "videos"
music_folder = "music"
output_folder = "output"
today = datetime.now().strftime("%Y-%m-%d")
short_max_duration = 60

os.makedirs(output_folder, exist_ok=True)

# ===============================
# LOAD VIDEO FILES
# ===============================
video_files = [
    os.path.join(video_folder, f)
    for f in os.listdir(video_folder)
    if f.endswith(".mp4")
]

if not video_files:
    print("❌ No video files found in 'videos/' folder.")
    exit(1)

clips = []
for file in video_files:
    clip = VideoFileClip(file).resize(width=720)
    clips.append(clip)
    print(f"Loaded: {file}")

final_long = concatenate_videoclips(clips, method="compose")

# ===============================
# ADD MUSIC
# ===============================
music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]
if music_files:
    audio = AudioFileClip(random.choice(music_files))
    if audio.duration < final_long.duration:
        audio = afx.audio_loop(audio, duration=final_long.duration)
    else:
        audio = audio.subclip(0, final_long.duration)
    final_long = final_long.set_audio(audio)
    print("🎵 Music added")

# ===============================
# EXPORT LONG VIDEO
# ===============================
long_path = os.path.join(output_folder, f"usa_trends_long_{today}.mp4")
final_long.write_videofile(long_path, codec="libx264", audio_codec="aac", fps=24)

# ===============================
# EXPORT SHORT VIDEO
# ===============================
short_duration = min(short_max_duration, final_long.duration)
final_short = final_long.subclip(0, short_duration)
short_path = os.path.join(output_folder, f"usa_trends_shorts_{today}.mp4")
final_short.write_videofile(short_path, codec="libx264", audio_codec="aac", fps=24)

# ===============================
# CLEANUP
# ===============================
for clip in clips:
    clip.close()
final_long.close()
final_short.close()
if music_files:
    audio.close()

print("🎉 All videos generated successfully!")
