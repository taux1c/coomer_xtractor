

def find_videos(soup):
    try:
        video_links = []
        post_videos = soup.find_all("video")
        if post_videos:
            for video in post_videos:
                source = video.find("source")
                src = source.get("src")
                video_links.append(src)
    except:
        video_links = []
        pass

    return video_links