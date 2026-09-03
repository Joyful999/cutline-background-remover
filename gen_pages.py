#!/usr/bin/env python3
from gen import page, write, breadcrumb, breadcrumb_jsonld, AD_BANNER, AD_INCONTENT, AD_SIDEBAR, SITE
import json

# ===========================================================================
# HOME / index.html
# ===========================================================================
INDEX_BODY = """
  <!-- HERO / WORKSPACE -->
  <section class="hero" id="workspace" aria-labelledby="hero-heading">
    <div class="container">
      <div class="hero-inner">
        <span class="eyebrow">On-device AI &middot; No uploads &middot; No watermark</span>
        <h1 id="hero-heading">Cut the background out.<br><em>Keep the moment in.</em></h1>
        <p class="lead">Drop a photo below and CutLine's on-device AI lifts the subject out in seconds &mdash; right here in your browser. Nothing is sent to a server.</p>
      </div>

      <div class="workspace">
        <!-- Upload dropzone (shown when there is no active image) -->
        <div class="dropzone" id="dropzone" tabindex="0" role="button" aria-describedby="dropzoneHint">
          <div class="marching-ants" aria-hidden="true"></div>
          <svg class="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
            <path d="M12 16V4M12 4l-4 4M12 4l4 4"/><path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>
          </svg>
          <h3>Drag &amp; drop an image, or click to browse</h3>
          <p class="hint" id="dropzoneHint">Process one photo or an entire batch at once. Everything happens on your device.</p>
          <div class="format-chips">
            <span class="chip">PNG</span><span class="chip">JPG</span><span class="chip">JPEG</span><span class="chip">WebP</span>
          </div>
          <input type="file" id="fileInput" accept="image/png,image/jpeg,image/webp" multiple aria-label="Choose image files">
        </div>

        <!-- Editor (shown once at least one image is loaded) -->
        <div class="editor" id="editor">
          <div class="canvas-stage">
            <div class="stage-toolbar" role="toolbar" aria-label="Image tools">
              <button class="btn btn-sm" id="removeBgBtn" type="button">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;" aria-hidden="true"><path d="M12 2l3 6 6 1-4.5 4.4 1 6.1L12 16l-5.5 3.5 1-6.1L3 8l6-1z"/></svg>
                Remove background
              </button>
              <span class="sep"></span>
              <div class="view-tabs" role="tablist" aria-label="Preview mode">
                <button type="button" role="tab" data-view="transparent" class="active" aria-selected="true">Transparent</button>
                <button type="button" role="tab" data-view="compare" aria-selected="false">Compare</button>
                <button type="button" role="tab" data-view="side" aria-selected="false">Side-by-side</button>
              </div>
              <span class="sep"></span>
              <button class="btn btn-icon btn-secondary" id="zoomOutBtn" type="button" aria-label="Zoom out">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M8 11h6"/></svg>
              </button>
              <button class="btn btn-icon btn-secondary" id="zoomInBtn" type="button" aria-label="Zoom in">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/></svg>
              </button>
              <button class="btn btn-icon btn-secondary" id="fitBtn" type="button" aria-label="Fit to screen">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>
              </button>
              <span class="sep"></span>
              <button class="btn btn-icon btn-secondary" id="rotateBtn" type="button" aria-label="Rotate 90 degrees">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 1 3 6.7"/><path d="M3 21v-6h6"/></svg>
              </button>
              <button class="btn btn-icon btn-secondary" id="flipHBtn" type="button" aria-label="Flip horizontally">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v18M6 7l-2 2 2 2M18 7l2 2-2 2M6 17l-2-2 2-2M18 17l2-2-2-2"/></svg>
              </button>
              <button class="btn btn-icon btn-secondary" id="cropBtn" type="button" aria-label="Toggle crop">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2v14a2 2 0 0 0 2 2h14M18 22V8a2 2 0 0 0-2-2H2"/></svg>
              </button>
              <span class="sep"></span>
              <button class="btn btn-icon btn-secondary" id="undoBtn" type="button" aria-label="Undo">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a5 5 0 0 1 0 10h-1"/></svg>
              </button>
              <button class="btn btn-icon btn-secondary" id="redoBtn" type="button" aria-label="Redo">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 14l4-4-4-4"/><path d="M19 10h-9a5 5 0 0 0 0 10h1"/></svg>
              </button>
              <span class="sep"></span>
              <button class="btn btn-secondary btn-sm" id="startOverBtn" type="button">Start over</button>
            </div>

            <div class="stage-canvas-wrap" id="stageWrap">
              <div id="transparentView" style="width:100%;height:100%;display:grid;place-items:center;">
                <canvas id="mainCanvas"></canvas>
              </div>
              <div id="sideView" style="width:100%;height:100%;display:none;grid-template-columns:1fr 1fr;place-items:center;">
                <canvas id="sideBeforeCanvas"></canvas>
                <canvas id="sideAfterCanvas"></canvas>
              </div>
              <div class="compare-slider-wrap" id="compareView">
                <div class="compare-after"><canvas id="compareAfterCanvas"></canvas></div>
                <div class="compare-before" id="compareBeforeLayer"><canvas id="compareBeforeCanvas"></canvas></div>
                <div class="compare-handle" id="compareHandle"></div>
              </div>

              <div class="stage-skeleton" id="stageSkeleton" aria-hidden="true"></div>
              <div class="progress-overlay" id="idleCtaOverlay">
                <button class="btn" id="removeBgBtnOverlay" type="button">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:17px;height:17px;" aria-hidden="true"><path d="M12 2l3 6 6 1-4.5 4.4 1 6.1L12 16l-5.5 3.5 1-6.1L3 8l6-1z"/></svg>
                  Remove background
                </button>
              </div>
              <div class="progress-overlay" id="progressOverlay" role="status" aria-live="polite">
                <div class="spinner" aria-hidden="true"></div>
                <div class="progress-bar-track"><div class="progress-bar-fill" id="progressFill"></div></div>
                <span class="progress-label" id="progressLabel">Loading AI engine&hellip;</span>
              </div>
            </div>

            <div class="batch-strip" id="batchStrip" aria-label="Batch queue"></div>
          </div>

          <aside class="side-panel" aria-label="Image editing options">
            <div class="panel-section">
              <h4>Image info</h4>
              <div class="info-grid mono">
                <div class="k">Width</div><div class="v" id="infoWidth">&mdash;</div>
                <div class="k">Height</div><div class="v" id="infoHeight">&mdash;</div>
                <div class="k">Size</div><div class="v" id="infoSize">&mdash;</div>
                <div class="k">Format</div><div class="v" id="infoFormat">&mdash;</div>
              </div>
            </div>

            <div class="panel-section">
              <h4>Background</h4>
              <div class="bg-options">
                <div class="bg-tabs" role="tablist" aria-label="Background type">
                  <button type="button" data-bg="transparent" class="active">None</button>
                  <button type="button" data-bg="color">Color</button>
                  <button type="button" data-bg="gradient">Gradient</button>
                  <button type="button" data-bg="image">Image</button>
                  <button type="button" data-bg="blur">Blur</button>
                </div>
                <div id="bgColorPanel" style="display:none;">
                  <div class="swatches" id="colorSwatches"></div>
                  <div class="range-row" style="margin-top:.6rem;">
                    <span>Custom</span><input type="color" id="customColor" value="#ffffff">
                  </div>
                </div>
                <div id="bgGradientPanel" style="display:none;">
                  <div class="gradient-list" id="gradientSwatches"></div>
                </div>
                <div id="bgImagePanel" style="display:none;">
                  <button class="upload-bg-btn" id="uploadBgBtn" type="button">Upload a background image&hellip;</button>
                  <input type="file" id="bgImageInput" accept="image/png,image/jpeg,image/webp" class="sr-only">
                </div>
                <div id="bgBlurPanel" style="display:none;">
                  <div class="range-row">
                    <span>Blur</span>
                    <input type="range" id="blurRange" min="2" max="30" value="14">
                    <output id="blurValue">14</output>
                  </div>
                </div>
              </div>
            </div>

            <div class="panel-section">
              <h4>Refine edges</h4>
              <div class="refine-row" style="margin-bottom:.7rem;">
                <label for="edgeSmoothToggle" style="font-size:.86rem;">Edge smoothing &amp; hair refinement</label>
                <label class="switch">
                  <input type="checkbox" id="edgeSmoothToggle" checked>
                  <span class="track"></span><span class="thumb"></span>
                </label>
              </div>
              <div class="range-row">
                <span>Feather</span>
                <input type="range" id="featherRange" min="0" max="12" value="1">
                <output id="featherValue">1px</output>
              </div>
            </div>

            <div class="panel-section">
              <h4>Download</h4>
              <div class="download-menu">
                <div class="actions-row">
                  <button class="btn" id="downloadPngBtn" type="button">Transparent PNG</button>
                </div>
                <div class="actions-row">
                  <button class="btn btn-secondary" id="downloadJpgBtn" type="button">JPG</button>
                  <button class="btn btn-secondary" id="downloadWebpBtn" type="button">WebP</button>
                </div>
                <button class="btn btn-secondary" id="processAllBtn" type="button">Process all in batch</button>
              </div>
            </div>

            <div class="panel-section" id="historySection">
              <h4>Recent history</h4>
              <div class="batch-strip" id="historyStrip" aria-label="Recent processing history"></div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  </section>

  <div class="container">""" + AD_BANNER + """</div>

  <!-- FEATURES -->
  <section class="section" id="features" aria-labelledby="features-heading">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Why CutLine</span>
        <h2 id="features-heading">Built like a professional editing tool, not a toy.</h2>
        <p>Every core feature you'd expect from a paid background remover, running for free in your browser.</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2l3 6 6 1-4.5 4.4 1 6.1L12 16l-5.5 3.5 1-6.1L3 8l6-1z"/></svg>
          <h3>On-device AI cutouts</h3>
          <p>A neural segmentation model runs locally via WebAssembly &mdash; your photos are never uploaded anywhere.</p>
        </article>
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M3 15l5-5 4 4 5-6 4 5"/></svg>
          <h3>Batch processing</h3>
          <p>Queue up dozens of photos and let CutLine work through them one after another.</p>
        </article>
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 6h16M4 12h10M4 18h7"/></svg>
          <h3>Full editing toolkit</h3>
          <p>Crop, rotate, flip, feather edges, and swap in a solid color, gradient, blur, or custom background.</p>
        </article>
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 12h4l3-9 4 18 3-9h6"/></svg>
          <h3>Before &amp; after compare</h3>
          <p>Drag a live slider between the original and the cutout to check edge quality at a glance.</p>
        </article>
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3v12M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>
          <h3>Export options</h3>
          <p>Download a transparent PNG, a flattened JPG, or an optimized WebP &mdash; whichever your project needs.</p>
        </article>
        <article class="feature-card">
          <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 2v10l7 4"/></svg>
          <h3>Recent history</h3>
          <p>Your last few cutouts stay in this browser so you can revisit or re-download them later.</p>
        </article>
      </div>
    </div>
  </section>

  <div class="container">""" + AD_INCONTENT + """</div>

  <!-- HOW IT WORKS -->
  <section class="section" id="how-it-works" aria-labelledby="how-heading" style="padding-top:0;">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Three steps</span>
        <h2 id="how-heading">From photo to cutout in seconds.</h2>
      </div>
      <div class="steps">
        <div class="step">
          <h3>Add your photo</h3>
          <p>Drag it in, click to browse, or drop a whole batch at once. JPG, PNG, and WebP are all supported.</p>
        </div>
        <div class="step">
          <h3>Let the AI work</h3>
          <p>CutLine segments the subject on your device and lifts it onto a transparent layer.</p>
        </div>
        <div class="step">
          <h3>Refine &amp; export</h3>
          <p>Swap in a new background, fine-tune the edges, then download the format you need.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="cta-heading">
    <div class="container">
      <div class="cta-band">
        <h2 id="cta-heading">Your next cutout is thirty seconds away.</h2>
        <p>No sign-up. No credit card. No watermark.</p>
        <a href="#workspace" class="btn btn-secondary">Remove a background now</a>
      </div>
    </div>
  </section>
"""

