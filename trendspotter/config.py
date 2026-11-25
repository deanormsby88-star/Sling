"""Settings for the Just Imagine trendspotter.

Everything here comes from the research brief "Just Imagine Trendspotter: Daily
Source Map for Ages 5-9 Toy Trends (South Africa)". Edit this file to change the
watchlist, sources, weights or calendar. The weekly run reads it each Friday.
"""

REPORT_NAME = "Just Imagine Trendspotter"

# Client PDF defaults (build.py client-pdf). Logos live in brand/.
CLIENT_NAME = "Wimpy"
CLIENT_LOGO = "brand/client-logo.png"
JI_LOGO = "brand/just-imagine-consulting.jpg"

# The weekly run (Friday) covers Tier 1 and Tier 2 sources in one pass.
# The first Friday of each month also covers the monthly sources.
MAX_NEW_CANDIDATES = 10

# ---------------------------------------------------------------------------
# Seed watchlist. The weekly run re-scores these and adds new candidates.
# ip: "generic" (sourceable from factories), "licensed" (only via licence or
# licensed distributor), "proprietary" (no legitimate route; lookalikes = red flag)
# ---------------------------------------------------------------------------
SEED_WATCHLIST = [
    {"name": "Squishy / sensory squeeze toys", "aliases": ["NeeDoh", "Nee Doh", "squishy cube", "squishies"], "ip": "generic"},
    {"name": "Fidget and tactile toys", "aliases": ["fidget", "pop it", "sensory toys"], "ip": "generic"},
    {"name": "Bag-charm plush and keychains", "aliases": ["plush clip", "bag charm", "keychain plush"], "ip": "generic"},
    {"name": "Blind-box minis (generic)", "aliases": ["blind box", "mystery minis", "surprise capsule"], "ip": "generic"},
    {"name": "Slime and creative kits", "aliases": ["slime kit", "craft kit", "Gui Gui slime"], "ip": "generic"},
    {"name": "STEM / inspiring-inventor toys", "aliases": ["STEM kit", "science kit", "coding toy"], "ip": "generic"},
    {"name": "Throwback 2000s toys", "aliases": ["Y2K toys", "retro toys", "Tamagotchi-style"], "ip": "generic"},
    {"name": "KPop Demon Hunters", "aliases": ["Huntr/x", "Saja Boys"], "ip": "licensed"},
    {"name": "Stitch (Lilo & Stitch)", "aliases": ["Stitch plush"], "ip": "licensed"},
    {"name": "Pokemon", "aliases": ["Pokémon"], "ip": "licensed"},
    {"name": "Bluey", "aliases": [], "ip": "licensed"},
    {"name": "Minecraft / Roblox", "aliases": ["Minecraft toys", "Roblox toys"], "ip": "licensed"},
    {"name": "MrBeast Lab", "aliases": ["Micro Beast"], "ip": "licensed"},
    {"name": "Labubu / Pop Mart", "aliases": ["Labubu", "Lafufu"], "ip": "proprietary"},
]

TIKTOK_HASHTAGS = ["#toytok", "#toyreview", "#unboxing", "#squishy", "#blindbox", "#fidget"]

# Trigger words to search trade news for.
KEYWORD_TRIGGERS = ["master toy licensee", "sold out", "shortage", "recall", "viral", "waiting list", "restock"]

# ---------------------------------------------------------------------------
# Sources to research each week, by cadence.
# ---------------------------------------------------------------------------
WEB_SOURCES = {
    "weekly": [
        "TikTok Creative Center trending hashtags (US, GB, ZA) and the toy hashtags " + ", ".join(TIKTOK_HASHTAGS),
        "Google Trends rising queries in Toys for ZA, US and GB, plus each watchlist item",
        "Amazon US and UK Toys & Games Movers & Shakers and Hot New Releases (and Amazon.co.za); new entrants and rank jumps above 500%",
        "Takealot toy best sellers and 'What's Hot'; new entrants and price points",
        "YouTube kids' toy review, unboxing and 'hunting' channels: top new uploads and the products named",
        "Trade news: The Toy Book, Toy World, Toy News, License Global, Kidscreen, Toys n Playthings; search for: " + ", ".join(KEYWORD_TRIGGERS),
        "Walmart, Target, Smyths, Argos and Hamleys bestsellers; Toys R Us SA, Toy Kingdom, PEP/Ackermans new-in pages",
        "Temu, AliExpress and 1688 for each watchlist item: number of copies, price floor, MOQ",
        "Reddit (r/toys, r/Parenting, r/Mommit, r/daddit, r/needoh) and parent communities: 'where can I find X?', school fads, safety complaints",
        "Safety and recall sweep: US CPSC, UK OPSS / Trading Standards, EU Safety Gate",
        "Netflix Top 10 (kids), Disney+ and cinema release slate for the next 12 months; licensing deal round-up",
        "SA market: Durban port and China-SA freight rates, ZAR exchange rate, SA toy retail news",
    ],
    "monthly": [
        "Circana releases (US, UK, G12) and Toy Association industry reports",
        "Pop Mart, Mattel, Hasbro, Spin Master, Schylling, Moose, Zuru investor updates",
        "Trade-fair and award calendar news (Spielwarenmesse, HK Toys & Games Fair, Toy Fair NY, Canton Fair, Brand Licensing Europe, Licensing Expo, DreamToys, US holiday lists)",
        "SA market data: Euromonitor, SATAGA, BusinessDay / BusinessTech retail coverage",
    ],
}

