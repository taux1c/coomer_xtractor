from bs4 import BeautifulSoup
from httpx import AsyncClient
from asyncio import Queue
from urllib.parse import urljoin

from coomer_xtractor.browser_vars import headers
from coomer_xtractor.config import base_url

soup_queue = Queue()




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
    async with AsyncClient(follow_redirects=True, headers=headers) as client:
        for url in urls:
            r = await client.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            await soup_queue.put(soup)

async def scrape_posts(urls):
    post_urls = []
    await find_media_posts(urls)
    while not soup_queue.empty():
        soup = await soup_queue.get()
        post_urls.append(find_media(soup))
    return post_urls



