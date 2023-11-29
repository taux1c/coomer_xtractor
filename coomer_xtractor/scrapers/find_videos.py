

def find_videos(post_videos):
    video_links = []
    try:
        if len(post_videos) > 0:
            for video in post_videos:
                source = video.find("source")
                src = source.get("src")
                video_links.append(src)
    except Exception as e:
        print(f"Encountered {e} while finding videos in {post_videos}.")

    return video_links