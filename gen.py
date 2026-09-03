#!/usr/bin/env python3
"""
gen.py — builds every HTML page in the site from shared partials so the
header, footer, nav, ad slots, and analytics placeholders stay identical
everywhere. This script is a one-off authoring tool; the OUTPUT is plain
static HTML with no build step required to deploy it.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://cutline.example.com"

# ---------------------------------------------------------------------------
# Shared partials
# ---------------------------------------------------------------------------

ANALYTICS_PLACEHOLDER = """
<!-- ================= ANALYTICS & VERIFICATION PLACEHOLDERS =================
     Nothing below is active. See /docs/analytics-setup.md before enabling
     any of these, and gate analytics/ad scripts behind cookie consent
     (assets/js/cookie-consent.js) for GDPR-minded behaviour.

<meta name="google-site-verification" content="YOUR_SEARCH_CONSOLE_CODE" />
<meta name="google-adsense-account" content="ca-pub-XXXXXXXXXXXXXXXX" />

<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>

<script>
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "CLARITY_PROJECT_ID");
</script>
================================================================================ -->
"""

def head(title, description, path, keywords=None, extra_jsonld="", og_type="website"):
    canonical = f"{SITE}{path}"
    kw = f'<meta name="keywords" content="{keywords}">' if keywords else ""
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
{kw}
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="CutLine">
{ANALYTICS_PLACEHOLDER}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="CutLine">
<meta property="og:image" content="{SITE}/assets/images/og-cover.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/assets/images/og-cover.jpg">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#fbfbfa">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/css/styles.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
{extra_jsonld}"""

def nav(active):
    def link(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    links = [
        link("/#workspace", "Remove background", "home"),
        link("/blog.html", "Blog", "blog"),
        link("/faq.html", "FAQ", "faq"),
        link("/about.html", "About", "about"),
        link("/contact.html", "Contact", "contact"),
    ]
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="brand" aria-label="CutLine home">
      <svg class="brand-mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <rect width="32" height="32" rx="9" fill="var(--indigo-500)"/>
        <path d="M8 20c3-6 5-9 8-9s5 3 8 9" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="3 3"/>
      </svg>
      CutLine
    </a>
    <nav class="main-nav" id="mainNav" aria-label="Primary">
      {links[0]}
      {links[1]}
      {links[2]}
      {links[3]}
      {links[4]}
    </nav>
    <div class="header-actions">
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle dark mode" aria-pressed="false">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z"/></svg>
      </button>
      <a href="/#workspace" class="btn btn-sm">Remove background</a>
      <button class="nav-toggle" id="navToggle" type="button" aria-label="Toggle menu" aria-expanded="false" aria-controls="mainNav">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" class="brand" style="margin-bottom:.6rem;display:inline-flex;">
          <svg class="brand-mark" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect width="32" height="32" rx="9" fill="var(--indigo-500)"/><path d="M8 20c3-6 5-9 8-9s5 3 8 9" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="3 3"/></svg>
          CutLine
        </a>
        <p style="max-width:34ch;">A private, on-device AI background remover. Your photos never leave your browser.</p>
        <div class="footer-social">
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="CutLine on X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.8l-5.3-6.9L4.8 22H1.7l8.1-9.3L1 2h7l4.8 6.3L18.9 2Z"/></svg></a>
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="CutLine on Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1"/></svg></a>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" aria-label="CutLine on GitHub"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.03a9.4 9.4 0 0 1 5 0c1.91-1.3 2.75-1.03 2.75-1.03.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.75c0 .26.18.58.69.48A10 10 0 0 0 12 2Z"/></svg></a>
        </div>
      </div>
      <div>
        <h5>Product</h5>
        <ul>
          <li><a href="/#workspace">Remove background</a></li>
          <li><a href="/#features">Features</a></li>
          <li><a href="/#how-it-works">How it works</a></li>
          <li><a href="/blog.html">Blog</a></li>
        </ul>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="/about.html">About</a></li>
          <li><a href="/contact.html">Contact</a></li>
          <li><a href="/faq.html">FAQ</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h5>Legal</h5>
        <ul>
          <li><a href="/privacy.html">Privacy policy</a></li>
          <li><a href="/terms.html">Terms &amp; conditions</a></li>
        </ul>
      </div>
      <div>
        <h5>&nbsp;</h5>
        <ul>
          <li><a href="/disclaimer.html">Disclaimer</a></li>
          <li><a href="/cookie-policy.html">Cookie policy</a></li>
        </ul>
      </div>
    </div>
    <div class="ad-slot ad-slot--footer" aria-label="Advertisement placeholder"></div>
    <div class="footer-bottom">
      <span>&copy; 2026 CutLine. All rights reserved.</span>
      <span>Made for people who just need the background gone.</span>
    </div>
  </div>
</footer>"""

def scripts(extra=""):
    return f"""<script type="module">
  import {{ initTheme }} from "/assets/js/theme.js";
  import {{ initNav }} from "/assets/js/nav.js";
  import {{ initCookieConsent }} from "/assets/js/cookie-consent.js";
  initTheme();
  initNav();
  initCookieConsent();
</script>
{extra}"""

def breadcrumb(items):
    """items: list of (label, href_or_None_for_current)"""
    lis = []
    ld_items = []
    for i, (label, href) in enumerate(items, start=1):
        if href:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            lis.append(f"<li>{label}</li>")
        ld_items.append({
            "@type": "ListItem", "position": i, "name": label,
            "item": f"{SITE}{href}" if href else f"{SITE}{items[-1][1] or ''}"
        })
    html = f'<ol class="breadcrumb">{"".join(lis)}</ol>'
    return html

def breadcrumb_jsonld(items):
    import json
    entries = []
    for i, (label, href) in enumerate(items, start=1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = f"{SITE}{href}"
        entries.append(entry)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": entries}
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'

AD_BANNER = '<div class="ad-slot ad-slot--banner" role="complementary" aria-label="Advertisement placeholder"></div>'
AD_INCONTENT = '<div class="ad-slot ad-slot--incontent" role="complementary" aria-label="Advertisement placeholder"></div>'
AD_SIDEBAR = '<div class="ad-slot ad-slot--sidebar" role="complementary" aria-label="Advertisement placeholder"></div>'

def page(title, description, path, body, active=None, keywords=None, extra_jsonld="", extra_scripts="", body_id="main"):
    return f"""<!doctype html>
<html lang="en">
<head>
{head(title, description, path, keywords, extra_jsonld)}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{nav(active)}
<main id="{body_id}">
{body}
</main>
{FOOTER}
{scripts(extra_scripts)}
</body>
</html>
"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)
