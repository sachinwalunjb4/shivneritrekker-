"""
Static content for the site: treks, categories, team, gallery and videos.

Everything here is plain Python data so it is easy to edit. When you outgrow
it, move it into a database (SQLite / PostgreSQL) and keep the same shape.
"""
import re
from datetime import date, timedelta

# Image names refer to entries in images.py – edit images there.

CATEGORIES = [
    {
        "slug": "sahyadri",
        "name": "Sahyadri Treks",
        "blurb": "Forts, ridges and monsoon trails across the Western Ghats.",
        "icon": "fa-mountain-sun",
        "image": "cat_sahyadri",
    },
    {
        "slug": "himalayan",
        "name": "Himalayan Treks",
        "blurb": "Classic high-mountain trails in India and Nepal.",
        "icon": "fa-mountain",
        "image": "cat_himalayan",
    },
    {
        "slug": "adventure",
        "name": "Backpacking & Expeditions",
        "blurb": "Multi-day backpacking trips and high-altitude summit climbs.",
        "icon": "fa-person-hiking",
        "image": "cat_adventure",
    },
    {
        "slug": "groups",
        "name": "School, Family & Corporate",
        "blurb": "School and family treks, summer camps and team offsites.",
        "icon": "fa-people-group",
        "image": "cat_groups",
    },
]
CATEGORY_MAP = {c["slug"]: c for c in CATEGORIES}

# Filters used by the "Treks by Location" section and the tours page.
LOCATION_FILTERS = [
    {"slug": "mumbai-pune", "name": "Treks from Mumbai & Pune", "icon": "fa-location-dot"},
    {"slug": "waterfall", "name": "Waterfall Treks", "icon": "fa-water"},
    {"slug": "monsoon", "name": "One-Day Monsoon Treks", "icon": "fa-cloud-rain"},
]

DIFFICULTY_LEVEL = {"Easy": 1, "Moderate": 2, "Difficult": 3, "Challenging": 4}

STANDARD_INCLUSIONS = [
    "Certified trek leader and local guides",
    "First-aid kit and basic safety equipment",
    "Forest/entry permits where applicable",
]
STANDARD_EXCLUSIONS = [
    "Personal expenses and tips",
    "Anything not mentioned under inclusions",
    "Travel insurance",
]