# ---------------------------------------------------------------------------
# Scoring framework (weights total 100). Each factor is scored 0-5.
# ---------------------------------------------------------------------------
WEIGHTS = {
    "velocity": 20,
    "cross_platform": 20,
    "age_fit": 15,
    "sourcing": 15,
    "runway": 10,
    "margin": 10,
    "longevity": 10,
}
FACTOR_LABELS = {
    "velocity": "Velocity",
    "cross_platform": "Cross-platform",
    "age_fit": "5-9 fit",
    "sourcing": "Sourcing and IP",
    "runway": "SA runway",
    "margin": "Margin",
    "longevity": "Longevity",
}
BANDS = [(75, "ACT"), (55, "PREPARE"), (35, "WATCH"), (0, "IGNORE")]
MIN_MONTHS_TO_SA_PEAK_FOR_ACT = 4  # import runway rule: 10-16 weeks
RISING_THRESHOLD = 10  # points up since last week's report
RETIRE_AFTER_DAYS = 30  # monthly clean-up of trends no longer seen

# ---------------------------------------------------------------------------
# Calendar: SA seasonality, retail events and trade fairs.
# (month, day) is a fixed date; day=None means "during this month".
# ---------------------------------------------------------------------------
CALENDAR = [
    ((1, None), "SA back to school", "Stationery-toys, fidgets, lunchbox collectibles. Should have been flagged Aug-Sep."),
    ((1, None), "Hong Kong Toys & Games Fair", "See what factories are tooling up for; MOQ and price discovery."),
    ((1, None), "Spielwarenmesse Nuremberg (late January)", "European range themes."),
    ((1, None), "Circana Global Toy Industry Performance Awards", "Confirms last year's winners by region."),
    ((2, None), "Toy Fair New York + Toy Association trends briefing", "Year's themes; confirmation, not discovery."),
    ((4, None), "Canton Fair (April phases)", "Factory readiness and copy speed."),
    ((5, None), "Toy Association / ICTI Global Toy Trends presentation", ""),
    ((5, 31), "Freeze the Christmas watchlist", "Brief recommendation 5: watchlist frozen by end of May, orders June-July."),
    ((6, None), "Christmas orders: place by June-July", "Ship by August at the latest, before Durban's Aug-Nov congestion."),
    ((6, None), "SA winter school holidays (Jun-Jul)", "Indoor play, crafts, games. Should have been flagged Jan-Feb."),
    ((6, None), "Licensing Expo (Las Vegas)", "Licensing deal announcements."),
    ((8, None), "Durban peak congestion begins (Aug-Nov)", "Add 3-10 days to transit."),
    ((8, None), "Flag back-to-school lines for next January", ""),
    ((10, None), "Spielwarenmesse ToyTrends announced", ""),
    ((10, None), "Canton Fair (October phases)", ""),
    ((10, None), "Brand Licensing Europe (London)", ""),
    ((10, 31), "Blue Dot Sale / Black Friday stock must be in SA", ""),
    ((11, None), "UK DreamToys list and US holiday lists", "What retailers bet on for Christmas; good for SA's next season."),
    ((11, None), "Takealot Blue Dot Sale / Black Friday", ""),
    ((11, None), "Flag Easter lines (squishies, small collectibles)", ""),
    ((12, 25), "Christmas (SA summer: outdoor, water, ride-ons)", ""),
]