INDEX_JSONLD = f"""<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "CutLine",
  "url": f"{SITE}/",
  "applicationCategory": "PhotoEditingApplication",
  "operatingSystem": "Any (runs in a web browser)",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
  "description": "AI-powered background remover that runs entirely in the browser. Remove and replace backgrounds with colors, gradients, or custom images \u2014 no uploads, no account required.",
  "featureList": [
    "AI background removal", "Transparent PNG export",
    "Background replacement with color, gradient, or image",
    "Batch processing", "Crop, rotate, and flip",
    "Before and after comparison slider"
  ]
}, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org", "@type": "Organization",
  "name": "CutLine", "url": f"{SITE}/", "logo": f"{SITE}/assets/icons/favicon.svg"
}, indent=2)}
</script>"""

write("index.html", page(
    "CutLine \u2014 Free AI Background Remover (Runs in Your Browser)",
    "Remove image backgrounds instantly with on-device AI. No uploads to a server, no account, no watermark. Replace backgrounds with colors, gradients, or your own photo \u2014 free in your browser.",
    "/",
    INDEX_BODY,
    active="home",
    keywords="background remover, remove background, ai background removal, transparent png, photo editor, remove.bg alternative, clipdrop alternative",
    extra_jsonld=INDEX_JSONLD,
    extra_scripts='<script type="module" src="/assets/js/main.js"></script>',
))

