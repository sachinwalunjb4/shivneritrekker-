# Shivneri Trekkers – Trekking Company Website

A responsive trekking website built with **Flask**, **Bootstrap 5**, Font Awesome and vanilla JavaScript.

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (optional for local development)
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux

# 4. Run the development server
python app.py
```

Open http://127.0.0.1:5000.

The site works without any configuration:
- **Contact form:** with no `SMTP_HOST` set, emails are printed to the terminal instead of being sent.
- **Checkout:** with no Razorpay keys set, it runs in demo mode and simulates a successful payment.

## Pages and routes

| URL | Template | Purpose |
|---|---|---|
| `/` | `index.html` | Hero slider, trending treks, treks by location, monsoon specials, categories |
| `/about` | `about.html` | Company story, mission and team |
| `/tours` | `tours.html` | Filterable grid/list of all treks (`?category=`, `?tag=`, `?q=`) |
| `/trek/<slug>` | `trek-detail.html` | Trek detail: slider, facts, itinerary, inclusions, gallery, booking |
| `/gallery` | `gallery.html` | Filterable photo gallery with lightbox, plus YouTube videos |
| `/contact` | `contact.html` | Contact form (GET shows it, POST emails the admin team) |
| `/checkout/<slug>` | `checkout.html` | Booking form and payment |
| `/api/treks` | – | JSON list of treks (`?tag=`, `?category=`) |
| `/api/payment/order` | – | Creates a Razorpay order (or a demo order) |
| `/api/payment/verify` | – | Verifies the payment signature and emails the booking to admin |

Links such as `/about.html` redirect to the clean URLs.

## Project structure

```
app.py              Flask app: routes, contact email (smtplib), payment endpoints
data.py             Treks, categories, team, gallery and videos (edit content here)
images.py           ALL image references in one place (edit images here)
static/img/         Your own photos
templates/
  base.html         Layout, navbar, footer, Google Analytics, WhatsApp button
  partials/_macros.html   Trek card, difficulty meter, page header
  index.html  about.html  tours.html  trek-detail.html
  gallery.html  contact.html  checkout.html  404.html
static/css/style.css
static/js/main.js       Navbar, parallax, reveal, lightbox, filters, YouTube, contact form
static/js/checkout.js   Razorpay checkout flow
```

## Configuration (`.env`)

| Setting | What it does |
|---|---|
| `GA_MEASUREMENT_ID` | Your GA4 ID (`G-XXXXXXXXXX`). Loads gtag.js on every page. Leave empty to disable. Events sent: `generate_lead`, `begin_checkout`, `purchase`, `video_play`. |
| `SMTP_*`, `MAIL_FROM`, `ADMIN_EMAIL` | Email delivery for the contact form and booking notifications. Works with Gmail (App Password), SendGrid SMTP, Amazon SES, Zoho, etc. |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` | Turns on live Razorpay checkout. Start with **test** keys. |
| `WHATSAPP_NUMBER` | Number for every WhatsApp button (country code, digits only). |
| `CONTACT_*`, `SITE_NAME`, `MAP_EMBED_URL` | Business details shown across the site. |

## Customising content

- **Treks:** edit the `TREKS` list in `data.py`. Each trek has a category, tags (`mumbai-pune`, `waterfall`, `monsoon`, `trending`, `nepal`), itinerary, inclusions, exclusions and photos. Departure dates are generated automatically from `weekday` and `season_months`.
- **Images:** every image on the site is listed in **`images.py`**, the only file you need to edit. Each name (e.g. `hero_1`, `header_about`, `rajmachi_1`, `team_1`, `gallery_5`) maps to an Unsplash photo ID, a file in `static/img/`, a full URL, or another name. To use your own photo, copy it to `static/img/` and set, for example, `"rajmachi_1": "treks/rajmachi-1.jpg"`. Templates call `{{ img('name', width) }}`. Broken images fall back to placeholders automatically.
- **Videos:** replace the `REPLACE_WITH_VIDEO_ID_*` values in `VIDEOS` (in `data.py`) with your 11-character YouTube video IDs.

## Payments

The amount is always calculated on the server from the trek price and participant count, so it can't be changed in the browser. In live mode, `/api/payment/verify` checks Razorpay's HMAC-SHA256 signature before confirming a booking.

To use **Stripe** instead, replace the Razorpay call in `create_order()` with `stripe.checkout.Session.create(...)`, return `session.url`, and redirect to it in `checkout.js`.

For production, also add a database to store bookings and a [Razorpay webhook](https://razorpay.com/docs/webhooks/) (`payment.captured`) so bookings are recorded even if the customer closes the browser.

## Production

```bash
# Linux / macOS
gunicorn -w 3 -b 0.0.0.0:8000 app:app
# Windows
waitress-serve --port=8000 app:app
```

Set `FLASK_DEBUG=0` and a strong `SECRET_KEY`, and serve over HTTPS (Razorpay requires HTTPS in live mode).
