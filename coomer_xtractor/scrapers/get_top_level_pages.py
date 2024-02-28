
from httpx import AsyncClient
from bs4 import BeautifulSoup
from coomer_xtractor.browser_vars import headers


async def get_pages(url):
    async with AsyncClient(follow_redirects=True, headers=headers) as client:
        r = await client.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        link_list = []
        for link in soup.select('menu a[href]'):
            link_list.append('https://coomer.su' + link['href'])
        urls = list(set(link_list))
        return urls
