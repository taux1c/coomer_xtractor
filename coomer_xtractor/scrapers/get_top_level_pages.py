
from httpx import AsyncClient
from bs4 import BeautifulSoup
from coomer_xtractor.browser_vars import headers


async def get_pages(url):
    async with AsyncClient(follow_redirects=True, headers=headers) as client:
        r = await client.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        last_page_count = int(soup.find('a', string=">>")['href'].split('o=')[-1])
        pages = last_page_count/50
        base = 0
        urls = []
        urls.append(url)
        for i in range(int(pages)):
            base += 50
            urls.append(f"{url}?o={base}")
        return urls