from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from ..config import dev_mode

if dev_mode:
    hdl = False
else:
    hdl = True

async def get_pages(url):
    async with async_playwright() as p:
        # Launch the browser and create a page
        browser = await p.chromium.launch(headless=hdl)
        page = await browser.new_page()

        # Go to the URL
        await page.goto(url)

        # Wait for the page to reach network idle state (no network activity for at least 500 ms)
        await page.wait_for_load_state('networkidle')

        # Get the page content (HTML) after it has loaded
        page_content = await page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(page_content, 'lxml')

        # Extract links using BeautifulSoup's select method
        link_list = []
        for link in soup.select('menu a[href]'):
            href = link.get('href')
            if href:
                link_list.append('https://coomer.su' + href)

        # Remove duplicates by converting to a set and back to a list
        urls = list(set(link_list))

        # Close the browser
        await browser.close()
        return urls
