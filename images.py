"""
ALL image references for the website live in this one file.

Each entry maps a name (used in data.py and the templates) to an image source.
A source can be:

  "photo-1464822759023-fed622ff2c3b"   an Unsplash photo ID (resized automatically)
  "treks/rajmachi-1.jpg"               a file inside static/img/
  "https://example.com/pic.jpg"        any full URL
  "mist"                               another name in this file (an alias)

To use your own photos: copy them into static/img/ (e.g. static/img/treks/)
and change the value here. Nothing else in the code needs to change.

In templates use:  {{ img('header_about', 1920) }}
In Python use:     from images import img; img('mist', 800)
The width only applies to Unsplash images; local files are served as they are.
"""

IMAGES = {
    # ------------------------------------------------------------------ Photo pool
    # Generic outdoor photos reused across the site.
    "peaks": "photo-1464822759023-fed622ff2c3b",
    "range": "photo-1506905925346-21bda4d32df4",
    "lake": "photo-1501785888041-af3ef285b470",
    "snow": "photo-1454496522488-7a8e488e8606",
    "stars": "photo-1519681393784-d120267933ba",
    "hikers": "photo-1551632811-561732d1e306",
    "valley": "photo-1500530855697-b586d89ba3ee",
    "waterfall": "photo-1432405972618-c60b0225b8f9",
    "mist": "photo-1470071459604-3b5ec3a7fe05",
    "ridge": "photo-1486870591958-9b9d0d1dda99",
    "alps": "photo-1483728642387-6c3bdd6c93e5",
    "climber": "photo-1522163182402-834f871fd851",
    "camp": "photo-1478131143081-80f7f84ca84d",
    "tent": "photo-1504280390367-361c6d9f38f4",
    "campfire": "photo-1445308394109-4ec2920981b1",
    "forest": "photo-1441974231531-c6227db76b6e",
    "green": "photo-1472214103451-9374bd1c798e",
    "trail": "photo-1501554728187-ce583db33af7",

    # ------------------------------------------------------------------ Homepage hero slider
    "hero_1": "range",
    "hero_2": "waterfall",
    "hero_3": "campfire",
    "monsoon_banner": "waterfall",

    # ------------------------------------------------------------------ Page header banners
    "header_about": "hikers",
    "header_tours": "range",
    "header_gallery": "stars",
    "header_contact": "lake",

    # ------------------------------------------------------------------ About page
    "about_1": "mist",
    "about_2": "camp",

    # ------------------------------------------------------------------ Trek categories
    "cat_sahyadri": "mist",
    "cat_himalayan": "snow",
    "cat_adventure": "climber",
    "cat_groups": "campfire",

    # ------------------------------------------------------------------ Team photos
    "team_1": "photo-1507003211169-0a1dd7228f2d",
    "team_2": "photo-1494790108377-be9c29b29330",
    "team_3": "photo-1500648767791-00dcc994a43e",
    "team_4": "photo-1438761681033-6461ffad8d80",

    # ------------------------------------------------------------------ Trek photos (first = cover)
    "rajmachi_1": "mist", "rajmachi_2": "green", "rajmachi_3": "trail", "rajmachi_4": "forest",
    "kalsubai_1": "stars", "kalsubai_2": "ridge", "kalsubai_3": "range", "kalsubai_4": "peaks",
    "harishchandragad_1": "ridge", "harishchandragad_2": "mist", "harishchandragad_3": "camp", "harishchandragad_4": "valley",
    "devkund_1": "waterfall", "devkund_2": "forest", "devkund_3": "green", "devkund_4": "trail",
    "kalu_1": "waterfall", "kalu_2": "mist", "kalu_3": "forest", "kalu_4": "green",
    "andharban_1": "forest", "andharban_2": "mist", "andharban_3": "waterfall", "andharban_4": "green",
    "hampta_1": "valley", "hampta_2": "snow", "hampta_3": "camp", "hampta_4": "alps",
    "kedarkantha_1": "snow", "kedarkantha_2": "alps", "kedarkantha_3": "tent", "kedarkantha_4": "peaks",
    "harkidun_1": "snow", "harkidun_2": "valley", "harkidun_3": "forest", "harkidun_4": "camp",
    # Har Ki Dun day-by-day itinerary photos
    "harkidun_day1": "forest", "harkidun_day2": "trail", "harkidun_day3": "green", "harkidun_day4": "snow",
    "harkidun_day5": "valley", "harkidun_day6": "tent", "harkidun_day7": "range",
    "ebc_1": "alps", "ebc_2": "snow", "ebc_3": "peaks", "ebc_4": "range",
    "spiti_1": "valley", "spiti_2": "lake", "spiti_3": "range", "spiti_4": "tent",
    "yunam_1": "climber", "yunam_2": "snow", "yunam_3": "alps", "yunam_4": "stars",
    "kolad_1": "campfire", "kolad_2": "tent", "kolad_3": "hikers", "kolad_4": "green",
    "corporate_1": "hikers", "corporate_2": "camp", "corporate_3": "campfire", "corporate_4": "mist",

    # ------------------------------------------------------------------ Gallery page
    "gallery_1": "mist", "gallery_2": "waterfall", "gallery_3": "snow", "gallery_4": "stars",
    "gallery_5": "camp", "gallery_6": "alps", "gallery_7": "forest", "gallery_8": "campfire",
    "gallery_9": "valley", "gallery_10": "green", "gallery_11": "tent", "gallery_12": "ridge",

    # ------------------------------------------------------------------ Video thumbnails
    "video_1": "mist",
    "video_2": "valley",
    "video_3": "alps",
}

UNSPLASH_URL = "https://images.unsplash.com/{id}?auto=format&fit=crop&w={w}&q=70"
STATIC_PREFIX = "/static/img/"


def resolve(name):
    """Follow aliases until we reach a real source (max 10 hops to avoid loops)."""
    src = name
    for _ in range(10):
        if src not in IMAGES:
            break
        src = IMAGES[src]
    return src


def img(name, w=1200):
    """Return a ready-to-use URL for an image name from IMAGES."""
    src = resolve(name)
    if src.startswith("photo-"):
        return UNSPLASH_URL.format(id=src, w=w)
    if src.startswith(("http://", "https://", "/")):
        return src
    return STATIC_PREFIX + src
