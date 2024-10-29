"""Script to handle the scraping of LastFM album tags and their DB insertion."""
import bs4
import requests as req

from db_utils import get_all_tags, insert_tag, insert_album_tag_assignment


def load_page_source(url: str) -> str:
    """Returns the page source from a URL."""
    response = req.get(url, timeout=10)
    if response.status_code == 200:
        return response.content
    raise ConnectionError("Failed to retrieve page source.")


def get_lastfm_url(album: str, artist: str) -> str:
    """Forms a Last FM page URL from an album and artist name."""
    album_str = "+".join(album.split(" "))
    artist_str = "+".join(artist.split(" "))
    return f"https://www.last.fm/music/{artist_str}/{album_str}"


def get_soup(source: str) -> bs4.BeautifulSoup:
    """Returns a BS4 object from a page's source."""
    return bs4.BeautifulSoup(source, 'html.parser')


def get_tag_section(soup: bs4.BeautifulSoup) -> bs4.Tag:
    """Returns the page section containing tags."""
    tags = soup.find("section", class_="catalogue-tags")
    return tags


def parse_tags(tag_section: bs4.Tag) -> list[str]:
    """Returns a list of tags from a tag section."""
    tags = tag_section.find_all("li", class_="tag")
    return [tag.find("a").text for tag in tags]


def process_tags(album_id: int, album_title: str, artist_name: str):
    """Scrapes and inserts the tags of a particular album."""
    url = get_lastfm_url(album_title, artist_name)
    source = load_page_source(url)
    soup = get_soup(source)
    tags = parse_tags(get_tag_section(soup))
    existing_tags = get_all_tags()
    for tag in tags:
        if tag not in existing_tags:
            existing_tags[tag] = insert_tag(tag)
        insert_album_tag_assignment(album_id, existing_tags[tag])
