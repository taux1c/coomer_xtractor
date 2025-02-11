from httpx import AsyncClient, RequestError, ConnectTimeout
import aiofiles
from asyncio import Semaphore
from pathlib import Path
from faker import Faker
import backoff

from coomer_xtractor.scrapers.add_to_database import add_to_database, not_in_database


# Initialize Faker instance
fake = Faker()

# Function to generate random headers using Faker
def generate_headers():
    return {
        "User-Agent": fake.user_agent(),
        "Accept-Language": fake.language_code(),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }

# Retry logic with backoff
def on_backoff(details):
    print(f"Backing off for {details['wait']} seconds due to {details['exception']}.")

@backoff.on_exception(backoff.expo, (RequestError, ConnectTimeout), max_tries=5, on_backoff=on_backoff)
async def fetch_url(client, url, headers):
    return await client.get(url, headers=headers, timeout=30.0)  # Adjusted timeout


async def download(urls, profile, site, user, loop):
    download_path = Path(profile.save_location, site, user)
    download_path.mkdir(parents=True, exist_ok=True)
    download_semaphore = Semaphore(profile.max_concurrent_downloads)
    saved_urls = []
    async with download_semaphore:
        async with AsyncClient(follow_redirects=True) as client:
            urls = [x for x in urls if x is not None]
            for url in not_in_database(urls, profile):
                try:
                    headers = generate_headers()  # Use the generated headers here
                    r = await fetch_url(client, url, headers)  # Use fetch_url with retry logic
                    if r.status_code == 200:
                        if "f=" in url:
                            file_name = url.split("f=")[-1]
                        else:
                            file_name = url.split("/")[-1][-20:]
                        async with aiofiles.open(Path(download_path, file_name), "wb") as f:
                            await f.write(r.content)
                            saved_urls.append(url)
                            print(f"Downloaded {file_name} to {download_path}.")
                except Exception as e:  # Catch all exceptions here
                    print(f"Encountered exception: {type(e).__name__} with args: {e.args} while trying to download {url}.")
    await add_to_database(saved_urls, profile)
