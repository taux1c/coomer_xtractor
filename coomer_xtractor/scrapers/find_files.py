
from httpx import AsyncClient
from asyncio import Semaphore, get_running_loop, gather
from bs4 import BeautifulSoup as BS


from coomer_xtractor.browser_vars import headers
from coomer_xtractor.scrapers.download import download
from coomer_xtractor.scrapers.find_videos import find_videos
from coomer_xtractor.scrapers.find_images import find_images



async def find_files(urls, profile):
    requests_semaphore = Semaphore(profile.max_concurrent_requests)
    site = urls[0][0].split("/")[3]
    user = urls[0][0].split("/")[5]
    loop = get_running_loop()
    async with requests_semaphore:
        async with AsyncClient(follow_redirects=True, headers=headers) as client:
            tasks = []
            for url_set in urls:
                for url in url_set:
                    r = await client.get(url)
                    if r.status_code == 200:
                        try:
                            media_links = []
                            soup = BS(r.content, 'lxml')
                            post_content = soup.find("div", class_="post__content")
                            post_videos = soup.find_all("video")
                            video_links = find_videos(post_videos)
                            if len(video_links) > 0:
                                try:
                                    tasks.append(loop.create_task(download(video_links, profile, site, user, loop)))
                                except Exception as e:
                                    print(f"Encountered {e} while downloading {video_links}.")
                            image_links = find_images(soup)
                            if len(image_links) > 0:
                                media_links.extend(image_links)
                                tasks.append(loop.create_task(download(media_links, profile, site, user, loop)))
                                print(f"Found {len(image_links)} files in {url}.")
                        except Exception as e:
                            print(e)

    await gather(*tasks)
