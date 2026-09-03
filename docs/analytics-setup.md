# Analytics, Search Console, AdSense & Clarity setup

This site ships **without** any live tracking or ad code. Every page has a
commented placeholder block right after `<head>` labeled
`ANALYTICS & VERIFICATION PLACEHOLDERS`. To turn a service on, uncomment the
relevant block in **every HTML file** (or, better, extract the `<head>` into
a single include if you introduce a build step) and fill in your own IDs.

Respect cookie consent: `assets/js/cookie-consent.js` records the visitor's
choice and fires a `cutline:consent-changed` event. Analytics and
advertising scripts should only be injected after checking
`getConsent().analytics` / `getConsent().advertising` (see the commented
example at the bottom of that file). This keeps the site GDPR-minded by
default — nothing loads until consent is granted.

## 1. Google Analytics 4 (GA4)

1. Create a GA4 property in [Google Analytics](https://analytics.google.com) and copy your Measurement ID (`G-XXXXXXXXXX`).
2. Uncomment the GA4 block in the placeholder section and replace `G-XXXXXXXXXX`.
3. Preferably gate the script behind analytics consent, as shown in `cookie-consent.js`.

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 2. Google Search Console verification

Fastest option: an HTML `<meta>` tag (already stubbed, commented, in every page's `<head>`):

```html
<meta name="google-site-verification" content="YOUR_VERIFICATION_CODE" />
```

Alternatively upload the HTML verification file Search Console gives you to
the site root — this static structure supports that with no changes.

Once verified, submit `sitemap.xml` from the Search Console "Sitemaps" panel.

## 3. Google AdSense verification & ad units

1. Apply at [Google AdSense](https://www.google.com/adsense/). Add the
   verification `<meta>` tag (stubbed, commented) or the `ads.txt` file AdSense
   provides to the site root.
2. This project reserves ad space with `.ad-slot` containers (`--banner`,
   `--incontent`, `--sidebar`, `--footer`) so approved ad units can be
   dropped in without shifting the layout. Replace the placeholder `<div>`
   inside each `.ad-slot` with your AdSense `<ins>` snippet once approved.
3. Do not enable ad code before AdSense approval — placeholders are
   intentionally inert divs, not `<ins class="adsbygoogle">` tags, so the
   site can be reviewed cleanly.

## 4. Microsoft Clarity

1. Create a project at [clarity.microsoft.com](https://clarity.microsoft.com) and copy your project ID.
2. Uncomment the Clarity block in the placeholder section and replace `CLARITY_PROJECT_ID`.

```html
<script>
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "CLARITY_PROJECT_ID");
</script>
```

## 5. Google Tag Manager (optional, in place of individual snippets)

If you'd rather manage all tags (GA4, Clarity, ads) from one place, use GTM
instead of the individual snippets above:

```html
<!-- In <head> -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>

<!-- Right after <body> -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
```

## Checklist before going live

- [ ] Replace `https://cutline-background-remover.vercel.app` throughout (HTML, `sitemap.xml`, `robots.txt`) with your real domain.
- [ ] Add a real `assets/images/og-cover.jpg` (1200×630) social preview image.
- [ ] Fill in GA4 / Clarity / GTM IDs and verification `<meta>` tags, or remove the commented blocks entirely if unused.
- [ ] Apply for AdSense only once the site has real, substantial content live (this project ships five original blog posts plus the full policy pages AdSense reviewers expect).
- [ ] After AdSense approval, replace the placeholder `<div>` inside each `.ad-slot` with the provided `<ins class="adsbygoogle">` snippet, and load `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js` per AdSense's instructions.
- [ ] Re-run Lighthouse after adding real ad code — third-party ad scripts are the most common cause of Core Web Vitals regressions.
