# extract_characters.py
import json, re
from collections import defaultdict
from typing import List, Dict

# 1) 기본 인물 사전(표준명 → 별칭/변형)
CHAR_DICT = {
    "Tanjiro Kamado": ["Tanjiro", "Kamado", "탄지로"],
    "Nezuko Kamado": ["Nezuko", "네즈코", "Nezuko Kamado"],
    "Giyu Tomioka": ["Giyu", "Tomioka", "기유", "Tomioka Giyu"],
    "Sakonji Urokodaki": ["Sakonji", "Urokodaki", "우로코다키"],
    "Kanao Tsuyuri": ["Kanao", "츠유리 카나오", "Tsuyuri"],
    "Kyojuro Rengoku": ["Rengoku", "렌고쿠", "Kyojuro"],
    # 필요시 계속 보강
}

# 2) 역색인(별칭 → 표준명)
ALIAS2CANON = {}
for canon, aliases in CHAR_DICT.items():
    for a in [canon] + aliases:
        ALIAS2CANON[a.lower()] = canon

def normalize_names(text: str) -> List[str]:
    found = set()
    # 단순 토큰 매칭(공백/문장부호 경계)
    for alias_lc, canon in ALIAS2CANON.items():
        pattern = r"\b" + re.escape(alias_lc) + r"\b"
        if re.search(pattern, text.lower()):
            found.add(canon)
    return sorted(found)

def main():
    data = json.load(open("output/1_원본데이터.json", encoding="utf-8"))
    for ep in data:
        syn = ep.get("synopsis") or ""
        ep["characters"] = normalize_names(syn)

    out = "output/2_인물추출.json"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("인물 추출 완료:", out)

if __name__ == "__main__":
    main()
