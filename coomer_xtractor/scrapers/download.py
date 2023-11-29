
from httpx import AsyncClient
import aiofiles
from asyncio import Semaphore
from pathlib import Path


from coomer_xtractor.browser_vars import headers


async def download(urls, profile, site, user):
    download_path = Path(profile.save_location, site, user)
    download_path.mkdir(parents=True, exist_ok=True)
    download_semaphore = Semaphore(profile.max_concurrent_downloads)
    async with download_semaphore:
        async with AsyncClient(follow_redirects=True, headers=headers) as client:
            urls = [x for x in urls if x is not None]
            for url in urls:
                try:
                    r = await client.get(url)
                    if r.status_code == 200:
                        file_name = url.split("f=")[-1]
                        async with aiofiles.open(Path(download_path, file_name), "wb") as f:
                            await f.write(r.content)
                            print(f"Downloaded {file_name} to {download_path}.")
                except Exception as e:
                    print(f"Encountered {e} while trying to download {url}.")

