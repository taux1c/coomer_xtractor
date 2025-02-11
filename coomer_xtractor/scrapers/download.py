from playwright.async_api import async_playwright
import aiofiles
from asyncio import Semaphore
from pathlib import Path

from coomer_xtractor.scrapers.add_to_database import add_to_database, not_in_database


async def download(urls, profile, site, user, loop):
    download_path = Path(profile.save_location, site, user)
    download_path.mkdir(parents=True, exist_ok=True)
    download_semaphore = Semaphore(profile.max_concurrent_downloads)
    saved_urls = []

    async with download_semaphore:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Launch browser in headless mode
            page = await browser.new_page()

            # Define a custom download path for Playwright
            download_dir = str(download_path)  # Set download folder to be used by Playwright
            await page.set_download_behavior(behavior='save', download_path=download_dir)  # Set download path

            urls = [x for x in urls if x is not None]
            for url in not_in_database(urls, profile):
                try:
                    # Go to the page and retrieve the response
                    response = await page.goto(url)

                    # Check for content type in response headers
                    content_type = response.headers.get('content-type', '')

                    # If it's a binary file (image/video)
                    if 'image' in content_type or 'video' in content_type:
                        file_name = url.split("/")[-1][-20:]  # Extract file name
                        file_path = Path(download_path, file_name)

                        # Save the binary content of the file
                        async with aiofiles.open(file_path, "wb") as f:
                            await f.write(await response.body())  # Write binary data to file
                        saved_urls.append(url)
                        print(f"Downloaded {file_name} to {download_path}.")
                    else:
                        # If it's not a binary file, save it as HTML content
                        await page.wait_for_load_state('networkidle', timeout=60000)  # Wait for 60 seconds
                        file_name = url.split("/")[-1][-20:]  # Extract file name
                        file_path = Path(download_path, file_name)

                        # Get page content for non-binary file types (e.g., HTML)
                        content = await page.content()
                        async with aiofiles.open(file_path, "wb") as f:
                            await f.write(content.encode())  # Encode HTML content and write
                        saved_urls.append(url)
                        print(f"Downloaded {file_name} to {download_path}.")

                except Exception as e:
                    print(f"Encountered {e} while trying to download {url}.")

            await browser.close()

    await add_to_database(saved_urls, profile)
