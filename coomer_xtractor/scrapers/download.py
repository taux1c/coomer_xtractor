
from httpx import AsyncClient
import aiofiles
from asyncio import Semaphore
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

class SavedUrls(Base):
    __tablename__ = "saved_urls"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    url = Column(Text, unique=True)

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
                        if "f=" in url:
                            file_name = url.split("f=")[-1]
                        else:
                            file_name = url.split("/")[-1][-20:]
                        async with aiofiles.open(Path(download_path, file_name), "wb") as f:
                            await f.write(r.content)
                            print(f"Downloaded {file_name} to {download_path}.")
                except Exception as e:
                    print(f"Encountered {e} while trying to download {url}.")

