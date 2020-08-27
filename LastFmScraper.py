from lxml import html
from lxml import etree


def scrape_from_string(content):
    tree = html.fromstring(content)

    track_names = tree.xpath('//section[@id="recent-tracks-section"]/table//td[@class="chartlist-name"]//a')
    track_artists = tree.xpath('//section[@id="recent-tracks-section"]/table//td[@class="chartlist-artist"]//a')
    track_times = tree.xpath('//section[@id="recent-tracks-section"]/table//td[contains(concat(" ",normalize-space(@class)," ")," chartlist-timestamp ")]//span')

    return [{"title": x.text_content(), "artist": y.text_content(), "time": z.get('title')} for (x, y, z) in zip(track_names, track_artists, track_times)]


if __name__ == '__main__':
    import requests
    import json
    page = requests.get('http://www.last.fm/user/Zaphodb65')
    if page.status_code != 200:
        die("Failed to connect to last.fm")

    tracks = scrape_from_string(page.content)

    print(json.dumps(tracks))