print("index.html written by gen_pages.py")

# ===========================================================================
# ABOUT
# ===========================================================================
ABOUT_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("About", None)])}
      <span class="eyebrow">About CutLine</span>
      <h1>A background remover that keeps your photos to itself.</h1>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container prose">
      <p>Most background removers work the same way: your photo travels to a server, a model runs somewhere in a data center, and a result comes back. CutLine skips that trip entirely. The segmentation model runs directly in your browser using WebAssembly, so the image never leaves the device you're using.</p>

      <h2>Why we built it this way</h2>
      <p>We wanted a tool we'd be comfortable using on client work, family photos, and anything in between &mdash; without wondering where a copy of the image ended up. Running the model locally also means there's no queue, no rate limit, and no dependency on a backend staying online.</p>

      {AD_INCONTENT}

      <h2>How the cutout works</h2>
      <p>When you drop in a photo, CutLine loads a compact image-segmentation model and asks it to separate the subject from everything behind it. The result is a mask that gets applied to your original photo, producing a transparent PNG. From there you can leave the background transparent, swap in a solid color or gradient, drop in your own image, or blur the original scene behind the subject.</p>

      <h2>What "on-device" means in practice</h2>
      <ul>
        <li>Your image is decoded and processed using your device's CPU or GPU, not a remote one.</li>
        <li>No image data is transmitted to CutLine or any third party during processing.</li>
        <li>Recent history thumbnails are stored only in your browser's local storage, and only on the device you used.</li>
        <li>The app itself &mdash; the HTML, styles, and scripts &mdash; is a static site, so it can run from any standard web host.</li>
      </ul>

      <h2>Who it's for</h2>
      <p>Online sellers cleaning up product photos, designers building mockups, students prepping presentation graphics, or anyone who just needs one photo without its background &mdash; CutLine is built to make that a thirty-second task rather than a multi-tab ordeal.</p>
    </div>
  </section>
"""

write("about.html", page(
    "About CutLine \u2014 On-Device AI Background Removal",
    "CutLine removes image backgrounds entirely on your device using a local AI model. Learn how it works and why nothing is uploaded to a server.",
    "/about.html", ABOUT_BODY, active="about",
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("About", "/about.html")]),
))

# ===========================================================================
# CONTACT
# ===========================================================================
CONTACT_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Contact", None)])}
      <span class="eyebrow">Get in touch</span>
      <h1>Questions, feedback, or something broken?</h1>
      <p class="lead">Send a message and we'll get back to you.</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container contact-grid">
      <form id="contactForm" novalidate aria-describedby="formStatus">
        <div class="field">
          <label for="name">Name</label>
          <input type="text" id="name" name="name" autocomplete="name" required aria-required="true">
          <span class="field-error" id="nameError"></span>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" autocomplete="email" required aria-required="true">
          <span class="field-error" id="emailError"></span>
        </div>
        <div class="field">
          <label for="topic">Topic</label>
          <select id="topic" name="topic" required aria-required="true" style="padding:.7em .9em;border-radius:14px;border:1px solid var(--surface-border);background:var(--surface);color:var(--text-1);">
            <option value="">Choose one</option>
            <option value="bug">Report a bug</option>
            <option value="feature">Feature request</option>
            <option value="privacy">Privacy question</option>
            <option value="advertising">Advertising / sponsorship</option>
            <option value="other">Something else</option>
          </select>
        </div>
        <div class="field">
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="6" required aria-required="true"></textarea>
          <span class="field-error" id="messageError"></span>
        </div>
        <button class="btn" type="submit">Send message</button>
        <p id="formStatus" role="status" aria-live="polite" style="margin-top:.9rem;font-size:.9rem;"></p>
      </form>

      <div class="prose">
        <h2 style="margin-top:0;">Other ways to reach us</h2>
        <p>For anything time-sensitive, email is fastest: <a href="mailto:hello@cutline.example.com">hello@cutline.example.com</a>.</p>
        <h2>Before you write in</h2>
        <p>If your question is about how the background removal works or what data is stored, the <a href="/about.html">about page</a>, <a href="/faq.html">FAQ</a>, and <a href="/privacy.html">privacy policy</a> answer most of it directly.</p>
      </div>
    </div>
  </section>
"""

CONTACT_SCRIPT = """<script type="module">
  const form = document.getElementById("contactForm");
  const status = document.getElementById("formStatus");

  function setError(fieldId, errorId, message) {
    const field = document.getElementById(fieldId);
    const error = document.getElementById(errorId);
    if (message) {
      field.setAttribute("aria-invalid", "true");
      error.textContent = message;
    } else {
      field.removeAttribute("aria-invalid");
      error.textContent = "";
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let valid = true;

    const name = document.getElementById("name").value.trim();
    if (!name) { setError("name", "nameError", "Enter your name."); valid = false; }
    else setError("name", "nameError", "");

    const email = document.getElementById("email").value.trim();
    const emailOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
    if (!emailOk) { setError("email", "emailError", "Enter a valid email address."); valid = false; }
    else setError("email", "emailError", "");

    const message = document.getElementById("message").value.trim();
    if (message.length < 10) { setError("message", "messageError", "Message should be at least 10 characters."); valid = false; }
    else setError("message", "messageError", "");

    if (!valid) {
      status.textContent = "Please fix the highlighted fields.";
      return;
    }

    status.textContent = "Thanks \u2014 your message has been noted. We'll reply by email.";
    form.reset();
  });
</script>"""

write("contact.html", page(
    "Contact CutLine",
    "Get in touch with the CutLine team with questions, feedback, or bug reports.",
    "/contact.html", CONTACT_BODY, active="contact",
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Contact", "/contact.html")]),
    extra_scripts=CONTACT_SCRIPT,
))

