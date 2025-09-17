# Create a CSV of character relationships for "폭싹 속았수다" (When Life Gives You Tangerines)
# Heuristic parser over the bullet-point cast lines copied from Wikipedia (Korean).
# The script extracts character names and tries to infer relationships (family, spouse/partner,
# dating, parent/child, sibling, grandchild, teacher-student, landlord-tenant, etc.) based on keywords.

import csv, re, os, pandas as pd

raw = """
### 애순 관식 가족
* 이지은 : 오애순 역 (아역 : 최여원, 김태연, 윤서연 / 중년, 노년 : 문소리) - ‘요망진 알감자’ 같은 반항아. 문학소녀.
* 박보검 : 양관식 역 (아역 : 이천무, 문우진 / 중년 : 박해준) - 양씨 집안의 4대 독자. 애순만 사랑하고 존중.
* 이지은 : 양금명 역 - 관식과 애순의 딸, 첫째.
* 강유석 : 양은명 역 - 관식과 애순의 장남, 둘째.
* 신새벽 : 양동명 역 - 관식과 애순의 차남, 셋째. (사망)

### 애순 관식 손주들
* 윤서진 : 박새봄 역 (아역: 경하윤)
* 김강훈 : 양제일 역 (아역: 신현서, 김인우, 16회)
* 손예린, 이주연 : 양영원 역 (아역: 김라희, 박가율, 송승아, 강리아)

### 애순의 가족
* 나문희 : 김춘옥 역 - 애순의 할머니
* 염혜란 : 전광례 역 - 애순의 어머니
* 정해균 : 오한무 역 - 일찍 유명을 달리한 오한규의 동생. 애순의 작은아버지
* 오정세 : 염병철 역 - 애순의 새 아버지이자 광례의 재혼한 남편 (1~2, 6회)
* 엄지원 : 나민옥 역 - 병철의 새 아내 (2, 4, 6회)
* 이연주 : 염순남 역 - 애순의 동생
* 최지혁 : 염순봉 역 - 애순의 동생
* 오연재 : 현이숙 역
* 조명연 : 오종구 역 (아역: 강규림)
* 변중희 : 김춘심 역
* 현승진 : 오종미 역 (아역: 김시하)

### 관식의 가족
* 김용림 : 박막천 역 - 관식의 할머니이자 마을의 무당
* 오민애 : 권계옥 역 - 관식의 어머니
* 서혜원 : 양경옥 역 - 관식의 동생이자 금명의 고모 (아역 : 김세아)
* 유병훈 : 양삼보 역 - 관식의 아버지

### 잠녀 3인방
* 차미경 : 박충수 역
* 이수미 : 최양임 역
* 백지원 : 홍경자 역

### 상길네
* 최대훈 : 부상길 역 - 애순의 맞선남, 도동리 부계장
* 장혜진 : 박영란 역 (젊은 시절: 채서안)
* 이수경 : 부현숙 역 - 상길과 영란의 딸
* 문유강 : 부오성 역 (아역: 박준서)
* 전민우 : 부한음 역
* 허진 : 고을남 역 - 상길의 어머니

### 금명 주변 인물
* 이준영 : 박영범 역 - 금명의 남자친구, 차관집 장남
* 故 강명주 : 윤부용 역 - 영범의 어머니
* 김선호 : 박충섭 역 - 극장 간판 그림을 그리는 화가, 금명의 남편 (9, 11~16회)

### 그 외 인물
* 이규회 : 박금명 역 - 영범의 아버지
* 표영서 : 오예림 역
* 김수연 : 민선 역
* 김계림 : 주경 역
* 남권아 : 제니네 가정부 역 - 제니의 집 가사도우미, 제니 어머니와 모종의 관계
* 김수안 : 오제니 역 - 금명이 불법 과외를 맡았던 학생 (7~8회)
* 김금순 : 김미향 역
* 김재영 : 제니 운전사 역 (7회)
* 김국희 : 교수 역 (8회)
* 전배수 : 송영삼 역 - 유학을 마친 금명이 하숙하는 집 주인 (10회)
* 정이서 : 송부선 역 - 영삼의 딸, 아버지 몰래 충섭과 연애중
* 유도윤 : 송영삼 아들 역
* 이지현 : 분희 역 - 중고책 및 제본 가게 운영
* 김해곤 : 김해봉 역 - 깐느 극장 사장 (9, 11, 13회)
* 하은섬 : 매점 아줌마 역
* 김동곤 : 영사기사 역
"""

# 1) 캐릭터 이름 추출
# 패턴: "* 배우 : 캐릭터명 역 - 설명"
name_pat = re.compile(r"^\*\s*[^:：]+[:：]\s*([^\s]+)\s*역\s*(?:-|—)?\s*(.*)$", re.MULTILINE)
characters = []  # list of (char_name, desc)
for m in name_pat.finditer(raw):
    char_name = m.group(1).strip()
    desc = m.group(2).strip()
    characters.append((char_name, desc))