TREKS = [
    # ---------------------------------------------------------------- Sahyadri
    {
        "slug": "rajmachi-fort-trek",
        "name": "Rajmachi Fort Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune", "monsoon", "trending", "one-day"],
        "region": "Lonavala, Maharashtra",
        "start_point": "Lonavala railway station",
        "duration_days": 1,
        "duration": "1 Day",
        "difficulty": "Easy",
        "altitude": "2,710 ft",
        "price": 1499,
        "rating": 4.8,
        "season_months": [6, 7, 8, 9, 10, 11, 12, 1, 2],
        "weekday": 6,  # Sunday
        "images": ["rajmachi_1", "rajmachi_2", "rajmachi_3", "rajmachi_4"],
        "summary": "Twin forts, misty plateaus and seasonal waterfalls on a beginner-friendly trail.",
        "overview": (
            "Rajmachi is one of the most loved treks near Mumbai and Pune. The trail from "
            "Lonavala winds through lush forest and open plateau to the twin forts of "
            "Shrivardhan and Manaranjan, with views over the Ulhas valley. In the monsoon "
            "the whole route turns green and dozens of small waterfalls appear along the way."
        ),
        "highlights": [
            "Twin forts of Shrivardhan and Manaranjan",
            "Kondane Buddhist rock-cut caves nearby",
            "Fireflies in the pre-monsoon season",
            "Ideal first trek for beginners",
        ],
        "itinerary": [
            {"title": "Meet at Lonavala, start the trek", "desc": "Meet at 7:00 AM at Lonavala station, breakfast, briefing and start of the 15 km trail through Tungarli and the forest belt."},
            {"title": "Explore the forts", "desc": "Reach Udhewadi village by noon. Lunch in a village home, then climb and explore both forts with the trek leader."},
            {"title": "Descend and return", "desc": "Descend to the base by 5:00 PM and travel back to Lonavala station by 7:00 PM."},
        ],
        "inclusions": ["Breakfast and veg lunch", "Local transport from Lonavala"] + STANDARD_INCLUSIONS,
        "exclusions": ["Train travel to Lonavala"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "kalsubai-peak-trek",
        "name": "Kalsubai Peak Night Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune", "trending"],
        "region": "Igatpuri, Maharashtra",
        "start_point": "Bari village (pick-up from Kasara)",
        "duration_days": 1,
        "duration": "1 Night",
        "difficulty": "Moderate",
        "altitude": "5,400 ft",
        "price": 1199,
        "rating": 4.7,
        "season_months": list(range(1, 13)),
        "weekday": 5,  # Saturday
        "images": ["kalsubai_1", "kalsubai_2", "kalsubai_3", "kalsubai_4"],
        "summary": "Watch the sunrise from the highest peak in Maharashtra.",
        "overview": (
            "Kalsubai is the highest summit in the Sahyadri range. This night trek starts "
            "from Bari village and climbs over iron ladders and rocky patches to the summit "
            "temple, reaching in time for sunrise over the Bhandardara reservoir."
        ),
        "highlights": [
            "Highest point in Maharashtra",
            "Sunrise above the clouds",
            "Iron ladders on the final ascent",
            "Views of Bhandardara and Alang-Madan-Kulang",
        ],
        "itinerary": [
            {"title": "Night: travel to Bari village", "desc": "Board the late-night train to Kasara. Our vehicle takes you to Bari village. Tea and briefing at the base."},
            {"title": "Early morning: summit push", "desc": "Start the climb around 2:00 AM with headlamps and reach the summit before sunrise."},
            {"title": "Morning: descent and return", "desc": "Breakfast at the base, then travel back to Kasara by noon."},
        ],
        "inclusions": ["Kasara to Bari return transport", "Tea and breakfast"] + STANDARD_INCLUSIONS,
        "exclusions": ["Train travel to Kasara", "Headlamp (carry your own)"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "harishchandragad-trek",
        "name": "Harishchandragad Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune"],
        "region": "Ahmednagar, Maharashtra",
        "start_point": "Khireshwar village",
        "duration_days": 2,
        "duration": "2 Days / 1 Night",
        "difficulty": "Moderate",
        "altitude": "4,670 ft",
        "price": 2799,
        "rating": 4.9,
        "season_months": [6, 7, 8, 9, 10, 11, 12, 1, 2, 3],
        "weekday": 5,
        "images": ["harishchandragad_1", "harishchandragad_2", "harishchandragad_3", "harishchandragad_4"],
        "summary": "The famous Konkan Kada cliff, ancient temples and an overnight camp.",
        "overview": (
            "Harishchandragad is a classic Sahyadri weekend trek. From Khireshwar the "
            "Tolar Khind route leads to the 6th-century Harishchandreshwar temple, the "
            "Kedareshwar cave and the curved Konkan Kada cliff, known for its sunsets and "
            "rare Indian Brocken spectre sightings."
        ),
        "highlights": [
            "Konkan Kada, a sheer concave cliff",
            "Kedareshwar cave with its Shiva linga in water",
            "Camping under the stars",
            "Taramati peak sunrise",
        ],
        "itinerary": [
            {"title": "Day 1: Khireshwar to the plateau", "desc": "Reach Khireshwar by 9:00 AM. Trek through Tolar Khind to the top (4–5 hrs). Visit the temple and caves, then sunset at Konkan Kada. Dinner and camp."},
            {"title": "Day 2: Taramati sunrise and descent", "desc": "Early hike to Taramati peak for sunrise, breakfast, then descend to Khireshwar and head home by evening."},
        ],
        "inclusions": ["Return transport from Mumbai/Pune", "4 meals (Day 1 lunch to Day 2 breakfast)", "Tents and sleeping mats"] + STANDARD_INCLUSIONS,
        "exclusions": STANDARD_EXCLUSIONS,
    },
    {
        "slug": "devkund-waterfall-trek",
        "name": "Devkund Waterfall Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune", "waterfall", "monsoon", "trending", "one-day"],
        "region": "Bhira, Raigad",
        "start_point": "Bhira village",
        "duration_days": 1,
        "duration": "1 Day",
        "difficulty": "Easy",
        "altitude": "1,500 ft",
        "price": 1349,
        "rating": 4.6,
        "season_months": [6, 7, 8, 9, 10],
        "weekday": 6,
        "images": ["devkund_1", "devkund_2", "devkund_3", "devkund_4"],
        "summary": "A forest trail to a plunge waterfall at the source of the Kundalika river.",
        "overview": (
            "Devkund is a plunge waterfall near Bhira dam, at the start of the Kundalika "
            "river. The easy trail crosses streams and paddy fields before reaching the "
            "turquoise pool at the base of the falls."
        ),
        "highlights": [
            "Turquoise plunge pool",
            "Stream crossings through the forest",
            "Close to Kolad river rafting",
            "Good for first-timers",
        ],
        "itinerary": [
            {"title": "Morning: travel to Bhira", "desc": "Pick-up from Mumbai/Pune at 5:00 AM, breakfast on the way, reach Bhira by 9:30 AM."},
            {"title": "Trek to the waterfall", "desc": "A 2-hour walk through the forest to the falls. Time at the pool (entry only when permitted by local authorities)."},
            {"title": "Return", "desc": "Trek back, lunch in the village and drive home by 8:00 PM."},
        ],
        "inclusions": ["AC transport from Mumbai/Pune", "Breakfast and lunch"] + STANDARD_INCLUSIONS,
        "exclusions": STANDARD_EXCLUSIONS,
    },
    {
        "slug": "kalu-waterfall-trek",
        "name": "Kalu Waterfall Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune", "waterfall", "monsoon", "one-day"],
        "region": "Malshej Ghat, Maharashtra",
        "start_point": "Khireshwar / Titwala",
        "duration_days": 1,
        "duration": "1 Day",
        "difficulty": "Moderate",
        "altitude": "1,200 ft",
        "price": 1099,
        "rating": 4.5,
        "season_months": [7, 8, 9],
        "weekday": 6,
        "images": ["kalu_1", "kalu_2", "kalu_3", "kalu_4"],
        "summary": "One of the tallest waterfalls near Mumbai, reached through dense monsoon forest.",
        "overview": (
            "Kalu waterfall drops almost 1,200 ft from the cliffs of Malshej. The monsoon "
            "trail follows the Kalu river through dense forest, with several river "
            "crossings that our leaders manage with ropes."
        ),
        "highlights": ["1,200 ft waterfall", "River crossings with fixed ropes", "Monsoon-only trail", "Close to Mumbai"],
        "itinerary": [
            {"title": "Morning: reach the base", "desc": "Meet at Titwala at 7:00 AM, travel to Kalu base, breakfast and briefing."},
            {"title": "Trek to the falls", "desc": "A 3-hour trail through the forest with river crossings to the base of the waterfall."},
            {"title": "Return", "desc": "Descend and travel back to Titwala by 6:00 PM."},
        ],
        "inclusions": ["Local transport from Titwala", "Breakfast and lunch"] + STANDARD_INCLUSIONS,
        "exclusions": ["Train travel to Titwala"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "andharban-jungle-trek",
        "name": "Andharban Jungle Trek",
        "category": "sahyadri",
        "tags": ["mumbai-pune", "waterfall", "monsoon", "one-day"],
        "region": "Tamhini Ghat, Pune",
        "start_point": "Pimpri village",
        "duration_days": 1,
        "duration": "1 Day",
        "difficulty": "Easy",
        "altitude": "2,160 ft",
        "price": 1599,
        "rating": 4.7,
        "season_months": [6, 7, 8, 9, 10],
        "weekday": 6,
        "images": ["andharban_1", "andharban_2", "andharban_3", "andharban_4"],
        "summary": "A downhill walk through the 'dark forest' with valley views and small waterfalls.",
        "overview": (
            "Andharban means 'dark forest'. This mostly downhill trail runs along the "
            "edge of the Kundalika valley, through thick canopy and past dozens of "
            "monsoon waterfalls, ending at Bhira village."
        ),
        "highlights": ["Mostly downhill, easy on the knees", "Dense canopy forest", "Valley-edge viewpoints", "Many small waterfalls"],
        "itinerary": [
            {"title": "Morning: travel to Pimpri", "desc": "Pick-up from Pune at 6:00 AM (Mumbai at 4:30 AM), breakfast, reach Pimpri village by 9:00 AM."},
            {"title": "13 km forest trail", "desc": "Walk the Andharban trail with a lunch stop by a stream."},
            {"title": "Finish at Bhira", "desc": "Reach Bhira by 4:00 PM, then drive back."},
        ],
        "inclusions": ["AC transport from Mumbai/Pune", "Breakfast and packed lunch", "Forest entry fee"] + STANDARD_INCLUSIONS,
        "exclusions": STANDARD_EXCLUSIONS,
    },
    # ---------------------------------------------------------------- Himalayan
    {
        "slug": "hampta-pass-trek",
        "name": "Hampta Pass Trek",
        "category": "himalayan",
        "tags": ["trending"],
        "region": "Manali, Himachal Pradesh",
        "start_point": "Manali",
        "duration_days": 5,
        "duration": "5 Days / 4 Nights",
        "difficulty": "Moderate",
        "altitude": "14,100 ft",
        "price": 9999,
        "rating": 4.9,
        "season_months": [6, 7, 8, 9],
        "weekday": 0,  # Monday
        "images": ["hampta_1", "hampta_2", "hampta_3", "hampta_4"],
        "summary": "Cross from the green Kullu valley into the stark desert of Lahaul.",
        "overview": (
            "Hampta Pass is a crossover trek. In a few days you walk from the green "
            "meadows of Kullu, over a 14,100 ft pass, into the bare landscape of Lahaul, "
            "with an optional visit to Chandratal lake."
        ),
        "highlights": ["Dramatic valley crossover", "Camping in alpine meadows", "Chandratal lake (weather permitting)", "Good first Himalayan trek"],
        "itinerary": [
            {"title": "Day 1: Manali to Jobra, trek to Chika", "desc": "Drive to Jobra (1.5 hrs) and trek 2 hrs to the Chika campsite."},
            {"title": "Day 2: Chika to Balu ka Ghera", "desc": "A 5-hour walk along the Rani nallah to the base of the pass."},
            {"title": "Day 3: Cross Hampta Pass to Shea Goru", "desc": "The big day: climb to the pass (14,100 ft) and descend into Lahaul."},
            {"title": "Day 4: Shea Goru to Chatru, Chandratal", "desc": "Trek to Chatru and drive to Chandratal lake if the road is open."},
            {"title": "Day 5: Drive back to Manali", "desc": "Cross Rohtang/Atal Tunnel and reach Manali by evening."},
        ],
        "inclusions": ["All meals during the trek", "Tents, sleeping bags and mats", "Manali to Manali transport", "Mules for common gear"] + STANDARD_INCLUSIONS,
        "exclusions": ["Travel to Manali", "Personal porter", "Stay in Manali"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "kedarkantha-trek",
        "name": "Kedarkantha Winter Trek",
        "category": "himalayan",
        "tags": ["trending"],
        "region": "Uttarkashi, Uttarakhand",
        "start_point": "Sankri",
        "duration_days": 6,
        "duration": "6 Days / 5 Nights",
        "difficulty": "Moderate",
        "altitude": "12,500 ft",
        "price": 10999,
        "rating": 4.8,
        "season_months": [12, 1, 2, 3, 4],
        "weekday": 0,
        "images": ["kedarkantha_1", "kedarkantha_2", "kedarkantha_3", "kedarkantha_4"],
        "summary": "A snow summit trek with pine forests and wide Garhwal views.",
        "overview": (
            "Kedarkantha is one of India's best-known winter treks. Snow-covered pine "
            "forests, the frozen Juda ka Talab and a summit with views of Swargarohini "
            "and Bandarpoonch make it a great introduction to snow trekking."
        ),
        "highlights": ["Snow summit at 12,500 ft", "Juda ka Talab lake", "Campsites in pine forest", "360° summit views"],
        "itinerary": [
            {"title": "Day 1: Dehradun to Sankri", "desc": "A 9-hour scenic drive to the base village of Sankri."},
            {"title": "Day 2: Sankri to Juda ka Talab", "desc": "Trek 4 km through pine and oak forest to the lake camp."},
            {"title": "Day 3: To Kedarkantha base", "desc": "A short climb to the base camp in open meadows."},
            {"title": "Day 4: Summit day", "desc": "Pre-dawn start to the summit for sunrise, then descend to Hargaon camp."},
            {"title": "Day 5: Hargaon to Sankri", "desc": "Descend to Sankri; celebration dinner."},
            {"title": "Day 6: Sankri to Dehradun", "desc": "Drive back to Dehradun by evening."},
        ],
        "inclusions": ["Dehradun to Dehradun transport", "All meals from Day 1 dinner to Day 6 breakfast", "Tents, sleeping bags, microspikes and gaiters"] + STANDARD_INCLUSIONS,
        "exclusions": ["Travel to Dehradun", "Backpack offloading"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "har-ki-dun-trek",
        "name": "Har Ki Dun Trek",
        "category": "himalayan",
        "tags": ["trending"],
        "region": "Uttarkashi, Uttarakhand",
        "start_point": "Dehradun",
        "duration_days": 7,
        "duration": "7 Days / 6 Nights",
        "difficulty": "Moderate",
        "altitude": "11,600 ft",
        "price": 12499,
        "rating": 4.9,
        "season_months": [3, 4, 5, 6, 9, 10, 11, 12],
        "weekday": 5,
        "images": ["harkidun_1", "harkidun_2", "harkidun_3", "harkidun_4"],
        "summary": "The 'Valley of Gods': ancient villages, the Tons river and views of Swargarohini.",
        "overview": (
            "Har Ki Dun is a cradle-shaped valley at the foot of Swargarohini in Govind "
            "National Park. The trail follows the Tons river past centuries-old wooden "
            "villages like Osla, through pine and walnut forest, to open meadows ringed by "
            "snow peaks. It is a gentle-gradient Himalayan trek that works well in both "
            "summer and winter."
        ),
        "highlights": [
            "Views of Swargarohini, Black Peak and Bandarpoonch",
            "Osla village and its ancient Someshwar temple",
            "Riverside trail along the Tons through Govind National Park",
            "Jaundar glacier seen from the Har Ki Dun meadow",
        ],
        # Each day can have: day, title, altitude (str or list), drive, trek, stay,
        # desc (one line for the quick view), details (paragraphs) and image.
        "itinerary": [
            {
                "day": 1, "title": "Dehradun to Sankri",
                "altitude": "Sankri: 1,950 m / 6,400 ft",
                "drive": "200 km | 9–10 hrs",
                "stay": "Guest house",
                "desc": "A full-day scenic drive via Mussoorie and Purola to the base village of Sankri.",
                "details": [
                    "Meet at Dehradun at 6:00 AM. If you are coming from Delhi, an overnight bus or "
                    "train to Dehradun gets you here on time. Sankri is about 200 km away and the "
                    "drive takes most of the day.",
                    "The road climbs past Mussoorie and Kempty Falls, then drops into the Yamuna and "
                    "Tons valleys through Naugaon, Purola, Mori and Netwar. Pine forest lines most of "
                    "the route, and we stop for lunch at a roadside dhaba. Finish important calls at "
                    "Purola – after that, only BSNL and Jio work, and only patchily.",
                    "The last 20 km after the Govind National Park checkpoint are the most scenic. "
                    "We reach Sankri around 6:00 PM. The village has views of Swargarohini and a "
                    "small market where you can pick up any last-minute gear.",
                ],
                "image": "harkidun_day1",
            },
            {
                "day": 2, "title": "Sankri to Dharkot, trek to Osla village",
                "altitude": ["Osla: 2,750 m / 9,000 ft", "Dharkot: 2,500 m / 8,400 ft"],
                "drive": "Sankri to Dharkot, 24 km | 2 hrs",
                "trek": "8 km | 5–6 hrs",
                "stay": "Homestay",
                "desc": "Drive to the roadhead and walk along the Tons river to the old village of Osla.",
                "details": [
                    "After breakfast we drive to Dharkot, the roadhead, and start walking. The trail "
                    "follows the Tons river upstream through walnut, chestnut and pine trees, with "
                    "a few small streams to cross.",
                    "Osla is one of the oldest villages in the valley, known for its carved wooden "
                    "houses and the Someshwar temple. We stay in a village homestay tonight.",
                ],
                "image": "harkidun_day2",
            },
            {
                "day": 3, "title": "Osla to Seematra",
                "altitude": "Seematra: 3,250 m / 10,800 ft",
                "trek": "7 km | 4–5 hrs",
                "stay": "Tents",
                "desc": "A climb past terraced fields to the Seematra meadow camp.",
                "details": [
                    "The trail climbs above Osla through terraced fields of millet and potato, with "
                    "the valley opening up behind you. After the fields, a forest section leads to "
                    "the meadow of Seematra.",
                    "We camp at Seematra for two nights, which also helps you acclimatise before "
                    "the walk into Har Ki Dun.",
                ],
                "image": "harkidun_day3",
            },
            {
                "day": 4, "title": "Seematra to Har Ki Dun and back",
                "altitude": "Har Ki Dun: 3,500 m / 11,600 ft",
                "trek": "8 km (both ways) | 6–7 hrs",
                "stay": "Tents",
                "desc": "The big day: walk into the Har Ki Dun valley and return to camp.",
                "details": [
                    "We start early and walk to the Har Ki Dun meadow, where the Har Ki Dun and "
                    "Maninda streams meet. Swargarohini, Black Peak and Hata peak rise above the "
                    "valley, and the Jaundar glacier is visible further up.",
                    "Spend time exploring the meadow and the small Mahadev temple, then walk back "
                    "to Seematra for the night.",
                ],
                "image": "harkidun_day4",
            },
            {
                "day": 5, "title": "Seematra to Pauni Gharat",
                "altitude": "Pauni Gharat: 2,500 m / 8,300 ft",
                "trek": "8–9 km | 4–5 hrs",
                "stay": "Tents",
                "desc": "A mostly downhill walk back along the river to the Pauni Gharat camp.",
                "details": [
                    "We descend past Osla and continue along the river to Pauni Gharat, named after "
                    "the old water-powered flour mills (gharats) along the stream.",
                ],
                "image": "harkidun_day5",
            },
            {
                "day": 6, "title": "Pauni Gharat to Dharkot, drive to Sankri",
                "altitude": "Sankri: 1,950 m / 6,400 ft",
                "trek": "3–4 km | 2–3 hrs",
                "drive": "24 km | 2 hrs",
                "stay": "Guest house",
                "desc": "A short walk out to the roadhead and a drive back to Sankri.",
                "details": [
                    "A short final walk takes us back to Dharkot, where the vehicles wait to drive "
                    "us to Sankri. The afternoon is free to rest, shop in the market or simply "
                    "enjoy a hot shower. Celebration dinner in the evening.",
                ],
                "image": "harkidun_day6",
            },
            {
                "day": 7, "title": "Sankri to Dehradun",
                "drive": "200 km | 9–10 hrs",
                "desc": "Saying goodbye to the mountains – drive back to Dehradun by evening.",
                "details": [
                    "We leave Sankri after an early breakfast and reach Dehradun between 6:00 and "
                    "8:00 PM. Please book onward travel for after 9:00 PM, or the next day.",
                ],
                "image": "harkidun_day7",
            },
        ],
        "itinerary_notes": [
            "Keep a buffer day in your travel plan in case of bad weather or road blocks.",
            "If the buffer day is not needed, you can use it to explore Dehradun or Mussoorie.",
            "Distances, altitudes and trekking hours are approximate and rounded off.",
            "Carry an original government ID and a photocopy for the forest permits.",
            "If you are flying in, arrive in Dehradun a day early.",
        ],
        "inclusions": ["Dehradun to Dehradun transport", "All meals from Day 1 dinner to Day 7 breakfast", "Guest house, homestay and tents on a sharing basis", "Govind National Park permits"] + STANDARD_INCLUSIONS,
        "exclusions": ["Travel to Dehradun", "Backpack offloading", "Meals during the drives"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "everest-base-camp-trek",
        "name": "Everest Base Camp Trek",
        "category": "himalayan",
        "tags": ["nepal"],
        "region": "Khumbu, Nepal",
        "start_point": "Kathmandu",
        "duration_days": 14,
        "duration": "14 Days / 13 Nights",
        "difficulty": "Challenging",
        "altitude": "17,598 ft",
        "price": 84999,
        "rating": 5.0,
        "season_months": [3, 4, 5, 10, 11],
        "weekday": 0,
        "images": ["ebc_1", "ebc_2", "ebc_3", "ebc_4"],
        "summary": "Walk to the foot of the world's highest mountain through Sherpa villages.",
        "overview": (
            "A once-in-a-lifetime journey to the base of Mount Everest. Fly to Lukla, walk "
            "through Namche Bazaar and Tengboche monastery, and climb Kala Patthar for a "
            "close view of Everest, Lhotse and Nuptse."
        ),
        "highlights": ["Everest Base Camp (17,598 ft)", "Kala Patthar sunrise", "Tengboche monastery", "Sherpa culture in Namche Bazaar"],
        "itinerary": [
            {"title": "Day 1: Arrive in Kathmandu", "desc": "Airport pick-up, hotel check-in and briefing."},
            {"title": "Day 2: Fly to Lukla, trek to Phakding", "desc": "Scenic mountain flight and a 3-hour walk to Phakding."},
            {"title": "Day 3–4: Namche Bazaar and acclimatisation", "desc": "Climb to Namche and spend a rest day with a hike to the Everest View Hotel."},
            {"title": "Day 5–7: Tengboche, Dingboche and acclimatisation", "desc": "Visit the monastery, continue to Dingboche and take an acclimatisation hike."},
            {"title": "Day 8–9: Lobuche, Gorakshep and Base Camp", "desc": "Reach Gorakshep and walk on to Everest Base Camp."},
            {"title": "Day 10: Kala Patthar and descent", "desc": "Sunrise on Kala Patthar, then descend to Pheriche."},
            {"title": "Day 11–12: Return to Lukla", "desc": "Walk back via Namche to Lukla."},
            {"title": "Day 13–14: Fly to Kathmandu and depart", "desc": "Fly back to Kathmandu; a free day for buffer, then departure."},
        ],
        "inclusions": ["Kathmandu–Lukla–Kathmandu flights", "Teahouse stays and all meals on the trek", "Sagarmatha National Park and TIMS permits", "2 nights hotel in Kathmandu"] + STANDARD_INCLUSIONS,
        "exclusions": ["International travel to Kathmandu", "Porter charges", "Hot showers and Wi-Fi in teahouses"] + STANDARD_EXCLUSIONS,
    },
    # ---------------------------------------------------------------- Backpacking & expeditions
    {
        "slug": "spiti-valley-backpacking",
        "name": "Spiti Valley Backpacking",
        "category": "adventure",
        "tags": ["trending"],
        "region": "Spiti, Himachal Pradesh",
        "start_point": "Manali",
        "duration_days": 8,
        "duration": "8 Days / 7 Nights",
        "difficulty": "Easy",
        "altitude": "14,900 ft",
        "price": 18999,
        "rating": 4.8,
        "season_months": [6, 7, 8, 9],
        "weekday": 5,
        "images": ["spiti_1", "spiti_2", "spiti_3", "spiti_4"],
        "summary": "Monasteries, high villages and Chandratal on a road trip through the cold desert.",
        "overview": (
            "A backpacking circuit through the cold desert of Spiti: Key monastery, the "
            "fossil village of Langza, Hikkim (home of the world's highest post office) "
            "and a night by Chandratal lake."
        ),
        "highlights": ["Key and Dhankar monasteries", "Hikkim, Komic and Langza villages", "Chandratal lake camp", "Homestays with Spitian families"],
        "itinerary": [
            {"title": "Day 1: Manali to Kaza", "desc": "Cross the Atal Tunnel and Kunzum Pass to Kaza."},
            {"title": "Day 2: Acclimatisation in Kaza", "desc": "Local sightseeing and a short walk."},
            {"title": "Day 3: Key, Kibber and Chicham bridge", "desc": "Visit Key monastery and the high villages."},
            {"title": "Day 4: Langza, Hikkim and Komic", "desc": "Fossil hunting and posting a letter from Hikkim."},
            {"title": "Day 5: Dhankar and Pin valley", "desc": "Dhankar monastery and a hike to Dhankar lake."},
            {"title": "Day 6: Kaza to Chandratal", "desc": "Drive to the lake and camp nearby."},
            {"title": "Day 7: Chandratal to Manali", "desc": "Return via Batal and Kunzum."},
            {"title": "Day 8: Departure", "desc": "Trip ends after breakfast."},
        ],
        "inclusions": ["Tempo Traveller for the circuit", "Homestays, hotels and camps on a twin/triple sharing basis", "Breakfast and dinner daily"] + STANDARD_INCLUSIONS,
        "exclusions": ["Travel to Manali", "Lunches", "Monastery donations"] + STANDARD_EXCLUSIONS,
    },
    {
        "slug": "yunam-peak-expedition",
        "name": "Yunam Peak Expedition",
        "category": "adventure",
        "tags": ["high-altitude"],
        "region": "Lahaul, Himachal Pradesh",
        "start_point": "Manali",
        "duration_days": 9,
        "duration": "9 Days / 8 Nights",
        "difficulty": "Challenging",
        "altitude": "20,000 ft",
        "price": 27999,
        "rating": 4.9,
        "season_months": [7, 8, 9],
        "weekday": 0,
        "images": ["yunam_1", "yunam_2", "yunam_3", "yunam_4"],
        "summary": "A first 20,000 ft summit for fit trekkers who want to try mountaineering.",
        "overview": (
            "Yunam Peak sits near Baralacha La on the Manali–Leh highway. It is a good "
            "introduction to high-altitude climbing: non-technical, but long and steep, "
            "with a summit day that tests your fitness and acclimatisation."
        ),
        "highlights": ["Summit at about 20,000 ft", "Camp by Bharatpur and Baralacha La", "Basic mountaineering skills", "Views into Zanskar and Lahaul"],
        "itinerary": [
            {"title": "Day 1–2: Manali to Jispa, acclimatisation", "desc": "Drive to Jispa and take an acclimatisation walk."},
            {"title": "Day 3: Jispa to Bharatpur", "desc": "Drive to the base camp near Baralacha La."},
            {"title": "Day 4–5: Advance base camp", "desc": "Load ferry and rest days with skills training."},
            {"title": "Day 6: Summit day", "desc": "Alpine start, summit push and return to base camp."},
            {"title": "Day 7: Buffer day", "desc": "Reserved for bad weather."},
            {"title": "Day 8–9: Return to Manali", "desc": "Drive back via Jispa to Manali."},
        ],
        "inclusions": ["All meals and camping", "Technical gear (harness, helmet, crampons)", "Expedition permits", "Manali to Manali transport"] + STANDARD_INCLUSIONS,
        "exclusions": ["Personal climbing boots", "Rescue/evacuation costs"] + STANDARD_EXCLUSIONS,
    },
    # ---------------------------------------------------------------- Groups
    {
        "slug": "kolad-summer-adventure-camp",
        "name": "Kolad Summer Adventure Camp",
        "category": "groups",
        "tags": ["mumbai-pune", "school", "family"],
        "region": "Kolad, Raigad",
        "start_point": "Mumbai / Pune",
        "duration_days": 3,
        "duration": "3 Days / 2 Nights",
        "difficulty": "Easy",
        "altitude": "—",
        "price": 5499,
        "rating": 4.8,
        "season_months": [4, 5, 10, 11, 12],
        "weekday": 4,  # Friday
        "images": ["kolad_1", "kolad_2", "kolad_3", "kolad_4"],
        "summary": "A supervised camp for kids aged 8–16 with trekking, rafting and campcraft.",
        "overview": (
            "A safe, fully supervised camp for school groups and families. Children learn "
            "to pitch tents, read a map and cook outdoors, try rafting and rope "
            "activities, and finish with a short trek and a campfire night."
        ),
        "highlights": ["1 instructor for every 8 children", "River rafting and rope course", "Campcraft and map reading", "Stargazing and campfire"],
        "itinerary": [
            {"title": "Day 1: Arrival and campcraft", "desc": "Travel to Kolad, pitch tents, team games and campfire."},
            {"title": "Day 2: Adventure day", "desc": "Rafting, zipline, rope course and a nature walk."},
            {"title": "Day 3: Sunrise trek and return", "desc": "Short sunrise trek, breakfast and return home."},
        ],
        "inclusions": ["AC bus from Mumbai/Pune", "All meals", "Tents and activity gear", "24×7 camp supervision"] + STANDARD_INCLUSIONS,
        "exclusions": STANDARD_EXCLUSIONS,
    },
    {
        "slug": "corporate-team-offsite-lonavala",
        "name": "Corporate Team Offsite – Lonavala",
        "category": "groups",
        "tags": ["mumbai-pune", "corporate"],
        "region": "Lonavala, Maharashtra",
        "start_point": "Your office (Mumbai / Pune)",
        "duration_days": 2,
        "duration": "2 Days / 1 Night",
        "difficulty": "Easy",
        "altitude": "—",
        "price": 6999,
        "rating": 4.7,
        "season_months": list(range(1, 13)),
        "weekday": 4,
        "images": ["corporate_1", "corporate_2", "corporate_3", "corporate_4"],
        "summary": "Team-building trek, outdoor challenges and a resort stay, tailored to your team.",
        "overview": (
            "A tailored offsite for teams of 15 to 200. We combine a guided fort trek with "
            "facilitated team challenges, a resort stay and an evening campfire. "
            "Itineraries are customised to your goals and fitness levels."
        ),
        "highlights": ["Custom itinerary for your team", "Facilitated team-building activities", "Resort or lakeside camp stay", "GST invoice provided"],
        "itinerary": [
            {"title": "Day 1: Travel and team challenges", "desc": "Pick-up from your office, check-in, facilitated outdoor challenges and campfire dinner."},
            {"title": "Day 2: Sunrise trek and debrief", "desc": "Guided fort trek, breakfast, debrief session and return."},
        ],
        "inclusions": ["Transport from your office", "Resort stay and all meals", "Facilitators and activity equipment"] + STANDARD_INCLUSIONS,
        "exclusions": ["Alcohol and room service"] + STANDARD_EXCLUSIONS,
    },
]
TREK_MAP = {t["slug"]: t for t in TREKS}


def _prepare_itineraries():
    """Give every itinerary step a short `label` for the day badges.

    Uses `day` when set, else a "Day 3–4: ..." prefix in the title (which is
    then removed from the title), else the step number.
    """
    for trek in TREKS:
        for i, step in enumerate(trek["itinerary"], start=1):
            if "day" in step:
                step["label"] = f"Day {step['day']}"
                continue
            m = re.match(r"(Days? [\d–-]+):\s*(.+)", step["title"])
            if m:
                step["label"], step["title"] = m.group(1), m.group(2)
            else:
                step["label"] = f"Step {i}"
        trek.setdefault("itinerary_notes", [])


_prepare_itineraries()


def upcoming_dates(trek, count=4, today=None):
    """Next `count` departures that fall on the trek's weekday and within its season."""
    today = today or date.today()
    dates = []
    d = today + timedelta(days=1)
    for _ in range(400):
        if d.weekday() == trek["weekday"] and d.month in trek["season_months"]:
            dates.append(d)
            if len(dates) == count:
                break
        d += timedelta(days=1)
    return dates


TEAM = [
    {"name": "Aarav Deshmukh", "role": "Founder & Lead Trek Leader",
     "bio": "Has led more than 500 Sahyadri treks and 40 Himalayan expeditions. Certified by NIM Uttarkashi.",
     "photo": "team_1"},
    {"name": "Meera Kulkarni", "role": "Head of Operations",
     "bio": "Plans every itinerary, permit and vehicle so that trips run safely and on time.",
     "photo": "team_2"},
    {"name": "Rohan Patil", "role": "Himalayan Expedition Lead",
     "bio": "Mountaineer with summits above 6,000 m and a Wilderness First Responder certificate.",
     "photo": "team_3"},
    {"name": "Sneha Joshi", "role": "School & Corporate Programs",
     "bio": "Former teacher who designs safe, fun outdoor programs for students and teams.",
     "photo": "team_4"},
]

GALLERY = [
    {"image": "gallery_1", "caption": "Monsoon mist at Rajmachi", "cat": "sahyadri"},
    {"image": "gallery_2", "caption": "Devkund waterfall", "cat": "monsoon"},
    {"image": "gallery_3", "caption": "Kedarkantha summit ridge", "cat": "himalayan"},
    {"image": "gallery_4", "caption": "Night sky over Kalsubai", "cat": "sahyadri"},
    {"image": "gallery_5", "caption": "Camp at Harishchandragad", "cat": "camping"},
    {"image": "gallery_6", "caption": "Khumbu valley, Nepal", "cat": "himalayan"},
    {"image": "gallery_7", "caption": "Andharban forest trail", "cat": "monsoon"},
    {"image": "gallery_8", "caption": "Campfire night at Kolad", "cat": "camping"},
    {"image": "gallery_9", "caption": "Hampta Pass crossover", "cat": "himalayan"},
    {"image": "gallery_10", "caption": "Green Sahyadri plateau", "cat": "monsoon"},
    {"image": "gallery_11", "caption": "Tents under the stars", "cat": "camping"},
    {"image": "gallery_12", "caption": "Konkan Kada cliff", "cat": "sahyadri"},
]
GALLERY_FILTERS = [("all", "All"), ("sahyadri", "Sahyadri"), ("himalayan", "Himalayan"),
                   ("monsoon", "Monsoon"), ("camping", "Camping")]

# Replace these YouTube IDs with your own trek videos.
VIDEOS = [
    {"youtube_id": "REPLACE_WITH_VIDEO_ID_1", "title": "Rajmachi in the monsoon", "poster": "video_1"},
    {"youtube_id": "REPLACE_WITH_VIDEO_ID_2", "title": "Hampta Pass crossover", "poster": "video_2"},
    {"youtube_id": "REPLACE_WITH_VIDEO_ID_3", "title": "Everest Base Camp diaries", "poster": "video_3"},
]

TESTIMONIALS = [
    {"name": "Priya S.", "trek": "Hampta Pass", "text": "Very well organised. The leaders were patient with our group, and the campsite food was great."},
    {"name": "Karan M.", "trek": "Rajmachi", "text": "My first trek and I'm hooked. Safety briefings were clear and the pace suited beginners."},
    {"name": "Ananya R.", "trek": "Kolad Summer Camp", "text": "My kids came back confident and full of stories. The supervision was excellent."},
]

HERO_SLIDES = [
    {"image": "hero_1", "eyebrow": "Himalayan Season 2027",
     "title": "Find your next summit", "text": "Guided treks across the Sahyadris, the Indian Himalaya and Nepal.",
     "cta": "Explore Treks", "href": "/tours"},
    {"image": "hero_2", "eyebrow": "Monsoon Specials",
     "title": "Chase waterfalls near Mumbai & Pune", "text": "One-day monsoon treks through forests, forts and falls.",
     "cta": "View Monsoon Treks", "href": "/tours?tag=monsoon"},
    {"image": "hero_3", "eyebrow": "Schools, Families & Teams",
     "title": "Adventures for every group", "text": "Summer camps, family treks and corporate offsites, planned end to end.",
     "cta": "Plan a Group Trip", "href": "/tours?category=groups"},
]
