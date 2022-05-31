import youtube_dl
with youtube_dl.YoutubeDL() as ydl:
    info = ydl.extract_info("https://youtu.be/NYGKiz-2dyU", download=True)
