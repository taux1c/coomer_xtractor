
from httpx import AsyncClient
from asyncio import Semaphore, get_running_loop
from bs4 import BeautifulSoup as BS


from coomer_xtractor.browser_vars import headers
from coomer_xtractor.scrapers.download import download



async def find_files(urls, profile):
    requests_semaphore = Semaphore(profile.max_concurrent_requests)
    site = urls[0][0].split("/")[3]
    user = urls[0][0].split("/")[5]
    loop = get_running_loop()
    async with requests_semaphore:
        async with AsyncClient(follow_redirects=True, headers=headers) as client:
            for url_set in urls:
                for url in url_set:
                    r = await client.get(url)
                    if r.status_code == 200:
                        try:
                            soup = BS(r.content, 'lxml')
                            post_content = soup.find("div", class_="post__content")
                            post_files = soup.find("div", class_="post__files")
                            post_file_links = post_files.find_all("a")
                            file_links = [x.get('href') for x in post_file_links]
                            file_links = [link for link in file_links if link is not None]
                            loop.run_until_complete(await download(file_links, profile, site, user))
                            print(f"Found {len(file_links)} files in {url}.")
                        except Exception as e:
                            pass