print("about + contact written")

# ===========================================================================
# PRIVACY POLICY
# ===========================================================================
PRIVACY_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Privacy Policy", None)])}
      <span class="eyebrow">Legal</span>
      <h1>Privacy policy</h1>
      <p class="legal-updated">Last updated: July 28, 2026</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container prose">
      <p>This policy explains what happens to your images and other data when you use CutLine at this domain. The short version: your photos are processed on your own device and are not uploaded to us.</p>

      <h2>Image processing</h2>
      <p>When you add a photo, it is decoded and processed locally in your browser using an on-device AI model. CutLine does not transmit the image, the resulting cutout, or any pixel data to our servers or to any third party as part of the background-removal feature.</p>

      <h2>What's stored locally</h2>
      <ul>
        <li><strong>Theme preference</strong> &mdash; whether you last used light or dark mode.</li>
        <li><strong>Cookie consent choice</strong> &mdash; whether you accepted or rejected optional cookies.</li>
        <li><strong>Recent history thumbnails</strong> &mdash; small, low-resolution previews of your last few cutouts.</li>
        <li>All of the above are stored in your browser's localStorage on your device only; none of it is sent to us.</li>
      </ul>

      {AD_INCONTENT}

      <h2>Cookies, analytics, and future advertising</h2>
      <p>This site is built to support optional analytics (such as Google Analytics 4 and Microsoft Clarity) and, in the future, contextual advertising through Google AdSense. Where those services are enabled, they may set their own cookies or similar identifiers to measure site usage or serve ads, and may collect information such as your IP address, browser type, device type, and pages visited.</p>
      <p>These services are only active where indicated in our <a href="/cookie-policy.html">Cookie Policy</a>, and only after you make a choice in the cookie consent banner shown on your first visit. You can change your choice at any time by clearing your browser's site data for this domain.</p>
      <p>If and when advertising is enabled, ads may be personalized based on your visit to this and other sites. You can opt out of personalized advertising through <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer">Google's Ads Settings</a> or via industry tools such as the <a href="https://optout.aboutads.info" target="_blank" rel="noopener noreferrer">DAA opt-out page</a>.</p>

      <h2>Third-party resources</h2>
      <p>The page loads its typefaces and the background-removal model library from third-party content delivery networks. Those requests are subject to the respective provider's own policies, and &mdash; like any web request &mdash; include standard connection information such as your IP address and browser type.</p>

      <h2>Contact form</h2>
      <p>If you use the contact form on this site, the information you submit is used only to respond to your message.</p>

      <h2>Children's privacy</h2>
      <p>This site is not directed at children under 13, and we do not knowingly collect personal information from children.</p>

      <h2>Changes to this policy</h2>
      <p>If this policy changes, the "last updated" date above will change too. We recommend checking back if you rely on the specifics for your own compliance needs.</p>

      <h2>Questions</h2>
      <p>Reach out through the <a href="/contact.html">contact page</a> with any privacy questions.</p>
    </div>
  </section>
"""

write("privacy.html", page(
    "Privacy Policy \u2014 CutLine",
    "CutLine processes images entirely on your device. Read exactly what data is stored locally, how analytics and advertising cookies work, and what, if anything, is transmitted.",
    "/privacy.html", PRIVACY_BODY, active=None,
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Privacy Policy", "/privacy.html")]),
))

# ===========================================================================
# TERMS & CONDITIONS
# ===========================================================================
TERMS_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Terms & Conditions", None)])}
      <span class="eyebrow">Legal</span>
      <h1>Terms &amp; conditions</h1>
      <p class="legal-updated">Last updated: July 28, 2026</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container prose">
      <p>These terms cover your use of CutLine (the "service"). By using the site, you agree to the points below.</p>

      <h2>The service</h2>
      <p>CutLine provides browser-based tools for removing and replacing image backgrounds. Processing runs on your own device; we do not review, store, or claim any rights over the images you process.</p>

      <h2>Your content</h2>
      <p>You retain all rights to the photos you process with CutLine. You're responsible for making sure you have the right to use and edit any image you upload &mdash; including photos of other people, copyrighted artwork, or licensed material.</p>

      {AD_INCONTENT}

      <h2>Acceptable use</h2>
      <ul>
        <li>Don't use the service to process content that is illegal, infringing, or that you don't have permission to use.</li>
        <li>Don't attempt to disrupt, reverse engineer for malicious purposes, or overload the service.</li>
      </ul>

      <h2>Advertising</h2>
      <p>CutLine may display advertising served by third-party networks such as Google AdSense, once approved. Ads are subject to the advertiser's own terms; we do not control the content of individual ads.</p>

      <h2>No warranty</h2>
      <p>CutLine is provided "as is." AI-based background removal is not perfect &mdash; results can vary depending on the photo, lighting, and subject. We make no guarantee of a particular level of accuracy. See also our <a href="/disclaimer.html">Disclaimer</a>.</p>

      <h2>Limitation of liability</h2>
      <p>To the extent permitted by law, CutLine and its operators are not liable for indirect, incidental, or consequential damages arising from use of the service.</p>

      <h2>Changes</h2>
      <p>We may update these terms from time to time. Continued use of the service after changes take effect means you accept the revised terms.</p>

      <h2>Contact</h2>
      <p>Questions about these terms can be sent through the <a href="/contact.html">contact page</a>.</p>
    </div>
  </section>
"""

write("terms.html", page(
    "Terms & Conditions \u2014 CutLine",
    "Terms and conditions for using the CutLine AI background remover, including acceptable use and advertising disclosures.",
    "/terms.html", TERMS_BODY, active=None,
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Terms & Conditions", "/terms.html")]),
))

print("privacy + terms written")

