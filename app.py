"""
Rock & Ridge Expeditions – trekking company website (Flask).

Run:  python app.py      (or)  flask --app app run --debug
"""
import base64
import calendar
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import smtplib
import ssl
import time
import urllib.error
import urllib.request
from collections import defaultdict, deque
from datetime import date
from email.message import EmailMessage
from urllib.parse import quote

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)

try:  # Optional: load settings from a .env file during development.
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import data
from images import img

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or secrets.token_hex(32)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("rock-ridge-expeditions")

SITE = {
    "name": os.getenv("SITE_NAME", "Rock & Ridge Expeditions"),
    "tagline": "Treks & Expeditions",
    "contact_person": os.getenv("CONTACT_PERSON", "Rock & Ridge  Desk support"),
    "phone": os.getenv("CONTACT_PHONE", "+91 98811 43180/ +91 93091 87676"),
    "email": os.getenv("CONTACT_EMAIL", "dhyassahyadri@gmail.com"),
    "address": os.getenv("CONTACT_ADDRESS", "Narayangaon, Junnar, Pune, Maharashtra 410504"),
    "hours": [
        "Monday - Saturday: 10 AM to 10 PM (GMT +5:30)",
        "Sunday: 10 AM to 06 PM (GMT +5:30)",
    ],
    "whatsapp": re.sub(r"\D", "", os.getenv("WHATSAPP_NUMBER", "919881143180")),
    "instagram": "https://instagram.com/",
    "facebook": "https://facebook.com/",
    "youtube": "https://youtube.com/",
    "ga_id": os.getenv("GA_MEASUREMENT_ID", ""),
    "map_embed": os.getenv(
        "MAP_EMBED_URL",
        "https://www.google.com/maps?q=Narayangaon,+Junnar,+Pune,+Maharashtra&z=14&output=embed",
    ),
    "map_link": os.getenv(
        "MAP_LINK_URL",
        "https://www.google.com/maps/search/?api=1&query=Narayangaon%2C+Junnar%2C+Pune%2C+Maharashtra",
    ),
}

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
PAYMENTS_LIVE = bool(RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET)
MAX_PARTICIPANTS = 20


# --------------------------------------------------------------------------- helpers
def whatsapp_link(text=""):
    return f"https://wa.me/{SITE['whatsapp']}" + (f"?text={quote(text)}" if text else "")


@app.context_processor
def inject_globals():
    return {
        "site": SITE,
        "categories": data.CATEGORIES,
        "category_map": data.CATEGORY_MAP,
        "levels": data.DIFFICULTY_LEVEL,
        "whatsapp_link": whatsapp_link,
        "img": img,
        "year": date.today().year,
    }


@app.template_filter("months")
def months(nums):
    """[6, 7, 8, 9] -> 'Jun, Jul, Aug, Sep'; all twelve -> 'All year'."""
    if len(set(nums)) == 12:
        return "All year"
    return ", ".join(calendar.month_abbr[n] for n in nums)


@app.template_filter("inr")
def inr(value):
    """Format a number with Indian digit grouping: 84999 -> ₹84,999; 1234567 -> ₹12,34,567."""
    s = str(int(value))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = ",".join(re.findall(r"\d{1,2}", head[::-1]))[::-1]
        s = f"{head},{tail}"
    return f"₹{s}"


def treks_with(tag=None, category=None, limit=None):
    items = [t for t in data.TREKS
             if (tag is None or tag in t["tags"]) and (category is None or t["category"] == category)]
    return items[:limit] if limit else items


def wants_json():
    return (request.headers.get("X-Requested-With") == "fetch"
            or request.accept_mimetypes.best == "application/json")


# Very small in-memory rate limiter for form posts (per process, per IP).
_hits = defaultdict(deque)


def rate_limited(key, limit=5, window=600):
    now = time.time()
    q = _hits[key]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= limit:
        return True
    q.append(now)
    return False


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[\d\s\-()]{7,20}$")


def clean(value, max_len):
    """Trim, collapse newlines (for single-line fields) and cap length."""
    return re.sub(r"[\r\n]+", " ", (value or "").strip())[:max_len]


