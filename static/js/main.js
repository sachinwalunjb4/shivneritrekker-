/* Rock & Ridge Expeditions – site-wide JavaScript (no dependencies beyond Bootstrap). */
(() => {
  "use strict";

  document.documentElement.classList.add("js");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* ------------------------------------------------ Broken image fallback */
  document.addEventListener("error", (e) => {
    const img = e.target;
    if (img.tagName !== "IMG" || img.dataset.fallback) return;
    img.dataset.fallback = "1";
    const seed = encodeURIComponent((img.alt || "trek").slice(0, 20));
    img.src = `https://picsum.photos/seed/${seed}/${img.getAttribute("width") || 800}/${img.getAttribute("height") || 600}`;
  }, true);

  /* ------------------------------------------------ Info popovers (add-ons) */
  if (window.bootstrap?.Popover) {
    $$('[data-bs-toggle="popover"]').forEach((el) => new bootstrap.Popover(el));
  }

  /* ------------------------------------------------ Navbar */
  const nav = $("#siteNav");
  const navMenu = $("#navMenu");
  const backToTop = $(".back-to-top");
  const onScrollUI = () => {
    const y = window.scrollY;
    nav?.classList.toggle("scrolled", y > 40);
    backToTop?.classList.toggle("show", y > 600);
  };
  navMenu?.addEventListener("show.bs.collapse", () => nav.classList.add("menu-open"));
  navMenu?.addEventListener("hidden.bs.collapse", () => nav.classList.remove("menu-open"));
  backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }));

  /* ------------------------------------------------ Parallax (rAF-throttled, transform only) */
  const parallaxSections = $$(".parallax").map((el) => ({
    el, bg: $(".parallax-bg", el), speed: parseFloat(el.dataset.parallaxSpeed || "0.3"),
  })).filter((p) => p.bg);
  const heroBgs = $$(".parallax-hero");

  const updateParallax = () => {
    const vh = window.innerHeight;
    const y = window.scrollY;
    heroBgs.forEach((bg) => {
      if (y < vh * 1.2) bg.style.transform = `translate3d(0, ${y * 0.35}px, 0)`;
    });
    parallaxSections.forEach(({ el, bg, speed }) => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const offset = (r.top + r.height / 2 - vh / 2) * -speed;
      bg.style.transform = `translate3d(0, ${offset.toFixed(1)}px, 0)`;
    });
  };

  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      onScrollUI();
      if (!reduceMotion) updateParallax();
      ticking = false;
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();

  /* ------------------------------------------------ Reveal on scroll */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("visible"));
  }

  /* ------------------------------------------------ Lightbox */
  (() => {
    let box, img, caption, items = [], index = 0, lastFocus = null, touchX = null;

    const build = () => {
      box = document.createElement("div");
      box.className = "lightbox";
      box.setAttribute("role", "dialog");
      box.setAttribute("aria-modal", "true");
      box.setAttribute("aria-label", "Image viewer");
      box.innerHTML = `
        <button type="button" class="lb-close" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>
        <button type="button" class="lb-prev" aria-label="Previous image"><i class="fa-solid fa-chevron-left"></i></button>
        <figure><img alt=""><figcaption></figcaption></figure>
        <button type="button" class="lb-next" aria-label="Next image"><i class="fa-solid fa-chevron-right"></i></button>`;
      document.body.appendChild(box);
      img = $("img", box);
      caption = $("figcaption", box);
      $(".lb-close", box).addEventListener("click", close);
      $(".lb-prev", box).addEventListener("click", () => show(index - 1));
      $(".lb-next", box).addEventListener("click", () => show(index + 1));
      box.addEventListener("click", (e) => { if (e.target === box) close(); });
      box.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
      box.addEventListener("touchend", (e) => {
        if (touchX === null) return;
        const dx = e.changedTouches[0].clientX - touchX;
        if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
        touchX = null;
      });
      img.addEventListener("load", () => img.classList.remove("loading"));
    };

    const show = (i) => {
      index = (i + items.length) % items.length;
      const a = items[index];
      img.classList.add("loading");
      img.src = a.href;
      img.alt = a.dataset.caption || "";
      caption.innerHTML = "";
      caption.append(a.dataset.caption || "");
      if (items.length > 1) {
        const count = document.createElement("small");
        count.textContent = `${index + 1} / ${items.length}`;
        caption.append(count);
      }
      const multi = items.length > 1;
      $(".lb-prev", box).hidden = !multi;
      $(".lb-next", box).hidden = !multi;
      // Preload neighbours for instant navigation.
      [index + 1, index - 1].forEach((n) => { new Image().src = items[(n + items.length) % items.length].href; });
    };

    const open = (group, start) => {
      if (!box) build();
      items = group;
      lastFocus = document.activeElement;
      show(items.indexOf(start));
      box.classList.add("open");
      document.body.style.overflow = "hidden";
      $(".lb-close", box).focus();
      document.addEventListener("keydown", onKey);
    };

    const close = () => {
      box.classList.remove("open");
      document.body.style.overflow = "";
      document.removeEventListener("keydown", onKey);
      lastFocus?.focus();
    };

    const onKey = (e) => {
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight") show(index + 1);
      else if (e.key === "ArrowLeft") show(index - 1);
      else if (e.key === "Tab") { // keep focus inside the dialog
        const focusables = $$("button:not([hidden])", box);
        const first = focusables[0], last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    };

    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-lightbox]");
      if (!a) return;
      e.preventDefault();
      const group = $$(`a[data-lightbox="${a.dataset.lightbox}"]`).filter((el) => !el.classList.contains("is-hidden"));
      open(group, a);
    });
  })();

  /* ------------------------------------------------ Gallery filter */
  const galleryGrid = $("#galleryGrid");
  $$(".filter-pills [data-filter]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const f = btn.dataset.filter;
      $$(".filter-pills [data-filter]").forEach((b) => {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      $$(".gallery-item", galleryGrid).forEach((item) => {
        item.classList.toggle("is-hidden", f !== "all" && item.dataset.cat !== f);
      });
    });
  });

  /* ------------------------------------------------ YouTube: load iframe on click */
  $$(".yt-lite").forEach((wrap) => {
    wrap.addEventListener("click", () => {
      const id = wrap.dataset.youtubeId || "";
      if (!/^[\w-]{11}$/.test(id)) {
        wrap.innerHTML = `<div class="d-flex align-items-center justify-content-center text-white p-3 text-center small">
          Add a real YouTube video ID for this video in data.py (VIDEOS).</div>`;
        return;
      }
      const iframe = document.createElement("iframe");
      iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
      iframe.title = wrap.dataset.title || "YouTube video";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      iframe.allowFullscreen = true;
      wrap.replaceChildren(iframe);
      window.gtag?.("event", "video_play", { video_id: id });
    }, { once: false });
  });

  /* ------------------------------------------------ Tours: filter, sort, grid/list */
  const filterForm = $("#trekFilters");
  if (filterForm) {
    const grid = $("#trekGrid");
    const cols = $$(".trek-col", grid);
    const countEl = $("#resultCount");
    const empty = $("#emptyState");
    const clearBtn = $("#clearFilters");
    const fields = ["q", "category", "tag", "difficulty", "days", "sort"].map((n) => filterForm.elements[n]);

    // Pre-fill selects from query string values not rendered by the server (difficulty, days, sort).
    const params = new URLSearchParams(location.search);
    fields.forEach((f) => { if (params.has(f.name)) f.value = params.get(f.name); });

    const apply = () => {
      const v = Object.fromEntries(fields.map((f) => [f.name, f.value.trim()]));
      const q = v.q.toLowerCase();
      const [minD, maxD] = v.days ? v.days.split("-").map(Number) : [0, Infinity];
      let shown = 0;

      cols.forEach((col) => {
        const c = col.firstElementChild.dataset;
        const days = Number(c.days);
        const match = (!q || c.name.includes(q))
          && (!v.category || c.category === v.category)
          && (!v.tag || c.tags.split(" ").includes(v.tag))
          && (!v.difficulty || c.difficulty === v.difficulty)
          && days >= minD && days <= maxD;
        col.classList.toggle("is-hidden", !match);
        if (match) shown++;
      });

      const [key, dir] = (v.sort || "order-asc").split("-");
      const val = (col) => key === "order" ? Number(col.dataset.order) : Number(col.firstElementChild.dataset[key]);
      cols.slice().sort((a, b) => (val(a) - val(b)) * (dir === "desc" ? -1 : 1)).forEach((col) => grid.appendChild(col));

      countEl.textContent = shown;
      empty.classList.toggle("d-none", shown > 0);
      const active = fields.some((f) => f.value);
      clearBtn.classList.toggle("d-none", !active);

      const qs = new URLSearchParams(fields.filter((f) => f.value).map((f) => [f.name, f.value])).toString();
      history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
    };

    let debounce;
    filterForm.addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(apply, 150); });
    filterForm.addEventListener("change", apply);
    clearBtn.addEventListener("click", () => { fields.forEach((f) => { f.value = ""; }); apply(); });
    apply();

    // Grid / list toggle (remembered per browser).
    const setView = (view) => {
      grid.classList.toggle("list-view", view === "list");
      $$(".view-toggle [data-view]").forEach((b) => {
        const on = b.dataset.view === view;
        b.classList.toggle("active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      try { localStorage.setItem("trekView", view); } catch (_) { /* storage unavailable */ }
    };
    $$(".view-toggle [data-view]").forEach((b) => b.addEventListener("click", () => setView(b.dataset.view)));
    try { setView(localStorage.getItem("trekView") || "grid"); } catch (_) { setView("grid"); }
  }

  /* ------------------------------------------------ Trek detail: carry selected date to checkout */
  const bookBtn = $("#bookNowBtn");
  if (bookBtn) {
    const sync = () => {
      const picked = $('input[name="date"]:checked');
      bookBtn.href = bookBtn.dataset.base + (picked ? `?date=${picked.value}` : "");
    };
    $$('input[name="date"]').forEach((r) => r.addEventListener("change", sync));
    sync();
    bookBtn.addEventListener("click", () => window.gtag?.("event", "begin_checkout", { item_name: document.title }));
  }

  /* ------------------------------------------------ Contact form (AJAX with graceful fallback) */
  const contactForm = $("#contactForm");
  if (contactForm) {
    const alertBox = $("#formAlert");
    const submit = $("#contactSubmit");
    const showAlert = (type, msg) => {
      alertBox.className = `alert alert-${type}`;
      alertBox.textContent = msg;
    };
    const setLoading = (on) => {
      submit.disabled = on;
      $(".spinner-border", submit).classList.toggle("d-none", !on);
    };

    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      $$(".is-invalid", contactForm).forEach((el) => el.classList.remove("is-invalid"));
      if (!contactForm.checkValidity()) {
        $$(":invalid", contactForm).forEach((el) => el.classList.add("is-invalid"));
        $(":invalid", contactForm)?.focus();
        return;
      }
      setLoading(true);
      try {
        const res = await fetch(contactForm.action, {
          method: "POST",
          headers: { "X-Requested-With": "fetch", Accept: "application/json" },
          body: new FormData(contactForm),
        });
        const data = await res.json();
        if (data.ok) {
          showAlert("success", data.message);
          contactForm.reset();
          window.gtag?.("event", "generate_lead", { form: "contact" });
        } else {
          showAlert("danger", data.message);
          Object.keys(data.errors || {}).forEach((name) => contactForm.elements[name]?.classList.add("is-invalid"));
        }
      } catch (err) {
        showAlert("danger", "Network error. Please try again, or contact us on WhatsApp.");
      } finally {
        setLoading(false);
        alertBox.scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
      }
    });
  }

  /* ------------------------------------------------ Home: first-visit enquiry popup */
  const inquiryModalEl = $("#inquiryModal");
  if (inquiryModalEl && window.bootstrap?.Modal) {
    const SEEN_KEY = "inquiryPopupSeen";
    const seen = () => { try { return localStorage.getItem(SEEN_KEY); } catch (_) { return "1"; } };
    const markSeen = () => { try { localStorage.setItem(SEEN_KEY, "1"); } catch (_) { /* storage unavailable */ } };

    if (!seen()) {
      const modal = new bootstrap.Modal(inquiryModalEl);
      inquiryModalEl.addEventListener("hidden.bs.modal", markSeen);
      setTimeout(() => { if (!document.querySelector(".modal.show, .lightbox.open")) modal.show(); }, 2500);

      const form = $("#inquiryForm");
      const alertBox = $("#inquiryAlert");
      const submit = $("#inquirySubmit");
      const showAlert = (type, msg) => {
        alertBox.className = `alert alert-${type}`;
        alertBox.textContent = msg;
      };
      const setLoading = (on) => {
        submit.disabled = on;
        $(".spinner-border", submit).classList.toggle("d-none", !on);
      };

      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        $$(".is-invalid", form).forEach((el) => el.classList.remove("is-invalid"));
        if (!form.checkValidity()) {
          $$(":invalid", form).forEach((el) => el.classList.add("is-invalid"));
          $(":invalid", form)?.focus();
          return;
        }
        setLoading(true);
        try {
          const res = await fetch(form.action, {
            method: "POST",
            headers: { "X-Requested-With": "fetch", Accept: "application/json" },
            body: new FormData(form),
          });
          const data = await res.json();
          if (data.ok) {
            markSeen();
            showAlert("success", data.message);
            form.classList.add("d-none");
            window.gtag?.("event", "generate_lead", { form: "home_popup" });
            setTimeout(() => modal.hide(), 3000);
          } else {
            showAlert("danger", data.message);
            Object.keys(data.errors || {}).forEach((name) => form.elements[name]?.classList.add("is-invalid"));
          }
        } catch (err) {
          showAlert("danger", "Network error. Please try again, or contact us on WhatsApp.");
        } finally {
          setLoading(false);
        }
      });
    }
  }
})();
