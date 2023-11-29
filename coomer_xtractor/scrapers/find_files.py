
from httpx import AsyncClient
from asyncio import Semaphore
from bs4 import BeautifulSoup as BS


from coomer_xtractor.browser_vars import headers
from coomer_xtractor.scrapers.download import download

requests_semaphore = Semaphore(20)

async def find_files(urls, profile):
    site = urls[0][0].split("/")[3]
    user = urls[0][0].split("/")[5]
    all_file_links = []
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
                            file_links = [x['href'] for x in post_file_links if x is not None]
                            await download(file_links, profile, site, user)
                            print(f"Found {len(file_links)} files in {url}.")
                        except Exception as e:
                            print(f"Encountered {e} while trying to find files.")