# --------------------------------------------------------------------------- email
def send_admin_email(subject, body, reply_to=None):
    """
    Send a plain-text email to the admin team over SMTP.

    Works with any SMTP provider, including SendGrid
    (SMTP_HOST=smtp.sendgrid.net, SMTP_USERNAME=apikey, SMTP_PASSWORD=<API key>).
    If SMTP_HOST is not set, the email is printed to the log instead, so the
    site works out of the box during development.
    """
    host = os.getenv("SMTP_HOST")
    admin = os.getenv("ADMIN_EMAIL", SITE["email"])
    sender = os.getenv("MAIL_FROM", os.getenv("SMTP_USERNAME", "no-reply@rockandridgeexpeditions.example"))

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = admin
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body)

    if not host:
        log.warning("SMTP_HOST not set - email not sent. Message follows:\n%s", msg)
        return True

    port = int(os.getenv("SMTP_PORT", "587"))
    user, password = os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD")
    context = ssl.create_default_context()
    try:
        if os.getenv("SMTP_USE_SSL", "false").lower() == "true" or port == 465:
            server = smtplib.SMTP_SSL(host, port, context=context, timeout=15)
        else:
            server = smtplib.SMTP(host, port, timeout=15)
            server.starttls(context=context)
        with server:
            if user and password:
                server.login(user, password)
            server.send_message(msg)
        log.info("Email sent to %s: %s", admin, subject)
        return True
    except (smtplib.SMTPException, OSError):
        log.exception("Failed to send email")
        return False


# --------------------------------------------------------------------------- pages
@app.route("/")
def index():
    location_groups = [
        {**f, "treks": treks_with(tag=f["slug"], limit=6)} for f in data.LOCATION_FILTERS
    ]
    category_counts = {c["slug"]: len(treks_with(category=c["slug"])) for c in data.CATEGORIES}
    return render_template(
        "index.html",
        slides=data.HERO_SLIDES,
        trending=treks_with(tag="trending", limit=4),
        location_groups=location_groups,
        monsoon=treks_with(tag="monsoon", limit=3),
        category_counts=category_counts,
        testimonials=data.TESTIMONIALS,
        trek_count=len(data.TREKS),
        treks=data.TREKS,
    )


@app.route("/about")
def about():
    return render_template("about.html", team=data.TEAM)


@app.route("/tours")
def tours():
    return render_template(
        "tours.html",
        treks=data.TREKS,
        location_filters=data.LOCATION_FILTERS,
        selected={
            "category": request.args.get("category", ""),
            "tag": request.args.get("tag", ""),
            "q": request.args.get("q", ""),
        },
    )


@app.route("/trek/<slug>")
def trek_detail(slug):
    trek = data.TREK_MAP.get(slug) or abort(404)
    related = [t for t in data.TREKS if t["category"] == trek["category"] and t["slug"] != slug][:3]
    return render_template(
        "trek-detail.html",
        trek=trek,
        dates=data.upcoming_dates(trek),
        related=related,
        treks=data.TREKS,
        wa_text=f"Hi! I'm interested in the {trek['name']} ({trek['duration']}). Please share details.",
    )


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", photos=data.GALLERY,
                           filters=data.GALLERY_FILTERS, videos=data.VIDEOS)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", treks=data.TREKS,
                               preselect=request.args.get("trek", ""))

    form = request.form
    fields = {
        "name": clean(form.get("name"), 100),
        "email": clean(form.get("email"), 150),
        "phone": clean(form.get("phone"), 20),
        "trek": clean(form.get("trek"), 150),
        "message": (form.get("message") or "").strip()[:3000],
    }

    def respond(ok, message, status=200, errors=None):
        if wants_json():
            return jsonify(ok=ok, message=message, errors=errors or {}), status
        flash(message, "success" if ok else "danger")
        return redirect(url_for("contact"))

    # Honeypot: real users never fill this hidden field.
    if form.get("website"):
        return respond(True, "Thanks! We'll get back to you shortly.")

    errors = {}
    if len(fields["name"]) < 2:
        errors["name"] = "Please enter your name."
    if not EMAIL_RE.match(fields["email"]):
        errors["email"] = "Please enter a valid email address."
    if not PHONE_RE.match(fields["phone"]):
        errors["phone"] = "Please enter a valid phone number."
    if len(fields["message"]) < 10:
        errors["message"] = "Please write a message of at least 10 characters."
    if errors:
        return respond(False, "Please correct the highlighted fields.", 400, errors)

    if rate_limited(f"contact:{request.remote_addr}"):
        return respond(False, "Too many messages. Please try again in a few minutes.", 429)

    body = (
        "New enquiry from the website\n"
        "----------------------------\n"
        f"Name:    {fields['name']}\n"
        f"Email:   {fields['email']}\n"
        f"Phone:   {fields['phone']}\n"
        f"Trek:    {fields['trek'] or 'Not specified'}\n\n"
        f"Message:\n{fields['message']}\n"
    )
    subject = f"New enquiry: {fields['trek'] or 'General'} – {fields['name']}"
    if not send_admin_email(subject, body, reply_to=fields["email"]):
        return respond(False, "We couldn't send your message right now. Please call or WhatsApp us.", 502)
    return respond(True, "Thanks! Your message has been sent. Our team will contact you within 24 hours.")


