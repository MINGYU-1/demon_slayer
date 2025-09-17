# scrape_episodes.py
import json, re, time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch_episode(link: str) -> List[Dict]:
    season = int(re.search(r"season_(\d+)", link).group(1))
    print(f"Fetching Season {season} from: {link}")
    response = requests.get(link, headers=HDRS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select_one("table.wikitable.plainrowheaders.wikiepisodetable")
    rows = table.select("tr.vevent.module-episode-list-row")

    episodes = []
    for i, row in enumerate(rows, start=1):
        # 제목/방영일(가능한 경우)
        title_cell = row.select_one("th.summary")
        title = title_cell.get_text(strip=True) if title_cell else None
        airdate_cell = row.select_one("td.airdate")
        airdate = airdate_cell.get_text(strip=True) if airdate_cell else None

        synopsis = None
        synopsis_row = row.find_next_sibling("tr", class_="expand-child")
        if synopsis_row:
            synopsis_cell = synopsis_row.select_one("td.description div.shortSummaryText")
            synopsis = synopsis_cell.get_text(" ", strip=True) if synopsis_cell else None

        episodes.append({
            "season": season,
            "episode_in_season": i,
            "title": title,
            "airdate": airdate,
            "synopsis": synopsis,
        })
        time.sleep(0.2)  # 예의 있는 딜레이

    return episodes

def main():
    episode_links = [
        "https://en.wikipedia.org/wiki/Demon_Slayer:_Kimetsu_no_Yaiba_season_1"
    ]
    all_episodes = []
    for link in episode_links:
        all_episodes.extend(fetch_episode(link))

    out = "output/1_원본데이터.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)
    print("데이터 수집 완료:", out)

if __name__ == "__main__":
    main()

