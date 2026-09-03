/**
 * cookie-consent.js — a lightweight, GDPR-minded consent banner.
 *
 * Behaviour:
 *  - Shows once per browser until the person makes a choice.
 *  - "Accept all" stores consent for analytics + advertising cookies.
 *  - "Reject non-essential" stores a refusal; only strictly necessary
 *    storage (like the theme preference) continues to be used.
 *  - The choice is saved in localStorage under `cutline:consent` as
 *    { analytics: bool, advertising: bool, timestamp: string }.
 *
 * Wiring analytics/ads to this consent:
 *  Any analytics or ad script (GA4, Clarity, AdSense, etc.) should only be
 *  injected AFTER checking `getConsent().analytics` / `.advertising` — see
 *  the commented example at the bottom of this file and the notes in
 *  /docs/analytics-setup.md.
 */
import { storage } from "./utils.js";

const CONSENT_KEY = "cutline:consent";

export function getConsent() {
  return storage.get(CONSENT_KEY, null);
}

function setConsent(consent) {
  storage.set(CONSENT_KEY, { ...consent, timestamp: new Date().toISOString() });
  document.dispatchEvent(new CustomEvent("cutline:consent-changed", { detail: consent }));
}

export function initCookieConsent() {
  if (getConsent()) return; // already decided

  const banner = document.createElement("div");
  banner.className = "cookie-banner";
  banner.setAttribute("role", "dialog");
  banner.setAttribute("aria-label", "Cookie consent");
  banner.setAttribute("aria-describedby", "cookieBannerText");
  banner.innerHTML = `
    <p id="cookieBannerText">
      We use cookies for essential site function, and — only with your consent —
      for analytics and future advertising. See our
      <a href="/cookie-policy.html" style="color:var(--accent);text-decoration:underline;">Cookie Policy</a>.
    </p>
    <div class="actions">
      <button type="button" class="btn btn-secondary btn-sm" id="cookieRejectBtn">Reject non-essential</button>
      <button type="button" class="btn btn-sm" id="cookieAcceptBtn">Accept all</button>
    </div>
  `;
  document.body.appendChild(banner);

  banner.querySelector("#cookieAcceptBtn").addEventListener("click", () => {
    setConsent({ analytics: true, advertising: true });
    banner.remove();
  });
  banner.querySelector("#cookieRejectBtn").addEventListener("click", () => {
    setConsent({ analytics: false, advertising: false });
    banner.remove();
  });
}

/* -------------------------------------------------------------------------
 * Example (inactive): only load GA4 once analytics consent is granted.
 * Uncomment and add a real Measurement ID to use.
 * -------------------------------------------------------------------------
 *
 * document.addEventListener("cutline:consent-changed", (e) => {
 *   if (e.detail.analytics) {
 *     const s = document.createElement("script");
 *     s.async = true;
 *     s.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX";
 *     document.head.appendChild(s);
 *     window.dataLayer = window.dataLayer || [];
 *     function gtag(){ dataLayer.push(arguments); }
 *     gtag("js", new Date());
 *     gtag("config", "G-XXXXXXXXXX");
 *   }
 * });
 */