@app.route("/inquiry", methods=["POST"])
def inquiry():
    """Quick enquiry from the home-page popup (AJAX only)."""
    form = request.form
    fields = {
        "name": clean(form.get("name"), 100),
        "email": clean(form.get("email"), 150),
        "phone": clean(form.get("phone"), 20),
        "city": clean(form.get("city"), 80),
        "trek": clean(form.get("trek"), 150),
    }

    # Honeypot: real users never fill this hidden field.
    if form.get("website"):
        return jsonify(ok=True, message="Thanks! We'll get back to you shortly.", errors={})

    errors = {}
    if len(fields["name"]) < 2:
        errors["name"] = "Please enter your name."
    if not EMAIL_RE.match(fields["email"]):
        errors["email"] = "Please enter a valid email address."
    if not PHONE_RE.match(fields["phone"]):
        errors["phone"] = "Please enter a valid mobile number."
    if len(fields["city"]) < 2:
        errors["city"] = "Please enter your city."
    if not fields["trek"]:
        errors["trek"] = "Please choose a trek."
    if errors:
        return jsonify(ok=False, message="Please correct the highlighted fields.", errors=errors), 400

    if rate_limited(f"inquiry:{request.remote_addr}"):
        return jsonify(ok=False, message="Too many requests. Please try again in a few minutes.", errors={}), 429

    body = (
        "New quick enquiry from the home-page popup\n"
        "------------------------------------------\n"
        f"Name:    {fields['name']}\n"
        f"Email:   {fields['email']}\n"
        f"Mobile:  {fields['phone']}\n"
        f"City:    {fields['city']}\n"
        f"Trek:    {fields['trek']}\n"
    )
    subject = f"Quick enquiry: {fields['trek']} – {fields['name']} ({fields['city']})"
    if not send_admin_email(subject, body, reply_to=fields["email"]):
        return jsonify(ok=False, message="We couldn't send your details right now. Please call or WhatsApp us.",
                       errors={}), 502
    return jsonify(ok=True, message="Thanks! Our team will contact you within 24 hours.", errors={})


@app.route("/checkout/<slug>")
def checkout(slug):
    trek = data.TREK_MAP.get(slug) or abort(404)
    return render_template(
        "checkout.html",
        trek=trek,
        dates=data.upcoming_dates(trek, count=6),
        selected_date=request.args.get("date", ""),
        payments_live=PAYMENTS_LIVE,
        razorpay_key=RAZORPAY_KEY_ID,
        max_participants=MAX_PARTICIPANTS,
    )


# --------------------------------------------------------------------------- APIs
@app.route("/api/treks")
def api_treks():
    tag, category = request.args.get("tag"), request.args.get("category")
    return jsonify([
        {k: t[k] for k in ("slug", "name", "category", "tags", "region", "duration",
                           "difficulty", "price", "rating", "summary")}
        | {"image": img(t["images"][0], 700), "url": url_for("trek_detail", slug=t["slug"])}
        for t in treks_with(tag=tag, category=category)
    ])


