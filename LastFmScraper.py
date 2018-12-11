from lxml import html
from lxml import etree


def scrape_from_string(content):
    tree = html.fromstring(content)

    track_names = tree.xpath('//section[@id="recent-tracks-section"]/table//td[@class="chartlist-name"]//a[@class="link-block-target"]')
    time_cells = tree.xpath('//td[@class="chartlist-timestamp"]/span[@title]')

    tracks = []
    for i, track in enumerate(track_names):
        track_info = list(map(str.strip, track.get('title').split(u'\u2014')))
        is_playing = False
        if 'now-scrobbling' in track.getparent().getparent().getparent().get('class'):
            is_playing = True
        else:
            # slight hack:
            # if there is no "now playing" track then we get a different
            # length time_cells list to the track_names list
            # If they are the same length, then we can use the same
            # index for both track names and play times
            if len(time_cells) == len(track_names):
                index = i
            else:
                # Here we have a "now playing" track and need to adjust for
                # the shorter list of time cells
                index = i - 1
        tracks.append({
            "artist": track_info[0],
            "title": track_info[1],
            "playing": is_playing,
            "time": time_cells[index].get('title')
        })
    return tracks


if __name__ == '__main__':
    import requests
    import json
    page = requests.get('http://www.last.fm/user/Zaphodb65')
    if page.status_code != 200:
        die("Failed to connect to last.fm")

    tracks = scrape_from_string(page.content)

    print(json.dumps(tracks))
