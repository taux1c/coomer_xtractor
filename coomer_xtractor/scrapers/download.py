
from httpx import AsyncClient
import aiofiles
from asyncio import Semaphore
from pathlib import Path


from coomer_xtractor.browser_vars import headers
from coomer_xtractor.scrapers.add_to_database import add_to_database, not_in_database


async def download(urls, profile, site, user, loop):
    download_path = Path(profile.save_location, site, user)
    download_path.mkdir(parents=True, exist_ok=True)
    download_semaphore = Semaphore(profile.max_concurrent_downloads)
    saved_urls = []
    async with download_semaphore:
        async with AsyncClient(follow_redirects=True, headers=headers) as client:
            urls = [x for x in urls if x is not None]
            for url in not_in_database(urls, profile):
                try:
                    r = await client.get(url)
                    if r.status_code == 200:
                        if "f=" in url:
                            file_name = url.split("f=")[-1]
                        else:
                            file_name = url.split("/")[-1][-20:]
                        async with aiofiles.open(Path(download_path, file_name), "wb") as f:
                            await f.write(r.content)
                            saved_urls.append(url)
                            print(f"Downloaded {file_name} to {download_path}.")
                except Exception as e:
                    print(f"Encountered {e} while trying to download {url}.")
    loop.run_until_complete(await add_to_database(saved_urls, profile))