# ===========================================================================
# DISCLAIMER
# ===========================================================================
DISCLAIMER_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Disclaimer", None)])}
      <span class="eyebrow">Legal</span>
      <h1>Disclaimer</h1>
      <p class="legal-updated">Last updated: July 28, 2026</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container prose">
      <p>The information and tools on CutLine are provided in good faith, but the following disclaimers apply to your use of the site and service.</p>

      <h2>No professional advice</h2>
      <p>Articles on our <a href="/blog.html">blog</a> about photo editing, image optimization, and related topics are provided for general informational purposes only. They are not professional design, legal, or technical consulting advice, and shouldn't be treated as a substitute for judgment specific to your project.</p>

      <h2>AI accuracy</h2>
      <p>Background removal is performed by an automated AI model. Results depend heavily on the input photo &mdash; lighting, contrast, hair and fur detail, and busy backgrounds can all affect edge quality. We do not guarantee a particular level of accuracy for any given image, and recommend reviewing the Compare view before relying on a result for commercial use.</p>

      {AD_INCONTENT}

      <h2>External links</h2>
      <p>Our site may link to third-party websites or resources, including advertising served by ad networks. We are not responsible for the content, accuracy, or practices of external sites, and including a link does not imply endorsement.</p>

      <h2>Affiliate &amp; advertising disclosure</h2>
      <p>CutLine is free to use. If the site displays advertising (for example, through Google AdSense) or participates in affiliate programs in the future, we will disclose that here and in the relevant page. Ads are clearly separated from editorial content and marked as advertisements.</p>

      <h2>Limitation</h2>
      <p>To the fullest extent permitted by law, CutLine disclaims liability for any loss or damage arising from reliance on information or tools provided on this site. See our <a href="/terms.html">Terms &amp; Conditions</a> for the full limitation of liability.</p>

      <h2>Questions</h2>
      <p>Reach out through the <a href="/contact.html">contact page</a> with any questions about this disclaimer.</p>
    </div>
  </section>
"""

write("disclaimer.html", page(
    "Disclaimer \u2014 CutLine",
    "Disclaimer covering AI accuracy, blog content, external links, and advertising on CutLine.",
    "/disclaimer.html", DISCLAIMER_BODY, active=None,
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Disclaimer", "/disclaimer.html")]),
))

# ===========================================================================
# COOKIE POLICY
# ===========================================================================
COOKIE_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Cookie Policy", None)])}
      <span class="eyebrow">Legal</span>
      <h1>Cookie policy</h1>
      <p class="legal-updated">Last updated: July 28, 2026</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container prose">
      <p>This policy explains what cookies and similar local storage CutLine uses, and the choices you have.</p>

      <h2>What we use instead of "cookies" for the core app</h2>
      <p>The background removal tool itself doesn't need cookies to function &mdash; it uses your browser's localStorage to remember your theme preference, your consent choice, and small thumbnails of recent results. These stay on your device.</p>

      <h2>Cookie categories</h2>
      <table style="width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.9rem;">
        <thead>
          <tr style="text-align:left;border-bottom:1px solid var(--surface-border);">
            <th style="padding:.6em .4em;">Category</th>
            <th style="padding:.6em .4em;">Purpose</th>
            <th style="padding:.6em .4em;">Requires consent?</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--surface-border);">
            <td style="padding:.6em .4em;">Strictly necessary</td>
            <td style="padding:.6em .4em;">Theme preference, cookie consent state, core site function.</td>
            <td style="padding:.6em .4em;">No</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface-border);">
            <td style="padding:.6em .4em;">Analytics</td>
            <td style="padding:.6em .4em;">Aggregate usage measurement (e.g. Google Analytics 4, Microsoft Clarity) &mdash; not yet active by default.</td>
            <td style="padding:.6em .4em;">Yes</td>
          </tr>
          <tr>
            <td style="padding:.6em .4em;">Advertising</td>
            <td style="padding:.6em .4em;">Ad delivery and measurement (e.g. Google AdSense), once enabled.</td>
            <td style="padding:.6em .4em;">Yes</td>
          </tr>
        </tbody>
      </table>

      {AD_INCONTENT}

      <h2>Your choice</h2>
      <p>On your first visit, a banner lets you accept all cookies or reject non-essential ones. Analytics and advertising scripts only load after you accept &mdash; nothing beyond strictly necessary storage runs before that choice is made.</p>
      <p>To change your mind later, clear this site's data in your browser settings; the consent banner will appear again on your next visit.</p>

      <h2>Third-party cookies</h2>
      <p>If analytics or advertising is enabled, the relevant provider (Google, Microsoft, etc.) may set its own cookies as described in their respective privacy policies. We don't control those cookies directly.</p>

      <h2>More information</h2>
      <p>See our <a href="/privacy.html">Privacy Policy</a> for how any collected data is used, or the <a href="/contact.html">contact page</a> for questions.</p>
    </div>
  </section>
"""

write("cookie-policy.html", page(
    "Cookie Policy \u2014 CutLine",
    "Details on the cookies and local storage CutLine uses, including analytics and advertising categories and how to manage consent.",
    "/cookie-policy.html", COOKIE_BODY, active=None,
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Cookie Policy", "/cookie-policy.html")]),
))

# ===========================================================================
# FAQ
# ===========================================================================
FAQS = [
    ("Is CutLine really free to use?", "Yes. Every editing feature &mdash; background removal, background replacement, crop/rotate/flip, and all export formats &mdash; is free, with no account and no watermark."),
    ("Do my photos get uploaded to a server?", "No. The AI model runs locally in your browser using WebAssembly. Your image is decoded, processed, and composited entirely on your device."),
    ("What image formats are supported?", "You can upload PNG, JPG/JPEG, or WebP files up to 30MB each. You can export as transparent PNG, flattened JPG, or optimized WebP."),
    ("Why does the cutout have rough edges around hair or fur?", "Fine detail like flyaway hair is the hardest case for any segmentation model. Turn on edge smoothing and increase the feather slider, or try a photo with more contrast between the subject and background for a cleaner result."),
    ("Can I process multiple photos at once?", "Yes. Drop in several images and use \"Process all in batch\" to run them through the AI one after another; each result stays in the batch strip so you can jump between them."),
    ("Does CutLine work on mobile?", "Yes. The interface is responsive and touch-friendly, including pinch-free zoom controls and a draggable compare slider."),
    ("What happens to my \"recent history\"?", "Small, low-resolution thumbnails of your last few results are stored in your browser's local storage so you can glance back at them. They're never sent anywhere and are specific to the browser and device you used."),
    ("Will there be ads on this site?", "We reserve clearly labeled ad spaces (for example, via Google AdSense) to help keep the tool free. Ads, where present, are separated from the editing tool and editorial content, and never appear inside the image workspace itself."),
    ("Do you use cookies?", "Only strictly necessary local storage by default (theme, consent choice). Analytics and advertising cookies are optional and only activate if you accept them in the cookie banner &mdash; see our Cookie Policy for details."),
    ("Can I use CutLine for commercial product photos?", "Yes, plenty of people use it exactly for that. Just review the Compare view before publishing, since AI cutouts can occasionally need a manual touch-up on tricky edges."),
]

