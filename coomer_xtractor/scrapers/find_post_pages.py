
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from urllib.parse import urljoin


from coomer_xtractor.config import base_url

from ..work import soup_queue

from ..config import dev_mode

if dev_mode:
    hdl = False
else:
    hdl = True


def find_media(soup):
    post_urls = []
    all_cards = soup.find("div", class_="card-list__items")
    posts = all_cards.find_all("article", class_="post-card")
    for post in posts:
        link = post.find('a')['href']
        url = urljoin(base_url, link)
        post_urls.append(url)
    return post_urls




async def find_media_posts(urls):
    async with async_playwright() as p:
        # Launch the browser and create a page
        browser = await p.chromium.launch(headless=hdl)
        page = await browser.new_page()

        for url in urls:
            # Go to the URL
            await page.goto(url)

            # Wait for the page to reach network idle state (no network activity for at least 500 ms)
            await page.wait_for_load_state('networkidle')

            # Get the page content (HTML) after it has loaded
            page_content = await page.content()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(page_content, "lxml")

            # Put the soup object in the queue (same as the original function)
            await soup_queue.put(soup)

        # Close the browser after processing all URLs
        await browser.close()


async def scrape_posts(urls):
    if len(urls) > 0:
        post_urls = []
        await find_media_posts(urls)
        while not soup_queue.empty():
            soup = await soup_queue.get()
            post_urls.append(find_media(soup))
        return post_urls
    else:
        raise ValueError("No posts were found!")


