
import feedparser
import random
import json
import os
from datetime import datetime
from gtts import gTTS
from moviepy.editor import *
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

RSS = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

def load_config():
    with open("config.json","r") as f:
        return json.load(f)

def log_error(e):
    with open("logs.txt","a") as f:
        f.write(str(e) + "\n")

def choose_category(categories):
    return random.choice(categories)

def log_performance(video_id, category, title):
    entry = {
        "video_id": video_id,
        "category": category,
        "title": title,
        "publish_time": datetime.utcnow().isoformat(),
        "views": 0,
        "likes": 0,
        "score": 0
    }

    with open("performance_data.json","r") as f:
        data = json.load(f)

    data.append(entry)

    with open("performance_data.json","w") as f:
        json.dump(data, f, indent=4)

try:

    config = load_config()
    feed = feedparser.parse(RSS)

    if not os.path.exists("used.txt"):
        open("used.txt","w").close()

    with open("used.txt","r") as f:
        used_titles = f.read()

    count = 0

    for entry in feed.entries:

        if count >= config["videos_per_day"]:
            break

        if entry.title in used_titles:
            continue

        category = choose_category(config["categories"])
        news_title = entry.title

        with open("used.txt","a") as f:
            f.write(news_title + "\n")

        script = f"""
        Breaking News Update.

        {news_title}.

        Stay tuned for more updates from the United States.
        """

        tts = gTTS(script, lang="en")
        voice_file = f"voice_{count}.mp3"
        tts.save(voice_file)

        background = ColorClip(
            size=(1080,1920),
            color=(10,20,50),
            duration=config["video_duration"]
        )

        audio = AudioFileClip(voice_file)

        title_clip = TextClip(
            news_title,
            fontsize=70,
            color="white",
            size=(1000,None),
            method="caption"
        ).set_position("center").set_duration(6)

        video = CompositeVideoClip([background, title_clip])
        video = video.set_audio(audio)

        output_file = f"final_{count}.mp4"
        video.write_videofile(output_file, fps=24)

        # Log performance placeholder (video_id unknown until upload)
        log_performance("pending_upload", category, news_title)

        count += 1

except Exception as e:
    log_error(e)
