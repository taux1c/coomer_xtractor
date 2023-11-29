
from coomer_xtractor.models.profiles import select_profile


from coomer_xtractor.scrapers.get_top_level_pages import get_pages
from coomer_xtractor.scrapers.find_post_pages import scrape_posts
from coomer_xtractor.scrapers.find_files import find_files

async def scrape(url, profile):
    await find_files(await scrape_posts(await get_pages(url)), profile)

async def scrape_url():
    profile = select_profile()
    url = input("Enter a url: ")
    await scrape(url, profile)

async def scrape_favorites():
    profile = select_profile()
    for url in profile.favorite_urls:
        await scrape(url, profile)