def _razorpay_request(path, payload=None):
    """Call the Razorpay REST API directly (no SDK needed). GET when payload is None."""
    token = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
    req = urllib.request.Request(
        f"https://api.razorpay.com/v1/{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Basic {token}", "Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


@app.route("/api/payment/order", methods=["POST"])
def create_order():
    """
    Create a payment order. The amount is always calculated on the server from
    the trek price so it cannot be tampered with in the browser.

    With RAZORPAY_KEY_ID/RAZORPAY_KEY_SECRET set, a real Razorpay order is
    created. Without them the endpoint returns a demo order so the checkout
    flow can be tested end to end.

    Stripe alternative: replace the Razorpay call with
    stripe.checkout.Session.create(...) and return the session URL.
    """
    body = request.get_json(silent=True) or {}
    trek = data.TREK_MAP.get(body.get("slug", ""))
    if not trek:
        return jsonify(ok=False, message="Unknown trek."), 400

    valid_dates = {d.isoformat() for d in data.upcoming_dates(trek, count=6)}
    if body.get("date") not in valid_dates:
        return jsonify(ok=False, message="Please choose one of the available dates."), 400
    try:
        participants = int(body.get("participants", 1))
    except (TypeError, ValueError):
        participants = 0
    if not 1 <= participants <= MAX_PARTICIPANTS:
        return jsonify(ok=False, message=f"Participants must be between 1 and {MAX_PARTICIPANTS}."), 400

    name, email, phone = (clean(body.get(k), 150) for k in ("name", "email", "phone"))
    if len(name) < 2 or not EMAIL_RE.match(email) or not PHONE_RE.match(phone):
        return jsonify(ok=False, message="Please enter a valid name, email and phone number."), 400

    # Add-ons and tent type: only options this trek offers, priced from data.py.
    addon_prices = {a["slug"]: a for a in trek["addon_list"]}
    chosen = body.get("addons") or []
    if not isinstance(chosen, list) or any(a not in addon_prices for a in chosen):
        return jsonify(ok=False, message="Please choose valid add-ons."), 400
    chosen = [addon_prices[a] for a in dict.fromkeys(chosen)]
    tent = None
    if trek["tent_list"]:
        tents = {t["slug"]: t for t in trek["tent_list"]}
        tent = tents.get(body.get("tent") or trek["tent_list"][0]["slug"])
        if not tent:
            return jsonify(ok=False, message="Please choose a valid tent type."), 400

    per_person = trek["price"] + sum(a["price"] for a in chosen) + (tent["price"] if tent else 0)
    amount_paise = per_person * participants * 100
    notes = {"trek": trek["name"], "date": body["date"], "participants": str(participants),
             "name": name, "email": email, "phone": phone,
             "addons": ", ".join(a["name"] for a in chosen) or "None"}
    if tent:
        notes["tent"] = tent["name"]

    if not PAYMENTS_LIVE:
        order_id = f"order_DEMO{secrets.token_hex(6)}"
        log.info("Demo order %s created: %s", order_id, notes)
        return jsonify(ok=True, demo=True, order_id=order_id, amount=amount_paise,
                       currency="INR", notes=notes)

    try:
        order = _razorpay_request("orders", {
            "amount": amount_paise, "currency": "INR",
            "receipt": f"rcpt_{secrets.token_hex(6)}", "notes": notes,
        })
    except (urllib.error.URLError, ValueError):
        log.exception("Razorpay order creation failed")
        return jsonify(ok=False, message="Payment gateway is unavailable. Please try again."), 502
    return jsonify(ok=True, demo=False, order_id=order["id"], amount=order["amount"],
                   currency=order["currency"], key=RAZORPAY_KEY_ID, notes=notes)


@app.route("/api/payment/verify", methods=["POST"])
def verify_payment():
    """Verify the Razorpay signature, then notify the admin team about the booking."""
    body = request.get_json(silent=True) or {}
    order_id = body.get("razorpay_order_id", "")
    payment_id = body.get("razorpay_payment_id", "")
    notes = body.get("notes") or {}

    if PAYMENTS_LIVE:
        expected = hmac.new(RAZORPAY_KEY_SECRET.encode(), f"{order_id}|{payment_id}".encode(),
                            hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, body.get("razorpay_signature", "")):
            return jsonify(ok=False, message="Payment verification failed."), 400
        try:  # Use the booking details stored on the order, not the ones sent by the browser.
            notes = _razorpay_request(f"orders/{quote(order_id)}").get("notes") or {}
        except (urllib.error.URLError, ValueError):
            log.exception("Could not fetch Razorpay order %s", order_id)
    elif not order_id.startswith("order_DEMO"):
        return jsonify(ok=False, message="Invalid demo order."), 400

    lines = "\n".join(f"{k.title():<13} {clean(str(v), 150)}" for k, v in notes.items())
    send_admin_email(
        f"New booking{' (DEMO)' if not PAYMENTS_LIVE else ''}: {clean(notes.get('trek'), 100)}",
        f"Payment ID:   {payment_id}\nOrder ID:     {order_id}\n{lines}\n",
        reply_to=notes.get("email") if EMAIL_RE.match(str(notes.get("email", ""))) else None,
    )
    return jsonify(ok=True, message="Booking confirmed!", payment_id=payment_id)


# --------------------------------------------------------------------------- misc
LEGACY_PAGES = {"index": "index", "about": "about", "tours": "tours",
                "gallery": "gallery", "contact": "contact"}


@app.route("/<page>.html")
def legacy_html(page):
    """Support links like /about.html by redirecting to the clean URL."""
    endpoint = LEGACY_PAGES.get(page) or abort(404)
    return redirect(url_for(endpoint), code=301)


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1",
            host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
