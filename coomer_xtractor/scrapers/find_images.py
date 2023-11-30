

def find_images(soup):
    media_links = []
    try:
        post_files = soup.find("div", class_="post__files")
        if post_files is None:
            return media_links
        post_file_links = post_files.find_all("a")
        file_links = [x.get('href') for x in post_file_links]
        [media_links.append(x) for x in file_links if x not in media_links and x is not None]
    except Exception as e:
        print(f"Encountered {e} while trying to find images.")
    return media_links