def faq_item(q, a):
    return f"""<details class="faq-item">
  <summary>{q}</summary>
  <div class="faq-answer">{a}</div>
</details>"""

FAQ_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("FAQ", None)])}
      <span class="eyebrow">Frequently asked questions</span>
      <h1>Answers to the questions we hear most.</h1>
      <p class="lead">Can't find what you're looking for? <a href="/contact.html">Get in touch</a>.</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="content-layout">
        <div class="faq-list">
          {chr(10).join(faq_item(q, a) for q, a in FAQS)}
        </div>
        <aside class="sidebar">
          <div class="sidebar-card">
            <h4>Still stuck?</h4>
            <ul>
              <li><a href="/about.html">How CutLine works</a></li>
              <li><a href="/privacy.html">Privacy policy</a></li>
              <li><a href="/contact.html">Contact support</a></li>
            </ul>
          </div>
          {AD_SIDEBAR}
        </aside>
      </div>
      <div class="container" style="padding:0;">{AD_INCONTENT}</div>
    </div>
  </section>
"""

FAQ_JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q.replace("&mdash;", "\u2014"),
         "acceptedAnswer": {"@type": "Answer", "text": a.replace("&mdash;", "\u2014")}}
        for q, a in FAQS
    ]
}, indent=2)

write("faq.html", page(
    "FAQ \u2014 CutLine Background Remover",
    "Frequently asked questions about CutLine's on-device AI background remover: formats, privacy, batch processing, cookies, and more.",
    "/faq.html", FAQ_BODY, active="faq",
    extra_jsonld=f'<script type="application/ld+json">\n{FAQ_JSONLD}\n</script>\n' + breadcrumb_jsonld([("Home", "/"), ("FAQ", "/faq.html")]),
))

print("disclaimer + cookie-policy + faq written")

# ===========================================================================
# BLOG
# ===========================================================================
POSTS = [
    {
        "slug": "ai-image-editing-explained",
        "tag": "AI Image Editing",
        "title": "AI Image Editing, Explained: What's Actually Happening Under the Hood",
        "description": "A plain-language look at how AI-powered image editing tools like background removers actually work, and why more of them now run in your browser.",
        "date": "2026-07-10",
        "read": "6 min read",
        "excerpt": "How segmentation models see a photo the way we do \u2014 and why so much of that work now happens on your own device instead of a server.",
        "body": """
<p>"AI image editing" has become a catch-all phrase for anything from one-click background removal to full scene generation. Underneath the marketing, though, most of the tools people use daily &mdash; including background removers &mdash; rely on one specific technique: <strong>semantic segmentation</strong>.</p>

<h2>Segmentation: teaching a model to see edges</h2>
<p>A segmentation model doesn't "understand" a photo the way a person does. Instead, it's trained on huge sets of images where every pixel has already been labeled &mdash; subject or background, person or product, foreground or sky. Over millions of examples, the model learns statistical patterns: edges where contrast changes sharply, textures typical of hair or fabric, shapes typical of a face or a bottle.</p>
<p>When you feed it a new photo, it doesn't look anything up online. It runs your pixels through the same layers of learned patterns and produces a probability map: for every pixel, how likely is it to belong to the subject? That map becomes the mask used to cut the subject away from its background.</p>

<h2>Why running it in your browser is a bigger deal than it sounds</h2>
<p>For years, this kind of model needed a beefy server with a GPU, which meant your photo had to be uploaded somewhere before anything could happen to it. Two things changed that: models got smaller and more efficient, and browsers got WebAssembly (WASM) &mdash; a way to run near-native-speed code directly on your device, no plugin required.</p>
<p>Put those together and you get tools that download a compact model once, then do every future cutout locally. No round trip to a server, no image leaving your machine, and no waiting behind other people's requests in a queue.</p>

<h2>Where it still struggles</h2>
<p>Segmentation is pattern matching, not true understanding, so it still trips up on the same kinds of images every model does: fine, wispy hair against a busy background; glass and other transparent objects; subjects that share a color with what's behind them. Increasing edge feathering or trying a shot with better subject-background contrast usually helps more than any single settings tweak.</p>

