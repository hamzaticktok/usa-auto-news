import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx

# ===============================
# SETTINGS
# ===============================
output_folder = "output"
music_folder = "music"
today = datetime.now().strftime("%Y-%m-%d")
short_max_duration = 60

os.makedirs(output_folder, exist_ok=True)

# ===============================
# LOAD VIDEO FILES
# ===============================
video_files = [
    os.path.join(output_folder, f)
    for f in os.listdir(output_folder)
    if f.endswith(".mp4") and "final" not in f
]

if not video_files:
    print("❌ No input video files found in output folder.")
    exit(1)

clips = []
for file in video_files:
    try:
        clip = VideoFileClip(file)
        clip = clip.resize(width=720)
        clips.append(clip)
        print(f"Loaded: {file}")
    except Exception as e:
        print(f"⚠️ Error loading {file}: {e}")

final_long = concatenate_videoclips(clips, method="compose")

# ===============================
# BACKGROUND MUSIC
# ===============================
music_files = []
if os.path.exists(music_folder):
    music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]

if music_files:
    selected_music = random.choice(music_files)
    audio = AudioFileClip(selected_music)
    if audio.duration < final_long.duration:
        audio = afx.audio_loop(audio, duration=final_long.duration)
    else:
        audio = audio.subclip(0, final_long.duration)
    final_long = final_long.set_audio(audio)
    print(f"🎵 Music added: {selected_music}")

# ===============================
# EXPORT LONG VIDEO
# ===============================
long_output_path = os.path.join(output_folder, f"usa_trends_long_{today}.mp4")
final_long.write_videofile(long_output_path, codec="libx264", audio_codec="aac", fps=24)

# ===============================
# EXPORT SHORT VIDEO
# ===============================
short_duration = min(short_max_duration, final_long.duration)
final_short = final_long.subclip(0, short_duration)
short_output_path = os.path.join(output_folder, f"usa_trends_shorts_{today}.mp4")
final_short.write_videofile(short_output_path, codec="libx264", audio_codec="aac", fps=24)

# ===============================
# CLEANUP
# ===============================
for clip in clips:
    clip.close()
final_long.close()
final_short.close()
if music_files:
    audio.close()

print("🎉 Videos generated successfully!")
