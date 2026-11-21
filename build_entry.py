#!/usr/bin/env python3
"""news-image-20261121-cand-a — "THE WORLD IN ONE DAY".

Generates entry.png deterministically with PIL: a one-page broadsheet
summing up Saturday 21 November 2026 in 35 stories, all first reported
that day. Flat vector-style illustrations drawn with PIL shapes only
(no photos). All paths resolve from this script's own directory.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = 1600
H = 4400
CREAM = (247, 242, 231)
PAPER = (255, 253, 246)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (180, 35, 24)
GOLD = (176, 132, 52)
TEAL = (18, 110, 105)
GREY = (90, 92, 98)
LIGHT = (226, 220, 205)
SKY = (214, 230, 238)
SAND = (238, 222, 190)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


# ---------------------------------------------------------------- data
# (number, headline, place, source, region, scene)
LEADS = [
    (1, "COP31 RUNS INTO OVERTIME AS NO DEAL LANDS",
     "Negotiators in Antalya push past the deadline with the draft text still open. The presidency says talks will run on into the weekend; no agreement has been reached.",
     "Antalya, T\u00fcrkiye", "Guardian / AP", "Europe", "climate"),
    (2, "RUSSIAN STRIKES KILL 12 AND WOUND 82 IN KRYVYI RIH",
     "Overnight attacks hit the central Ukrainian city, officials say, as rescue teams search the rubble and hospitals treat the wounded.",
     "Kryvyi Rih, Ukraine", "AP", "Europe", "war"),
    (3, "COURT APPROVES $7.25B BAYER ROUNDUP SETTLEMENT",
     "A judge signs off on the multi-billion-dollar deal to resolve Roundup claims, one of the largest settlements of its kind.",
     "Global", "AP", "Global", "money"),
]

# (number, headline, place, source, region, scene, lon, lat)
CARDS = [
    (4, "HIMARS HIT WIPES OUT 20 RUSSIAN COMMANDERS",
     "Sumy, Ukraine", "Reports", "Europe", "strike", 34.8, 50.9),
    (5, "INDIA LAUNCHES FIRST H3N1 VACCINE",
     "New Delhi, India", "PR", "Asia", "health", 77.2, 28.6),
    (6, "CALIFORNIA SUBPOENAS NVIDIA",
     "California, US", "Reuters", "Americas", "chip", -121.5, 38.5),
    (7, "TAKAICHI GETS FROSTY APEC GREETING",
     "Tokyo, Japan", "Asahi", "Asia", "summit", 139.7, 35.7),
    (8, "COALITION DESTROYS SIX HOUTHI WORKSHOPS",
     "Sana'a, Yemen", "Alliance", "Middle East", "strike", 44.2, 15.4),
    (9, "MEASLES COSTS US ITS ELIMINATION STATUS",
     "Atlanta, US", "Health officials", "Americas", "health", -84.4, 33.7),
    (10, "AUSTRALIA v ENGLAND OPEN T20 SERIES AT THE MCG",
     "Melbourne, Australia", "Tonight", "Oceania", "sport", 145.0, -37.8),
    (11, "ANC SCRAMBLES AFTER WORST RESULT \u2014 31% VOTE SHARE",
     "Johannesburg, South Africa", "Reports", "Africa", "politics", 28.0, -26.2),
    (12, "JAPAN TO BUY UP TO 8M BARRELS OF SAUDI CRUDE",
     "Tokyo, Japan", "Energy", "Asia", "energy", 46.7, 24.7),
    (13, "BRAZIL ADVANCES INDIGENOUS LAND BILL",
     "Brasilia, Brazil", "Reports", "Americas", "land", -47.9, -15.8),
]

# (number, one-liner, place, source, region)
ONELINERS = [
    (14, "Britain hits Moscow with cyberattacks", "London", "UK", "Europe"),
    (15, "\u201cCoalition of the willing\u201d meets on Ukraine with Zelenskyy", "Berlin", "Reports", "Europe"),
    (16, "Students march against rearmament and mandatory service", "Berlin", "Reports", "Europe"),
    (17, "Montenegro rejects land concessions to Croatia in EU bid row", "Podgorica", "Reports", "Europe"),
    (18, "Russian missile lands in Poland", "Eastern Poland", "Security", "Europe"),
    (19, "NATO chief takes Poland\u2019s airspace case to Warsaw", "Warsaw", "Security", "Europe"),
    (20, "Modi opens SCO dialogue forum", "New Delhi", "PR", "Asia"),
    (21, "Jakarta asks Google: why 19,000 accounts gone?", "Jakarta", "Ministry", "Asia"),
    (22, "China warns on climbing Mount Fuji; family offers reward", "Tokyo", "Reports", "Asia"),
    (23, "Manipur\u2019s capital counts 11 dead as violence spreads", "Imphal", "Reports", "Asia"),
    (24, "Mumbai: IndusInd ends ex-CEO\u2019s job, seeks to recover his pay", "Mumbai", "Reports", "Asia"),
    (25, "Nepal\u2019s new leader faces India test", "Kathmandu", "Politics", "Asia"),
    (26, "Iran claims waters 500 km beyond the strait", "Strait of Hormuz", "IRGC", "Middle East"),
    (27, "Iran crews a tanker convoy to test the US blockade", "Kharg Island", "Energy", "Middle East"),
    (28, "Pipeline chief arrested over illicit oil trading accusations", "Baghdad", "Reports", "Middle East"),
    (29, "US engagement against Iran has cost $48.3B, Pentagon says", "Washington", "Pentagon", "Middle East"),
    (30, "Trump: Iran wants a deal", "Washington", "AP", "Americas"),
    (31, "Jury convicts man who started deadly 2025 Palisades Fire", "Los Angeles", "AP", "Americas"),
    (32, "AP fact-checks false claims at Trump\u2019s post-Asia news conference", "Washington", "AP", "Americas"),
    (33, "Second judge blocks Trump\u2019s triumphal arch", "Washington", "Court", "Americas"),
    (34, "Caravan of about 500 migrants crosses into Mexico", "Southern Mexico", "Reports", "Americas"),
    (35, "Murder rate falls, but homicides still average 60 a day", "Johannesburg", "Stats", "Africa"),
]

NUMBERS = [
    ("12", "killed in Russian strikes on Kryvyi Rih"),
    ("900,000", "AI chips cleared by the US for China"),
    ("$7.25B", "Bayer Roundup settlement approved"),
    ("19,000", "Google accounts queried in Jakarta"),
    ("20", "Russian commanders hit in Sumy"),
    ("8m", "barrels of Saudi crude for Japan"),
]

REGIONS = [("Europe", 9), ("Asia", 9), ("Middle East", 5),
           ("Africa", 2), ("Americas", 8), ("Oceania", 1), ("Global", 1)]

EXCLUDED = [
    "Kyiv bridges hit (20 Nov)",
    "KCI ruling on the Myanmar genocide case (20 Nov)",
    "Trump\u2013Xi summit in Shenzhen (20 Nov)",
    "COP31 Friday closing session (20 Nov)",
    "Senate 62\u201333 permitting vote (20 Nov)",
    "Anthropic $81.3B IPO (19 Nov)",
    "Mexico Revolution Day parade (20 Nov)",
    "GTA VI first-day sales (20 Nov)",
]

MAP_PINS = [(1, 30.7, 36.9), (2, 33.4, 47.9)] + [
    (n, lon, lat) for (n, _h, _p, _s, _r, _sc, lon, lat) in CARDS]

# sanity: region counts must sum to the story total
assert sum(c for _r, c in REGIONS) == 35
assert len(LEADS) + len(CARDS) + len(ONELINERS) == 35
assert [n for n, *_ in LEADS + CARDS + ONELINERS] == list(range(1, 36))


# ---------------------------------------------------------------- scenes
def scene(draw, box, kind):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "climate":
        draw.rectangle(box, fill=(198, 226, 214))
        draw.ellipse([x0 + w * 0.68, y0 + h * 0.08, x0 + w * 0.92, y0 + h * 0.42],
                     fill=(240, 180, 60))
        draw.rectangle([x0 + w * 0.10, y0 + h * 0.55, x0 + w * 0.42, y0 + h * 0.92],
                       fill=(90, 110, 120))
        draw.rectangle([x0 + w * 0.46, y0 + h * 0.68, x0 + w * 0.60, y0 + h * 0.92],
                       fill=(70, 88, 100))
        draw.polygon([(x0 + w * 0.62, y0 + h * 0.92), (x0 + w * 0.78, y0 + h * 0.45),
                      (x0 + w * 0.94, y0 + h * 0.92)], fill=(34, 139, 92))
        draw.polygon([(x0 + w * 0.70, y0 + h * 0.92), (x0 + w * 0.78, y0 + h * 0.62),
                      (x0 + w * 0.86, y0 + h * 0.92)], fill=(247, 242, 231))
    elif kind == "war":
        draw.rectangle(box, fill=(226, 214, 196))
        for i, r in enumerate([150, 105, 62]):
            draw.ellipse([cx - r, cy - 20 - r // 2, cx + r, cy - 20 + r // 2],
                         fill=[(240, 160, 60), (220, 90, 40), (180, 35, 24)][i])
        draw.rectangle([x0 + w * 0.08, y0 + h * 0.78, x0 + w * 0.92, y0 + h * 0.92],
                       fill=(70, 70, 78))
        for bx in (0.14, 0.38, 0.62, 0.82):
            draw.rectangle([x0 + w * bx, y0 + h * 0.62, x0 + w * (bx + 0.10),
                            y0 + h * 0.78], fill=(50, 50, 58))
    elif kind == "money":
        draw.rectangle(box, fill=(214, 230, 214))
        for i, dx in enumerate((-70, 0, 70)):
            draw.ellipse([cx + dx - 52, cy - 52, cx + dx + 52, cy + 52],
                         fill=(212, 175, 55), outline=(150, 120, 30), width=4)
            draw.text((cx + dx - 14, cy - 26), "$", font=font(SANS_B, 52),
                      fill=(120, 95, 20))
        draw.rectangle([x0, y1 - 26, x1, y1], fill=(34, 139, 92))
    elif kind == "health":
        draw.rectangle(box, fill=(206, 226, 240))
        draw.polygon([(x0 + w * 0.30, y0 + h * 0.30), (x0 + w * 0.62, y0 + h * 0.30),
                      (x0 + w * 0.62, y0 + h * 0.55), (x0 + w * 0.78, y0 + h * 0.55),
                      (x0 + w * 0.78, y0 + h * 0.68), (x0 + w * 0.62, y0 + h * 0.68),
                      (x0 + w * 0.62, y0 + h * 0.92), (x0 + w * 0.30, y0 + h * 0.92),
                      (x0 + w * 0.30, y0 + h * 0.68), (x0 + w * 0.14, y0 + h * 0.68),
                      (x0 + w * 0.14, y0 + h * 0.55), (x0 + w * 0.30, y0 + h * 0.55)],
                     fill=(255, 255, 255), outline=(18, 110, 105))
        draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(18, 110, 105))
        draw.text((cx - 12, cy - 26), "+", font=font(SANS_B, 52), fill=(255, 255, 255))
    elif kind == "chip":
        draw.rectangle(box, fill=(30, 40, 66))
        draw.rectangle([cx - 70, cy - 70, cx + 70, cy + 70], fill=(60, 90, 140),
                       outline=(140, 180, 220), width=4)
        draw.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(214, 230, 238))
        for k in range(-1, 2):
            for xx in (cx - 70, cx + 70):
                draw.line([xx, cy + k * 40, xx + (-22 if xx < cx else 22), cy + k * 40],
                          fill=(140, 180, 220), width=6)
            for yy in (cy - 70, cy + 70):
                draw.line([cx + k * 40, yy, cx + k * 40, yy + (-22 if yy < cy else 22)],
                          fill=(140, 180, 220), width=6)
    elif kind == "summit":
        draw.rectangle(box, fill=(226, 214, 196))
        for i, dx in enumerate((-90, 0, 90)):
            draw.ellipse([cx + dx - 34, cy - 60, cx + dx + 34, cy + 8],
                         fill=(240, 200, 140))
            draw.polygon([(cx + dx - 52, y1 - 10), (cx + dx + 52, y1 - 10),
                          (cx + dx + 26, cy + 8), (cx + dx - 26, cy + 8)],
                         fill=[(20, 33, 61), (180, 35, 24), (18, 110, 105)][i])
        draw.rectangle([x0 + w * 0.30, y0 + h * 0.30, x0 + w * 0.70, y0 + h * 0.36],
                       fill=(176, 132, 52))
    elif kind == "strike":
        draw.rectangle(box, fill=(240, 214, 180))
        draw.polygon([(cx, cy - 80), (cx + 26, cy - 26), (cx + 84, cy - 26),
                      (cx + 40, cy + 10), (cx + 58, cy + 70), (cx, cy + 34),
                      (cx - 58, cy + 70), (cx - 40, cy + 10), (cx - 84, cy - 26),
                      (cx - 26, cy - 26)], fill=(240, 160, 60),
                     outline=(180, 35, 24))
        draw.rectangle([x0 + w * 0.10, y0 + h * 0.82, x0 + w * 0.90, y0 + h * 0.92],
                       fill=(90, 70, 50))
    elif kind == "sport":
        draw.rectangle(box, fill=(198, 226, 190))
        draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=(255, 255, 255),
                     outline=(180, 35, 24), width=5)
        draw.arc([cx - 62, cy - 62, cx + 62, cy + 62], 200, 340, fill=(180, 35, 24), width=5)
        draw.rectangle([x0 + w * 0.12, y0 + h * 0.78, x0 + w * 0.88, y0 + h * 0.86],
                       fill=(34, 139, 92))
    elif kind == "politics":
        draw.rectangle(box, fill=(214, 220, 238))
        for i, ht in enumerate((90, 60, 120, 75)):
            x = x0 + w * (0.14 + i * 0.20)
            draw.rectangle([x, y1 - 30 - ht, x + w * 0.14, y1 - 30],
                           fill=[(20, 33, 61), (180, 35, 24), (18, 110, 105),
                                 (176, 132, 52)][i])
        draw.line([x0 + w * 0.08, y1 - 30, x1 - w * 0.08, y1 - 30], fill=INK, width=4)
    elif kind == "energy":
        draw.rectangle(box, fill=(30, 40, 66))
        draw.ellipse([cx - 70, cy - 46, cx + 70, cy + 46], fill=(240, 180, 60))
        draw.rectangle([cx - 14, cy - 46, cx + 14, cy + 46], fill=(30, 40, 66))
        draw.polygon([(x0 + w * 0.10, y1 - 24), (x0 + w * 0.30, y0 + h * 0.30),
                      (x0 + w * 0.44, y1 - 24)], fill=(120, 140, 160))
        draw.polygon([(x0 + w * 0.56, y1 - 24), (x0 + w * 0.72, y0 + h * 0.45),
                      (x0 + w * 0.90, y1 - 24)], fill=(90, 110, 130))
    elif kind == "land":
        draw.rectangle(box, fill=(198, 226, 190))
        draw.polygon([(x0 + w * 0.15, y1 - 20), (x0 + w * 0.30, y0 + h * 0.30),
                      (x0 + w * 0.55, y0 + h * 0.20), (x0 + w * 0.85, y0 + h * 0.45),
                      (x0 + w * 0.80, y1 - 20)], fill=(34, 139, 92))
        draw.ellipse([x0 + w * 0.60, y0 + h * 0.12, x0 + w * 0.74, y0 + h * 0.30],
                     fill=(240, 180, 60))


# ---------------------------------------------------------------- map
CONTINENTS = [  # (lon centre, lat centre, lon radius, lat radius)
    (-100, 45, 34, 19), (-60, -12, 17, 23), (15, 52, 19, 9),
    (20, 4, 19, 24), (90, 45, 48, 23), (134, -27, 14, 12),
    (105, -2, 12, 7), (78, 21, 12, 10),
]


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 240, 244), outline=INK, width=2)

    def to_xy(lon, lat):
        return (x0 + (lon + 180) / 360 * (x1 - x0),
                y0 + (90 - lat) / 180 * (y1 - y0))

    lon = -180
    while lon <= 180:
        lat = -60
        while lat <= 84:
            for (clon, clat, rx, ry) in CONTINENTS:
                if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                    px, py = to_xy(lon, lat)
                    draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(140, 165, 175))
                    break
            lat += 4
        lon += 4
    for (n, lon, lat) in MAP_PINS:
        px, py = to_xy(lon, lat)
        ox, oy = {2: (0, -30), 4: (34, -12)}.get(n, (0, 0))
        if (ox, oy) != (0, 0):
            draw.line([px, py, px + ox, py + oy], fill=RED, width=2)
            px, py = px + ox, py + oy
        draw.ellipse([px - 15, py - 15, px + 15, py + 15], fill=RED,
                     outline=(255, 255, 255), width=2)
        t = str(n)
        tw = draw.textlength(t, font=font(SANS_B, 17))
        draw.text((px - tw / 2, py - 12), t, font=font(SANS_B, 17), fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 56  # margin
    y = 34

    # top rule line
    d.text((M, y), "SATURDAY EDITION", font=font(SANS_B, 26), fill=INK)
    rt = "35 STORIES  \u00b7  7 REGIONS  \u00b7  ALL DATED 21 NOVEMBER 2026"
    d.text((W - M - d.textlength(rt, font=font(SANS_B, 26)), y), rt,
           font=font(SANS_B, 26), fill=INK)
    y += 44
    d.line([M, y, W - M, y], fill=INK, width=4)
    y += 26

    # masthead (auto-fit to the page width)
    def fit_font(path, size, text, max_w):
        while size > 14 and ImageDraw.Draw(img).textlength(text, font=font(path, size)) > max_w:
            size -= 2
        return font(path, size)
    y = centre(d, y, "THE WORLD IN ONE DAY",
               fit_font(SERIF_B, 108, "THE WORLD IN ONE DAY", W - 2 * M), INK) + 6
    y = centre(d, y, "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
               font(SANS_B, 27), RED) + 4
    d.line([M, y, W - M, y], fill=GOLD, width=3)
    y += 18

    # giant date
    y = centre(d, y, "Saturday 21 November 2026", font(SERIF_B, 84), NAVY) + 2
    y = centre(d, y, "The whole planet, in a single day \u2014 read it in one image.",
               font(SERIF, 30), GREY) + 6
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 16

    # headline strip
    strip = ("COP31 OVERTIME  \u00b7  STRIKES KILL 12 IN KRYVYI RIH  \u00b7  "
             "BAYER $7.25B SETTLEMENT APPROVED")
    y = centre(d, y, strip, fit_font(SANS_B, 28, strip, W - 2 * M), INK) + 4
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 22

    # 6-number strip
    d.text((M, y), "THE DAY IN NUMBERS", font=font(SANS_B, 24), fill=RED)
    y += 36
    cell_w = (W - 2 * M) // 6
    top = y
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * cell_w
        d.rectangle([x + 4, top, x + cell_w - 4, top + 128], fill=PAPER,
                    outline=LIGHT, width=2)
        nf = fit_font(SERIF_B, 52, num, cell_w - 20)
        nw = d.textlength(num, font=nf)
        d.text((x + cell_w / 2 - nw / 2, top + 12), num, font=nf, fill=NAVY)
        text_block(d, x + 14, top + 74, cap, font(SANS, 19), GREY, cell_w - 28, leading=22)
        if i:
            d.line([x, top + 10, x, top + 118], fill=LIGHT, width=2)
    y = top + 128 + 22

    # region bar
    d.text((M, y), "WHERE THE STORIES COME FROM", font=font(SANS_B, 24), fill=RED)
    y += 36
    total_w = W - 2 * M
    seg_w = total_w // 7
    x = M
    for (name, cnt) in REGIONS:
        d.rectangle([x, y, x + seg_w - 2, y + 62], fill=NAVY if cnt >= 8 else TEAL
                    if cnt >= 5 else GOLD)
        label = f"{name} {cnt}"
        lf = fit_font(SANS_B, 22, label, seg_w - 12)
        tw = d.textlength(label, font=lf)
        d.text((x + (seg_w - 2) / 2 - tw / 2, y + 18), label, font=lf,
               fill=(255, 255, 255))
        x += seg_w
    y += 62 + 10
    d.text((M, y), "Region counts add up to 35 stories.",
           font=font(SANS, 20), fill=GREY)
    y += 34

    # section header helper
    def section(title):
        nonlocal y
        d.line([M, y, W - M, y], fill=INK, width=3)
        y += 12
        d.text((M, y), title, font=font(SERIF_B, 40), fill=INK)
        y += 58

    # 3 big leads
    section("THE THREE BIG STORIES")
    lead_w = (W - 2 * M - 2 * 24) // 3
    lead_h = 560
    top = y
    for i, (n, head, copy, place, src, region, kind) in enumerate(LEADS):
        x = M + i * (lead_w + 24)
        d.rectangle([x, top, x + lead_w, top + lead_h], fill=PAPER, outline=INK, width=2)
        scene(d, (x + 2, top + 2, x + lead_w - 2, top + 232), kind)
        d.ellipse([x + 16, top + 16, x + 56, top + 56], fill=RED)
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 24))
        d.text((x + 36 - tw / 2, top + 20), t, font=font(SANS_B, 24), fill=(255, 255, 255))
        yy = text_block(d, x + 18, top + 248, head, font(SERIF_B, 31), INK,
                        lead_w - 36, leading=38)
        yy = text_block(d, x + 18, yy + 8, copy, font(SANS, 21), GREY,
                        lead_w - 36, leading=27)
        d.text((x + 18, top + lead_h - 34), f"{place}  \u00b7  {src}",
               font=font(SANS_B, 19), fill=RED)
    y = top + lead_h + 30

    # 10 small cards, 5 x 2
    section("TEN MORE STORIES")
    card_w = (W - 2 * M - 4 * 18) // 5
    card_h = 400
    for row in range(2):
        top = y
        for col in range(5):
            idx = row * 5 + col
            n, head, place, src, region, kind, _lon, _lat = CARDS[idx]
            x = M + col * (card_w + 18)
            d.rectangle([x, top, x + card_w, top + card_h], fill=PAPER,
                        outline=INK, width=2)
            scene(d, (x + 2, top + 2, x + card_w - 2, top + 158), kind)
            d.ellipse([x + 12, top + 12, x + 46, top + 46], fill=RED)
            t = str(n)
            tw = d.textlength(t, font=font(SANS_B, 20))
            d.text((x + 29 - tw / 2, top + 15), t, font=font(SANS_B, 20),
                   fill=(255, 255, 255))
            yy = text_block(d, x + 14, top + 172, head, font(SERIF_B, 25), INK,
                            card_w - 28, leading=30)
            pf = fit_font(SANS_B, 18, place, card_w - 28)
            d.text((x + 14, top + card_h - 58), place, font=pf, fill=RED)
            d.text((x + 14, top + card_h - 32), f"Source: {src}",
                   font=font(SANS, 18), fill=GREY)
        y = top + card_h + 22
    y += 8

    # 22 one-liners, 2 columns
    section("ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES")
    col_w = (W - 2 * M - 40) // 2
    top = y
    for i, (n, line, place, src, region) in enumerate(ONELINERS):
        col = i // 11
        r = i % 11
        x = M + col * (col_w + 40)
        yy = top + r * 56
        d.text((x, yy), f"{n}.", font=font(SANS_B, 22), fill=RED)
        text_block(d, x + 48, yy, line, font(SANS, 22), INK, col_w - 48 - 210,
                   leading=26)
        d.text((x + col_w - 200, yy), f"{place} \u00b7 {src}",
               font=font(SANS, 18), fill=GREY)
    y = top + 11 * 56 + 26

    # map
    section("WHERE IT HAPPENED")
    map_top = y
    draw_map(d, (M, map_top, W - M, map_top + 430))
    y = map_top + 430 + 14
    y = text_block(d, M, y,
                   "Numbered dots mark stories 1\u201313 above.  1 Antalya  \u00b7  2 Kryvyi Rih  \u00b7  "
                   "4 Sumy  \u00b7  5 New Delhi  \u00b7  6 California  \u00b7  7 Tokyo  \u00b7  "
                   "8 Sana'a  \u00b7  9 Atlanta  \u00b7  10 Melbourne  \u00b7  11 Johannesburg  \u00b7  "
                   "12 Riyadh  \u00b7  13 Brasilia",
                   font(SANS, 19), GREY, W - 2 * M, leading=24)
    y += 12

    # date check
    section("DATE CHECK \u2014 WHAT WE LEFT OUT")
    box_top = y
    lines = ["Every story above happened, or was first reported, on Saturday 21 November 2026.",
             "These real stories are from 20 November or earlier, so they are NOT counted here:"]
    yy = box_top + 16
    for ln in lines:
        d.text((M + 20, yy), ln, font=font(SANS, 22), fill=INK)
        yy += 30
    for item in EXCLUDED:
        d.text((M + 20, yy), "\u2022  " + item, font=font(SANS, 22), fill=GREY)
        yy += 30
    box_h = yy - box_top + 16
    d.rectangle([M, box_top, W - M, box_top + box_h], outline=RED, width=3)
    # redraw text over the border (text was drawn first, border after is fine)
    y = box_top + box_h + 26

    # footer
    d.line([M, y, W - M, y], fill=INK, width=3)
    y += 14
    y = centre(d, y, "Every story here happened, or was first reported, on Saturday 21 November 2026.",
               font(SERIF, 26), INK)
    y = centre(d, y, "Sources named beside each story  \u00b7  Drawn illustrations, not photographs  \u00b7  35 stories, 7 regions",
               font(SANS, 22), GREY)
    y += 10
    assert y < H, f"layout overflow: y={y} > H={H}"
    img = img.crop((0, 0, W, y + 30))
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