<h2>What this means for you</h2>
<p>If you're choosing a background-removal tool, "AI-powered" isn't the differentiator anymore &mdash; almost everything is, at this point. What actually matters is where the processing happens (your device or someone's server), how much control you get over the edges afterward, and whether the export options match what you'll actually use the image for.</p>
"""
    },
    {
        "slug": "background-removal-guide-for-online-sellers",
        "tag": "Background Removal",
        "title": "The Complete Guide to Background Removal for Online Sellers",
        "description": "A practical walkthrough for turning ordinary product photos into clean, marketplace-ready images using AI background removal.",
        "date": "2026-07-14",
        "read": "7 min read",
        "excerpt": "Consistent, background-free product photos build trust faster than almost any other visual change you can make to a listing.",
        "body": """
<p>Marketplace shoppers scroll fast, and inconsistent product photography is one of the quickest ways to look unprofessional next to competitors who've already cleaned theirs up. The good news: getting there no longer requires a photo studio or a subscription to expensive desktop software.</p>

<h2>Start with a photo the model can actually work with</h2>
<p>Background removal quality depends more on the original photo than most sellers expect. A few habits make a bigger difference than any editing setting:</p>
<ul>
  <li>Shoot against a background that contrasts with your product's color and material.</li>
  <li>Use even, diffuse lighting &mdash; harsh shadows get mistaken for part of the subject.</li>
  <li>Keep the product in focus and reasonably large in the frame; tiny, blurry subjects are harder to segment cleanly.</li>
</ul>

<h2>Choosing what goes behind the product</h2>
<p>Once the background is gone, you have three realistic options for a marketplace listing: pure white (the safest default for most platforms' requirements), a soft gradient or brand color (good for hero images on your own site), or a lifestyle scene (best reserved for secondary images, not the primary thumbnail, since it can distract from the product itself).</p>

<h2>Batch consistency matters more than any single photo</h2>
<p>If you're photographing a whole catalog, process it in one batch rather than one photo at a time across different sessions. Lighting, framing, and background choice drift slightly every time you start fresh, and shoppers notice inconsistency across a storefront even if they can't say exactly why.</p>

<h2>Export format checklist</h2>
<p>Most marketplaces want a flattened image (JPG) with a plain background rather than transparency, since not every platform renders transparent PNGs consistently in search results. Keep the transparent PNG as your master file, then export a flattened JPG version for the listing itself &mdash; that way you can always swap the background later without redoing the cutout.</p>

<h2>A quick pre-publish check</h2>
<p>Before uploading, zoom into the edges around any fine detail &mdash; straps, fabric texture, thin hardware. These are exactly the spots an AI cutout can leave a faint halo or slightly soft edge. A comparison slider between the original and the cutout makes this a five-second check instead of a guessing game.</p>
"""
    },
    {
        "slug": "photo-editing-tips-that-actually-matter",
        "tag": "Photo Editing Tips",
        "title": "Photo Editing Tips That Actually Matter (and a Few That Don't)",
        "description": "A grounded look at which photo editing habits genuinely improve results, versus which ones are more folklore than fact.",
        "date": "2026-07-18",
        "read": "5 min read",
        "excerpt": "Not every editing habit pulls its weight. Here's what's worth your time and what you can safely skip.",
        "body": """
<p>Photo editing advice tends to pile up over time until it's hard to tell which habits actually improve your results and which ones are just repeated because everyone else repeats them. A few, tested against real editing sessions, hold up consistently.</p>

<h2>Worth doing: fix exposure before anything else</h2>
<p>Color correction, cropping, and background work all get harder on a poorly exposed photo. If the subject is under- or overexposed, fix that first &mdash; every downstream edit, including AI background removal, performs better on an image with clear tonal separation between subject and background.</p>

<h2>Worth doing: crop with intention, not just to "fill the frame"</h2>
<p>A crop should serve a purpose: removing a distraction, tightening the composition, or matching a required aspect ratio for a platform. Cropping purely to zoom in on a subject often removes context a viewer needs, especially for product or portrait photography.</p>

<h2>Worth doing: keep a non-destructive original</h2>
<p>Always keep your unedited source file. Once you flatten a background, apply a heavy crop, or export a compressed JPG, you can't recover the original detail. Treat every edit as a new export from the original, not an edit of your last edit.</p>

<h2>Skip it: over-sharpening</h2>
<p>Sharpening is one of the most overused tools in casual photo editing. Past a certain point it doesn't add detail &mdash; it adds visible haloing around edges, which is especially noticeable around a subject that's just been cut from its background. A light touch, or none at all, usually looks more natural than people expect.</p>

<h2>Skip it: stacking multiple filters "just in case"</h2>
<p>Layering several presets or filters on top of each other tends to muddy color and contrast rather than improve it. Pick one clear direction for an edit &mdash; correct exposure, adjust white balance, then stop &mdash; instead of running an image through everything available.</p>

<h2>The habit that ties it together</h2>
<p>Whatever else you do, compare before and after at 100% zoom before calling an edit finished. Edits that look fine at thumbnail size frequently reveal rough edges, banding, or artifacts once you actually look closely &mdash; the same way an AI-cut background can look perfect until you zoom in on a strand of hair.</p>
"""
    },
    {
        "slug": "image-optimization-for-faster-websites",
        "tag": "Image Optimization",
        "title": "Image Optimization for Faster Websites (Without Losing Quality)",
        "description": "How format choice, compression, and dimensions affect page speed \u2014 and how to optimize images without visibly hurting quality.",
        "date": "2026-07-21",
        "read": "6 min read",
        "excerpt": "Most page-weight problems trace back to a handful of oversized images. Here's how to fix that without a visible quality hit.",
        "body": """
<p>Images are usually the single largest contributor to page weight, and page weight is one of the more direct levers you have over Core Web Vitals metrics like Largest Contentful Paint. The good news is that most of the gains come from a small number of decisions, not constant fiddling.</p>

<h2>Pick the right format for the job</h2>
<p>JPG remains a solid default for photos with lots of color variation and no transparency. PNG is the right call specifically when you need transparency &mdash; like a cutout product shot &mdash; but it's a poor choice for full photographic backgrounds since file sizes balloon quickly. WebP splits the difference well: it supports transparency like PNG but compresses closer to JPG sizes, which is why it's become the practical default for the web.</p>

<h2>Serve images at the size they're actually displayed</h2>
<p>A 4000px-wide photo displayed in a 600px-wide card is wasted bandwidth, full stop. Resize images to the largest size they'll realistically be shown at (accounting for high-density displays, roughly 1.5&ndash;2x the display size) rather than shipping the original camera resolution to every visitor.</p>

<h2>Compression is a dial, not a switch</h2>
<p>"Compressed" isn't binary. JPG and WebP quality settings typically run from 0&ndash;100, and the useful range for most photography sits between 70&ndash;85 &mdash; high enough that compression artifacts aren't visible at normal viewing distance, low enough that file size drops substantially compared to a 100%-quality export. Push much lower and you'll start seeing blocky artifacts, especially around sharp edges like a cutout subject against a solid background.</p>

<h2>Don't forget the basics that aren't about the image itself</h2>
<ul>
  <li>Use <code>loading="lazy"</code> for images below the fold so the browser doesn't fetch them before they're needed.</li>
  <li>Set explicit width and height (or aspect-ratio) attributes so the browser can reserve layout space and avoid content jumping around as images load.</li>
  <li>Serve images from a CDN or with proper cache headers so repeat visitors aren't re-downloading the same files.</li>
</ul>

<h2>A simple workflow</h2>
<p>Cut the background if you need to, resize to the actual display dimensions, export as WebP at roughly 80% quality, and confirm the result still looks correct at 100% zoom. That single pass handles the overwhelming majority of image-related page speed issues without a visible drop in quality.</p>
"""
    },
    {
        "slug": "transparent-png-guide",
        "tag": "Transparent PNGs",
        "title": "Transparent PNGs: When to Use Them and When Not To",
        "description": "A practical breakdown of how transparent PNG files work, when they're the right export choice, and when another format serves you better.",
        "date": "2026-07-25",
        "read": "5 min read",
        "excerpt": "Transparency is a feature with real tradeoffs, not a default you should reach for out of habit.",
        "body": """
<p>A transparent PNG is exactly what it sounds like: a PNG file where an alpha channel marks certain pixels as partially or fully see-through, so whatever sits behind the image shows through instead of a solid background color. It's the standard output of most background-removal tools, but it isn't automatically the right file for every situation.</p>

<h2>How the transparency actually works</h2>
<p>Alongside red, green, and blue values, a PNG with transparency stores a fourth channel &mdash; alpha &mdash; per pixel, usually on a scale of 0 (fully transparent) to 255 (fully opaque). Soft, feathered edges around a cutout subject use intermediate alpha values so the transition to whatever's behind it looks natural instead of jagged.</p>

<h2>Good use cases</h2>
<ul>
  <li><strong>Logos and icons</strong> that need to sit on top of different colored backgrounds without a visible box around them.</li>
  <li><strong>Product cutouts</strong> destined for a design tool, presentation, or a page where you'll control the background yourself.</li>
  <li><strong>Layered composites</strong> &mdash; anywhere you're combining the subject with a different background later.</li>
</ul>

<h2>When it's the wrong choice</h2>
<p>Transparent PNGs are typically larger than an equivalent flattened JPG, since compression works less efficiently on complex alpha data. They're also not universally supported: some platforms flatten transparency to a default color (often white or black) rather than honoring it, which can produce an unexpected outline around your subject. If you're uploading directly to a marketplace or social platform, check whether it actually preserves transparency before relying on it &mdash; flattening onto a plain background yourself first is safer.</p>

<h2>Transparent PNG vs. WebP with alpha</h2>
<p>WebP also supports an alpha channel and generally compresses smaller than PNG at equivalent quality, which makes it a good alternative for web use once you've confirmed your target platform and browsers support it. For maximum compatibility &mdash; print workflows, older software, or platforms with unclear WebP support &mdash; PNG remains the safer default.</p>

<h2>A simple rule of thumb</h2>
<p>Keep a transparent PNG as your master, editable file whenever you've cut out a subject. Export a flattened JPG or WebP for anywhere the background will be fixed and final, like a marketplace listing or a social post. That way you never have to redo a cutout just because you decided you wanted a different background later.</p>
"""
    },
]

def post_card(p):
    return f"""<a class="blog-card" href="/blog-{p['slug']}.html">
  <div class="thumb"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3 6 6 1-4.5 4.4 1 6.1L12 16l-5.5 3.5 1-6.1L3 8l6-1z"/></svg></div>
  <div class="body">
    <span class="tag">{p['tag']}</span>
    <h3>{p['title']}</h3>
    <p>{p['excerpt']}</p>
    <span class="meta">{p['date']} &middot; {p['read']}</span>
  </div>
</a>"""

BLOG_INDEX_BODY = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Blog", None)])}
      <span class="eyebrow">The CutLine blog</span>
      <h1>Notes on AI image editing, background removal, and getting images web-ready.</h1>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="content-layout">
        <div>
          <div class="blog-grid">
            {chr(10).join(post_card(p) for p in POSTS)}
          </div>
          {AD_INCONTENT}
        </div>
        <aside class="sidebar">
          <div class="sidebar-card">
            <h4>Topics</h4>
            <ul>
              <li><a href="/blog.html">AI image editing</a></li>
              <li><a href="/blog.html">Background removal</a></li>
              <li><a href="/blog.html">Photo editing tips</a></li>
              <li><a href="/blog.html">Image optimization</a></li>
              <li><a href="/blog.html">Transparent PNGs</a></li>
            </ul>
          </div>
          {AD_SIDEBAR}
        </aside>
      </div>
    </div>
  </section>
"""

write("blog.html", page(
    "Blog \u2014 CutLine",
    "Guides and tips on AI image editing, background removal, photo editing, image optimization, and transparent PNGs.",
    "/blog.html", BLOG_INDEX_BODY, active="blog",
    extra_jsonld=breadcrumb_jsonld([("Home", "/"), ("Blog", "/blog.html")]),
))

# Individual blog post pages
for i, p in enumerate(POSTS):
    others = [o for o in POSTS if o["slug"] != p["slug"]][:3]
    related = "".join(f'<li><a href="/blog-{o["slug"]}.html">{o["title"]}</a></li>' for o in others)
    body = f"""
  <section class="page-hero">
    <div class="container">
      {breadcrumb([("Home", "/"), ("Blog", "/blog.html"), (p['title'], None)])}
      <span class="eyebrow">{p['tag']}</span>
      <h1>{p['title']}</h1>
      <div class="post-meta">
        <span>{p['date']}</span><span>{p['read']}</span><span>By the CutLine team</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="content-layout">
        <article class="prose post-body">
          {p['body']}
          {AD_INCONTENT}
          <div class="post-tags">
            <a href="/blog.html">{p['tag']}</a>
            <a href="/blog.html">CutLine Blog</a>
          </div>
        </article>
        <aside class="sidebar">
          <div class="sidebar-card">
            <h4>More from the blog</h4>
            <ul>{related}</ul>
          </div>
          {AD_SIDEBAR}
        </aside>
      </div>
    </div>
  </section>
"""
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": p["description"],
        "datePublished": p["date"],
        "dateModified": p["date"],
        "author": {"@type": "Organization", "name": "CutLine"},
        "publisher": {"@type": "Organization", "name": "CutLine", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icons/favicon.svg"}},
        "mainEntityOfPage": f"{SITE}/blog-{p['slug']}.html",
        "image": f"{SITE}/assets/images/og-cover.jpg",
    }, indent=2)
    extra_ld = f'<script type="application/ld+json">\n{jsonld}\n</script>\n' + breadcrumb_jsonld([("Home", "/"), ("Blog", "/blog.html"), (p["title"], f"/blog-{p['slug']}.html")])
    write(f"blog-{p['slug']}.html", page(
        f"{p['title']} \u2014 CutLine Blog",
        p["description"], f"/blog-{p['slug']}.html", body, active="blog",
        extra_jsonld=extra_ld,
    ))

print("blog index + posts written")

# ===========================================================================
# 404
# ===========================================================================
NOTFOUND_BODY = """
  <section class="error-page">
    <div class="container">
      <div class="error-code">404</div>
      <h1>This page took its own background off.</h1>
      <p>The page you're looking for doesn't exist, or may have moved. Let's get you back on track.</p>
      <div class="error-actions">
        <a href="/" class="btn">Go to homepage</a>
        <a href="/blog.html" class="btn btn-secondary">Visit the blog</a>
        <a href="/contact.html" class="btn btn-secondary">Contact us</a>
      </div>
    </div>
  </section>
"""

write("404.html", page(
    "Page Not Found \u2014 CutLine",
    "The page you're looking for doesn't exist or may have moved.",
    "/404.html", NOTFOUND_BODY, active=None,
))

print("404 written")
print("\\nAll pages generated.")