char_set = sorted(set([c for c,_ in characters]))
# Helper for fuzzy matching short mentions like '관식', '애순' → '양관식','오애순'
def map_mention_to_char(mention, candidates):
    mention = mention.strip()
    # exact match preferred
    for c in candidates:
        if c == mention:
            return c
    # endswith match (e.g., '관식' in '양관식')
    for c in candidates:
        if c.endswith(mention) and len(mention) >= 2:
            return c
    # contains match
    for c in candidates:
        if mention in c and len(mention) >= 2:
            return c
    return None

# 2) 관계 추출 규칙
rules = [
    # (regex, relation_type, direction ('->','<-','-'), extractor for targets)
    (r"(.+?)의\s*딸", "parent-child", "<-", lambda s: [s]),      # X의 딸 → X <- 캐릭터
    (r"(.+?)의\s*아들|(.+?)의\s*장남|(.+?)의\s*차남", "parent-child", "<-", lambda s: [s]), # X의 아들 → X <- 캐릭터
    (r"(.+?)의\s*어머니|(.+?)의\s*엄마", "parent-child", "->", lambda s: [s]), # X의 어머니 → 캐릭터 -> X
    (r"(.+?)의\s*아버지|(.+?)의\s*아빠", "parent-child", "->", lambda s: [s]),  # X의 아버지 → 캐릭터 -> X
    (r"(.+?)의\s*할머니", "grandparent-grandchild", "->", lambda s: [s]),
    (r"(.+?)의\s*할아버지", "grandparent-grandchild", "->", lambda s: [s]),
    (r"(.+?)의\s*동생", "siblings", "-", lambda s: [s]),
    (r"(.+?)의\s*누나|(.+?)의\s*언니|(.+?)의\s*형|(.+?)의\s*오빠", "siblings", "-", lambda s: [s]),
    (r"(.+?)의\s*남자친구", "dating", "-", lambda s: [s]),
    (r"(.+?)의\s*남편", "spouse", "-", lambda s: [s]),
    (r"(.+?)의\s*아내", "spouse", "-", lambda s: [s]),
    (r"(.+?)의\s*맞선남", "matchdate", "-", lambda s: [s]),
    (r"(.+?)의\s*고모", "aunt-niece/nephew", "->", lambda s: [s]),
    (r"(.+?)의\s*새\s*아버지", "step-parent-child", "->", lambda s: [s]),
    (r"(.+?)의\s*새\s*아내", "spouse", "-", lambda s: [s]),
    (r"(.+?)의\s*아들", "parent-child", "->", lambda s: [s]), # 캐릭터가 X의 아들 → 캐릭터 -> X
    (r"(.+?)와\s*연애중|(.+?)과\s*연애중", "dating", "-", lambda s: [s]),
    (r"(.+?)의\s*학생|(.+?)가\s*불법\s*과외를\s*맡았던\s*학생", "teacher-student", "-", lambda s: [s]),
    (r"(.+?)하숙.*집\s*주인", "landlord-tenant", "-", lambda s: [s]),
]

edges = []  # (source, target, relation, evidence)

# Seed explicit couple from "관식과 애순의 딸/장남/차남" → spouse between 관식-애순
def add_spouse_if_pair(desc):
    pair_m = re.findall(r"([가-힣]+)\s*과\s*([가-힣]+)\s*의\s*(딸|아들|장남|차남)", desc)
    for a,b,_ in pair_m:
        A = map_mention_to_char(a, char_set)
        B = map_mention_to_char(b, char_set)
        if A and B:
            # spouse/partner undirected
            if (A,B,"spouse",None) not in edges and (B,A,"spouse",None) not in edges:
                edges.append((A,B,"spouse","관식과 애순의 자녀 언급으로 부부/파트너 추정"))

for char, desc in characters:
    add_spouse_if_pair(desc)

for char, desc in characters:
    # apply rules
    for pat, rel, direction, target_extractor in rules:
        for m in re.finditer(pat, desc):
            # find first non-None group
            groups = [g for g in m.groups() if g]
            for g in groups:
                g = g.strip()
                # clean particles like '영삼의' → '영삼'
                g = re.sub(r"[의]$", "", g)
                target = map_mention_to_char(g, char_set)
                if not target:
                    continue
                if direction == "->":
                    edges.append((char, target, rel, desc))
                elif direction == "<-":
                    edges.append((target, char, rel, desc))
                else:
                    # undirected
                    edges.append((char, target, rel, desc))

# Deduplicate edges (keep first evidence)
seen = set()
deduped = []
for s,t,r,e in edges:
    key = (s,t,r)
    revkey = (t,s,r)
    if key in seen or revkey in seen:
        continue
    seen.add(key)
    deduped.append((s,t,r,e))

out_path = "/mnt/data/when_life_gives_you_tangerines_relationships.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["source","target","relation","evidence"])
    for row in deduped:
        w.writerow(row)

# Show a quick preview
df = pd.read_csv(out_path)
df.head(30)
