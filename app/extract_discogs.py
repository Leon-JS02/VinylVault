"""Script to handle the extraction of listings from Discogs."""
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import bs4
from endpoints import DISCOGS_SEARCH


def format_search_url(artist_name: str, album_name: str) -> str:
    """Formats the URL for a Discogs marketplace search for a given
    artist and album name."""
    artist_chunk = "+".join(artist_name.split(" "))
    album_chunk = "+".join(album_name.split(" "))
    filters = "&format=Vinyl"
    return f"{DISCOGS_SEARCH}{artist_chunk}+{album_chunk}{filters}"


def get_soop(page_source: str) -> bs4.BeautifulSoup:
    """Returns a page soup from a URL."""
    return bs4.BeautifulSoup(page_source, 'html.parser')


def scrape_listings(page_soop: bs4.BeautifulSoup) -> list[bs4.Tag]:
    """Returns a list of listing objects from a page soup."""
    return page_soop.find_all('tr', class_="shortcut_navigable")


def load_page_source(url: str) -> str:
    """Loads the page source using Selenium with Firefox WebDriver in headless mode.
    Returns the page source as a string."""
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
        page_source = driver.page_source
        return page_source
    finally:
        driver.quit()


def get_item_description(listing: bs4.Tag) -> str:
    """Returns an item's description from a listing tag."""
    return listing.find("a", class_="item_description_title").text


def get_original_price(listing: bs4.Tag) -> str:
    """Returns an item's original price from a listing tag."""
    return listing.find("span", class_="price").text


def get_converted_price(listing: bs4.Tag) -> str:
    """Returns an item's converted price from a listing tag."""
    return listing.find("span", class_="converted_price").text


def get_listing_url(listing: bs4.Tag) -> str:
    """Returns an item's listing URL."""
    base_url = "https://discogs.com/"
    slug = listing.find("a", class_="item_description_title")['href']
    return f"{base_url}{slug}"


def clean_price(price_string):
    """Removes the comment from a price label."""
    match = re.search(r"[€$£¥₹]\s?\d+(\.\d{1,2})?", price_string)
    return match.group(0) if match else price_string


def clean_media_condition(raw_condition: str) -> str:
    """Removes the comment from a media condition label."""
    clean_condition = raw_condition.strip()
    match = re.match(r"^[^\n]+", clean_condition)
    return match.group(0).strip() if match else clean_condition


def get_media_condition(listing: bs4.Tag) -> str:
    """Returns an item's media condition from a listing tag."""
    condition_box = listing.find("p", class_="item_condition")
    condition_value_tag = condition_box.find_all('span')[2]
    return condition_value_tag.get_text()


def get_sleeve_condition(listing: bs4.Tag) -> str:
    """Returns an item's sleeve condition from a listing tag."""
    sleeve_condition_tag = listing.find('span', class_='item_sleeve_condition')
    return sleeve_condition_tag.get_text(strip=True)


def get_seller_rating(listing: bs4.Tag) -> str:
    """Returns an item's seller rating from a listing tag."""
    seller_info_tag = listing.find('td', class_='seller_info')
    return seller_info_tag.find_all('li')[1].find('strong').text


def parse_listing(listing: bs4.Tag) -> dict:
    """Returns a dictionary consisting of listing information."""
    return {
        'description': get_item_description(listing),
        'original_price': clean_price(get_original_price(listing)),
        'converted_price': clean_price(get_converted_price(listing)),
        'url': get_listing_url(listing),
        'media_condition': clean_media_condition(get_media_condition(listing)),
        'sleeve_condition': get_sleeve_condition(listing),
        'seller_rating': get_seller_rating(listing)
    }
