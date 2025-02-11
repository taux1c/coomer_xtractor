from asyncio import Semaphore, get_running_loop, gather
from bs4 import BeautifulSoup as BS
from playwright.async_api import async_playwright

from coomer_xtractor.scrapers.download import download
from coomer_xtractor.scrapers.find_videos import find_videos
from coomer_xtractor.scrapers.find_images import find_images

from ..config import dev_mode

if dev_mode:
    hdl = False
else:
    hdl = True

async def find_files(urls, profile):
    print("Finding files")
    requests_semaphore = Semaphore(profile.max_concurrent_requests)
    site = urls[0][0].split("/")[3]
    user = urls[0][0].split("/")[5]
    loop = get_running_loop()

    async with async_playwright() as p:
        # Launch Playwright browser
        browser = await p.chromium.launch(headless=hdl)
        page = await browser.new_page()

        tasks = []
        for url_set in urls:
            for url in url_set:
                async with requests_semaphore:  # Ensure limited concurrent requests
                    await page.goto(url)
                    await page.wait_for_load_state('networkidle')  # Wait until network is idle

                    # Get the HTML content of the page after it has loaded
                    content = await page.content()

                    try:
                        media_links = []
                        soup = BS(content, 'lxml')

                        # Parse post content and media links
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
                        print(f"Error processing {url}: {e}")

        # Close the browser once the scraping is done
        await browser.close()

    # Wait for all download tasks to finish
    await gather(*tasks)
