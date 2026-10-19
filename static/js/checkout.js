/*
 * Checkout flow
 *   1. POST /api/payment/order   -> server validates and calculates the amount, creates the order
 *   2. Razorpay Checkout popup   -> customer pays (skipped in demo mode)
 *   3. POST /api/payment/verify  -> server verifies the signature and notifies the admin team
 *
 * Stripe alternative: have /api/payment/order create a Stripe Checkout Session
 * and redirect with `window.location = session.url` instead of opening Razorpay.
 */
(() => {
  "use strict";
  const form = document.getElementById("checkoutForm");
  if (!form) return;

  const cfg = form.dataset;
  const price = Number(cfg.price);
  const live = cfg.live === "true";
  const pax = document.getElementById("cPax");
  const payBtn = document.getElementById("payBtn");
  const alertBox = document.getElementById("checkoutAlert");
  const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

  const clampPax = () => {
    const max = Number(pax.max) || 20;
    pax.value = Math.min(max, Math.max(1, parseInt(pax.value, 10) || 1));
  };
  // Selected add-ons and tent upgrade. The server recalculates the real amount.
  const chosenExtras = () => [...form.querySelectorAll('input[name="addons"]:checked, input[name="tent"]:checked')]
    .filter((el) => Number(el.dataset.price) > 0);
  const perPerson = () => price + chosenExtras().reduce((sum, el) => sum + Number(el.dataset.price), 0);
  const updateSummary = () => {
    const extras = chosenExtras();
    const extrasTotal = perPerson() - price;
    document.getElementById("sumAddonsRow")?.classList.toggle("d-none", !extras.length);
    if (extras.length) {
      document.getElementById("sumAddons").textContent = inr.format(extrasTotal);
      document.getElementById("sumAddonsList").textContent = extras.map((el) => el.dataset.name).join(", ");
    }
    document.getElementById("sumPax").textContent = pax.value;
    document.getElementById("sumTotal").textContent = inr.format(perPerson() * Number(pax.value));
  };
  form.querySelectorAll('input[name="addons"], input[name="tent"]').forEach((el) => el.addEventListener("change", updateSummary));
  form.querySelectorAll("[data-step]").forEach((btn) => btn.addEventListener("click", () => {
    pax.value = Number(pax.value) + Number(btn.dataset.step);
    clampPax();
    updateSummary();
  }));
  pax.addEventListener("change", () => { clampPax(); updateSummary(); });
  pax.addEventListener("input", updateSummary);

  const setLoading = (on) => {
    payBtn.disabled = on;
    payBtn.querySelector(".spinner-border").classList.toggle("d-none", !on);
  };
  const fail = (msg) => {
    alertBox.textContent = msg;
    alertBox.classList.remove("d-none");
    alertBox.scrollIntoView({ block: "center" });
    setLoading(false);
  };
  const postJSON = async (url, body) => {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(body),
    });
    return res.json();
  };

  const verify = async (payload, notes) => {
    const result = await postJSON("/api/payment/verify", { ...payload, notes });
    if (!result.ok) return fail(result.message || "Payment could not be verified. Please contact us.");
    document.getElementById("paymentId").textContent = result.payment_id;
    document.getElementById("checkoutCard").classList.add("d-none");
    document.getElementById("successCard").classList.remove("d-none");
    payBtn.classList.add("d-none");
    window.gtag?.("event", "purchase", { currency: "INR", value: perPerson() * Number(pax.value), items: [{ item_name: cfg.trek }] });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    alertBox.classList.add("d-none");
    form.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));
    clampPax();
    if (!form.checkValidity()) {
      form.querySelectorAll(":invalid").forEach((el) => el.classList.add("is-invalid"));
      form.querySelector(":invalid")?.focus();
      return;
    }
    setLoading(true);

    const fd = new FormData(form);
    const customer = { name: fd.get("name"), email: fd.get("email"), phone: fd.get("phone") };
    let order;
    try {
      order = await postJSON("/api/payment/order", {
        slug: cfg.slug, date: fd.get("date"), participants: Number(fd.get("participants")), ...customer,
        addons: fd.getAll("addons"), tent: fd.get("tent") || "",
      });
    } catch (err) {
      return fail("Network error. Please try again.");
    }
    if (!order.ok) return fail(order.message);

    // Demo mode: simulate a successful payment so the full flow can be tested.
    if (order.demo) {
      setTimeout(() => verify({
        razorpay_order_id: order.order_id,
        razorpay_payment_id: `pay_DEMO${Date.now()}`,
        razorpay_signature: "demo",
      }, order.notes).catch(() => fail("Network error. Please try again.")), 900);
      return;
    }

    if (!live || typeof window.Razorpay !== "function") {
      return fail("Payment gateway failed to load. Please refresh and try again.");
    }
    const rzp = new window.Razorpay({
      key: order.key || cfg.key,
      amount: order.amount,
      currency: order.currency,
      order_id: order.order_id,
      name: cfg.site,
      description: `${cfg.trek} – ${fd.get("participants")} participant(s)`,
      prefill: { name: customer.name, email: customer.email, contact: customer.phone },
      notes: order.notes,
      theme: { color: "#14532d" },
      handler: (response) => verify(response, order.notes).catch(() => fail("Could not confirm payment. Please contact us with your payment ID.")),
      modal: { ondismiss: () => setLoading(false) },
    });
    rzp.on("payment.failed", (resp) => fail(resp.error?.description || "Payment failed. Please try again."));
    rzp.open();
  });

  updateSummary();
})();
