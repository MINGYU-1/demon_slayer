# build_graph.py
import json
from itertools import combinations
from collections import defaultdict

episodes = json.load(open("output/2_인물추출.json", encoding="utf-8"))

# 노드 집합
persons = set()
# 간선 누적 (무방향)
co_edges = defaultdict(int)

# Person–Episode 관계도 함께 만들기
appear = []  # (person, season, ep_no, title)

for ep in episodes:
    chars = ep.get("characters", [])
    season, epno, title = ep["season"], ep["episode_in_season"], ep.get("title")
    for c in chars:
        persons.add(c)
        appear.append((c, season, epno, title))

    for a, b in combinations(sorted(set(chars)), 2):
        co_edges[(a, b, season, epno)] += 1  # 에피소드 단위 weight=1

# 출력 구조(Neo4j 적재용)
graph = {
    "persons": sorted(persons),
    "episodes": [
        {"season": e["season"], "ep": e["episode_in_season"], "title": e.get("title")}
        for e in episodes
    ],
    "appears_in": [
        {"person": p, "season": s, "ep": e, "title": t} for (p, s, e, t) in appear
    ],
    "co_occurs": [
        {"p1": a, "p2": b, "season": s, "ep": e, "weight": w}
        for (a, b, s, e), w in co_edges.items()
    ],
}
out = "output/3_graph.json"
json.dump(graph, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("그래프 구성 완료:", out)
