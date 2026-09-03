/**
 * main.js — application entry point. Wires together the upload dropzone,
 * batch queue, AI background removal, editing tools, background
 * compositing, and download actions.
 */
import {
  showToast,
  formatBytes,
  loadImage,
  canvasToBlob,
  downloadBlob,
  uid,
} from "./utils.js";
import { preloadEngine, removeBackground } from "./processor.js";
import { compositeBackground, loadCustomBackground, GRADIENT_PRESETS } from "./background.js";
import { createViewport, applyOrientation, applyCrop, createCompareSlider } from "./editor.js";
import { addHistoryEntry, getHistory } from "./history.js";

const ACCEPTED_TYPES = ["image/png", "image/jpeg", "image/webp"];
const MAX_FILE_MB = 30;
const SWATCH_COLORS = ["#ffffff", "#101116", "#5b5fef", "#34d399", "#f5a623", "#ef5b6f", "#e7e7e4", "#7477f5"];

/** @type {Array<object>} */
let queue = [];
let activeId = null;
let currentView = "transparent";

const el = (id) => document.getElementById(id);

const dropzone = el("dropzone");
const fileInput = el("fileInput");
const editor = el("editor");
const stageWrap = el("stageWrap");
const mainCanvas = el("mainCanvas");
const sideBeforeCanvas = el("sideBeforeCanvas");
const sideAfterCanvas = el("sideAfterCanvas");
const compareBeforeCanvas = el("compareBeforeCanvas");
const compareAfterCanvas = el("compareAfterCanvas");
const compareBeforeLayer = el("compareBeforeLayer");
const compareHandle = el("compareHandle");
const stageSkeleton = el("stageSkeleton");
const progressOverlay = el("progressOverlay");
const progressFill = el("progressFill");
const progressLabel = el("progressLabel");
const batchStrip = el("batchStrip");
const historyStrip = el("historyStrip");

// Fetch the engine while the browser is idle so a click can start processing immediately.
const scheduleIdle = window.requestIdleCallback || ((callback) => setTimeout(callback, 800));
scheduleIdle(() => preloadEngine(), { timeout: 2000 });

/* -------------------------------------------------------------------------
 * Queue item factory
 * ---------------------------------------------------------------------- */
function createItem(file) {
  return {
    id: uid(),
    file,
    name: file.name,
    format: file.type.split("/")[1]?.toUpperCase() || "?",
    size: file.size,
    originalImage: null, // HTMLImageElement
    baseCanvas: null, // after orientation/crop, pre-AI
    resultImage: null, // HTMLImageElement of the AI cutout (transparent PNG)
    status: "idle", // idle | processing | done | error
    transform: { rotate: 0, flipH: false, flipV: false },
    crop: null, // {x,y,w,h} normalized, or null
    bg: { type: "transparent", color: "#ffffff", gradient: GRADIENT_PRESETS[0], image: null, imageEl: null },
    feather: 1,
    smoothEdges: true,
    history: [],
    historyIndex: -1,
  };
}

function activeItem() {
  return queue.find((q) => q.id === activeId) || null;
}

function pushHistory(item) {
  const snapshot = JSON.stringify({ transform: item.transform, crop: item.crop, bg: { ...item.bg, imageEl: undefined }, feather: item.feather });
  item.history = item.history.slice(0, item.historyIndex + 1);
  item.history.push(snapshot);
  item.historyIndex = item.history.length - 1;
  updateUndoRedoState(item);
}

function updateUndoRedoState(item) {
  el("undoBtn").disabled = !item || item.historyIndex <= 0;
  el("redoBtn").disabled = !item || item.historyIndex >= item.history.length - 1;
}

/* -------------------------------------------------------------------------
 * File intake
 * ---------------------------------------------------------------------- */
function validateFile(file) {
  if (!ACCEPTED_TYPES.includes(file.type)) {
    showToast(`"${file.name}" isn't a supported format. Use PNG, JPG, or WebP.`, "error");
    return false;
  }
  if (file.size > MAX_FILE_MB * 1024 * 1024) {
    showToast(`"${file.name}" is over ${MAX_FILE_MB}MB. Try a smaller file.`, "error");
    return false;
  }
  return true;
}

async function addFiles(fileList) {
  const files = Array.from(fileList).filter(validateFile);
  if (files.length === 0) return;

  for (const file of files) {
    const item = createItem(file);
    queue.push(item);
    try {
      const url = URL.createObjectURL(file);
      item.originalImage = await loadImage(url);
      rebuildBaseCanvas(item);
      pushHistory(item);
    } catch {
      item.status = "error";
      showToast(`Couldn't read "${file.name}".`, "error");
    }
  }

  const wasEmpty = !activeId;
  if (wasEmpty) activeId = queue[0].id;
  editor.classList.add("is-active");
  dropzone.style.display = "none";
  renderBatchStrip();
  await renderActive();
  showToast(files.length > 1 ? `${files.length} images added to the batch.` : `"${files[0].name}" added.`, "success", 2600);

  // Show the "Remove background" call-to-action rather than processing
  // automatically, so it's clear a click is what starts the AI.
  updateIdleCta();
}

function rebuildBaseCanvas(item) {
  let canvas = applyOrientation(item.originalImage, item.transform);
  if (item.crop) canvas = applyCrop(canvas, item.crop);
  item.baseCanvas = canvas;
}

/* -------------------------------------------------------------------------
 * Rendering
 * ---------------------------------------------------------------------- */
function sizeCanvas(canvas, w, h) {
  canvas.width = w;
  canvas.height = h;
}

function updateIdleCta() {
  const item = activeItem();
  const overlay = el("idleCtaOverlay");
  if (!overlay) return;
  const show = Boolean(item) && (item.status === "idle" || item.status === "error");
  overlay.classList.toggle("active", show);
}

async function renderActive() {
  const item = activeItem();
  if (!item) return;

  // Info panel
  el("infoWidth").textContent = item.baseCanvas ? `${item.baseCanvas.width}px` : "—";
  el("infoHeight").textContent = item.baseCanvas ? `${item.baseCanvas.height}px` : "—";
  el("infoSize").textContent = formatBytes(item.size);
  el("infoFormat").textContent = item.format;

  updateUndoRedoState(item);
  syncBackgroundPanelUI(item);
  updateIdleCta();

  const w = item.baseCanvas.width;
  const h = item.baseCanvas.height;
  [mainCanvas, sideBeforeCanvas, sideAfterCanvas, compareBeforeCanvas, compareAfterCanvas].forEach((c) => sizeCanvas(c, w, h));

  // "before" layers always show the base photo
  sideBeforeCanvas.getContext("2d").drawImage(item.baseCanvas, 0, 0);
  compareBeforeCanvas.getContext("2d").drawImage(item.baseCanvas, 0, 0);

  if (item.status !== "done" || !item.resultImage) {
    // Nothing to composite yet — show the plain photo on the main canvas.
    const ctx = mainCanvas.getContext("2d");
    ctx.clearRect(0, 0, w, h);
    ctx.drawImage(item.baseCanvas, 0, 0);
    sideAfterCanvas.getContext("2d").clearRect(0, 0, w, h);
    compareAfterCanvas.getContext("2d").clearRect(0, 0, w, h);
    return;
  }

  const bgConfig = resolveBgConfig(item);
  await compositeBackground(mainCanvas, item.resultImage, bgConfig, {
    feather: item.feather,
    originalImage: item.baseCanvas,
    blurAmount: item.blurAmount || 14,
  });
  await compositeBackground(sideAfterCanvas, item.resultImage, bgConfig, {
    feather: item.feather,
    originalImage: item.baseCanvas,
    blurAmount: item.blurAmount || 14,
  });
  await compositeBackground(compareAfterCanvas, item.resultImage, bgConfig, {
    feather: item.feather,
    originalImage: item.baseCanvas,
    blurAmount: item.blurAmount || 14,
  });
}

function resolveBgConfig(item) {
  const { bg } = item;
  if (bg.type === "gradient") return { type: "gradient", stops: bg.gradient.stops };
  if (bg.type === "image") return { type: "image", image: bg.imageEl };
  return bg;
}

function renderBatchStrip() {
  batchStrip.innerHTML = "";
  queue.forEach((item) => {
    const thumb = document.createElement("div");
    thumb.className = "batch-thumb" + (item.id === activeId ? " active" : "");
    thumb.setAttribute("role", "button");
    thumb.setAttribute("tabindex", "0");
    thumb.setAttribute("aria-label", `Select ${item.name}`);
    const img = document.createElement("img");
    img.src = item.originalImage ? item.originalImage.src : "";
    img.alt = "";
    const status = document.createElement("span");
    status.className = "status" + (item.status === "done" ? " done" : "");
    const remove = document.createElement("button");
    remove.className = "remove";
    remove.type = "button";
    remove.setAttribute("aria-label", `Remove ${item.name}`);
    remove.textContent = "×";
    remove.addEventListener("click", (e) => {
      e.stopPropagation();
      queue = queue.filter((q) => q.id !== item.id);
      if (activeId === item.id) activeId = queue[0]?.id || null;
      renderBatchStrip();
      if (activeId) renderActive();
      else resetToEmptyState();
    });
    thumb.append(img, status, remove);
    const select = () => {
      activeId = item.id;
      renderBatchStrip();
      renderActive();
    };
    thumb.addEventListener("click", select);
    thumb.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(); }
    });
    batchStrip.appendChild(thumb);
  });
}

function resetToEmptyState() {
  editor.classList.remove("is-active");
  dropzone.style.display = "";
  fileInput.value = "";
}

/* -------------------------------------------------------------------------
 * AI processing
 * ---------------------------------------------------------------------- */
async function processItem(item) {
  item.status = "processing";
  renderBatchStrip();
  updateIdleCta();
  stageSkeleton.classList.add("active");
  progressOverlay.classList.add("active");
  progressFill.style.width = "0%";
  progressLabel.textContent = "Loading AI engine…";

  try {
    const blob = await canvasToBlob(item.baseCanvas, "image/png");
    const resultBlob = await removeBackground(blob, ({ key, current, total }) => {
      const pct = total ? Math.round((current / total) * 100) : 0;
      progressFill.style.width = `${pct}%`;
      progressLabel.textContent = key ? `${key} — ${pct}%` : `Processing — ${pct}%`;
    });
    const url = URL.createObjectURL(resultBlob);
    item.resultImage = await loadImage(url);
    item.status = "done";
    addHistoryEntry({ name: item.name, resultCanvas: await compositedThumbCanvas(item) });
    renderHistoryStrip();
    showToast(`Background removed from "${item.name}".`, "success");
  } catch (err) {
    item.status = "error";
    showToast(err.message || "Background removal failed. Please try again.", "error");
  } finally {
    stageSkeleton.classList.remove("active");
    progressOverlay.classList.remove("active");
    renderBatchStrip();
    if (item.id === activeId) renderActive();
  }
}

async function compositedThumbCanvas(item) {
  const c = document.createElement("canvas");
  c.width = item.baseCanvas.width;
  c.height = item.baseCanvas.height;
  await compositeBackground(c, item.resultImage, resolveBgConfig(item), { feather: item.feather, originalImage: item.baseCanvas });
  return c;
}

function renderHistoryStrip() {
  const items = getHistory();
  historyStrip.innerHTML = "";
  if (items.length === 0) {
    historyStrip.innerHTML = '<p style="font-size:.82rem;color:var(--text-3);">Nothing processed yet this session.</p>';
    return;
  }
  items.forEach((h) => {
    const thumb = document.createElement("div");
    thumb.className = "batch-thumb";
    thumb.title = `${h.name} — ${new Date(h.date).toLocaleString()}`;
    const img = document.createElement("img");
    img.src = h.thumbnail;
    img.alt = `${h.name} thumbnail`;
    thumb.appendChild(img);
    historyStrip.appendChild(thumb);
  });
}

/* -------------------------------------------------------------------------
 * View tabs (transparent / compare / side-by-side)
 * ---------------------------------------------------------------------- */
function setView(view) {
  currentView = view;
  el("transparentView").style.display = view === "transparent" ? "grid" : "none";
  el("sideView").style.display = view === "side" ? "grid" : "none";
  el("compareView").classList.toggle("active", view === "compare");
  document.querySelectorAll(".view-tabs button").forEach((btn) => {
    const on = btn.dataset.view === view;
    btn.classList.toggle("active", on);
    btn.setAttribute("aria-selected", String(on));
  });
}

document.querySelectorAll(".view-tabs button").forEach((btn) => {
  btn.addEventListener("click", () => setView(btn.dataset.view));
});

/* -------------------------------------------------------------------------
 * Upload wiring
 * ---------------------------------------------------------------------- */
["dragenter", "dragover"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-over");
  })
);
["dragleave", "drop"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-over");
  })
);
dropzone.addEventListener("drop", (e) => {
  if (e.dataTransfer?.files?.length) addFiles(e.dataTransfer.files);
});
dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileInput.click(); }
});
fileInput.addEventListener("change", () => {
  if (fileInput.files.length) addFiles(fileInput.files);
});

/* -------------------------------------------------------------------------
 * Toolbar: zoom / pan / fit
 * ---------------------------------------------------------------------- */
const viewport = createViewport(stageWrap, mainCanvas);
el("zoomInBtn").addEventListener("click", viewport.zoomIn);
el("zoomOutBtn").addEventListener("click", viewport.zoomOut);
el("fitBtn").addEventListener("click", viewport.fit);

/* -------------------------------------------------------------------------
 * Toolbar: rotate / flip / crop / start over / undo-redo
 * ---------------------------------------------------------------------- */
el("rotateBtn").addEventListener("click", () => {
  const item = activeItem();
  if (!item) return;
  item.transform.rotate = (item.transform.rotate + 90) % 360;
  invalidateResult(item);
  rebuildBaseCanvas(item);
  pushHistory(item);
  renderActive();
});
el("flipHBtn").addEventListener("click", () => {
  const item = activeItem();
  if (!item) return;
  item.transform.flipH = !item.transform.flipH;
  invalidateResult(item);
  rebuildBaseCanvas(item);
  pushHistory(item);
  renderActive();
});
el("cropBtn").addEventListener("click", () => {
  const item = activeItem();
  if (!item) return;
  if (item.crop) {
    item.crop = null;
    invalidateResult(item);
    rebuildBaseCanvas(item);
    pushHistory(item);
    renderActive();
    showToast("Crop removed.", "info", 2200);
  } else {
    // Simple centered 80% crop as a quick, accessible default.
    item.crop = { x: 0.1, y: 0.1, w: 0.8, h: 0.8 };
    invalidateResult(item);
    rebuildBaseCanvas(item);
    pushHistory(item);
    renderActive();
    showToast("Cropped to center 80%. Click again to remove.", "info", 3000);
  }
});
el("startOverBtn").addEventListener("click", () => {
  queue = [];
  activeId = null;
  resetToEmptyState();
  renderBatchStrip();
});

function invalidateResult(item) {
  if (item.status === "done") {
    item.status = "idle";
    item.resultImage = null;
    showToast("Edits reset the cutout — click Remove Background again.", "info", 3200);
  }
}

el("undoBtn").addEventListener("click", () => {
  const item = activeItem();
  if (!item || item.historyIndex <= 0) return;
  item.historyIndex -= 1;
  restoreSnapshot(item);
});
el("redoBtn").addEventListener("click", () => {
  const item = activeItem();
  if (!item || item.historyIndex >= item.history.length - 1) return;
  item.historyIndex += 1;
  restoreSnapshot(item);
});
function restoreSnapshot(item) {
  const snap = JSON.parse(item.history[item.historyIndex]);
  item.transform = snap.transform;
  item.crop = snap.crop;
  item.bg = { ...item.bg, ...snap.bg };
  item.feather = snap.feather;
  rebuildBaseCanvas(item);
  updateUndoRedoState(item);
  renderActive();
}

document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !e.shiftKey) {
    e.preventDefault();
    el("undoBtn").click();
  }
  if ((e.ctrlKey || e.metaKey) && (e.key.toLowerCase() === "y" || (e.key.toLowerCase() === "z" && e.shiftKey))) {
    e.preventDefault();
    el("redoBtn").click();
  }
});

/* -------------------------------------------------------------------------
 * Background panel
 * ---------------------------------------------------------------------- */
SWATCH_COLORS.forEach((color) => {
  const btn = document.createElement("button");
  btn.className = "swatch";
  btn.style.background = color;
  btn.type = "button";
  btn.setAttribute("aria-label", `Use ${color} background`);
  btn.addEventListener("click", () => {
    const item = activeItem();
    if (!item) return;
    item.bg.type = "color";
    item.bg.color = color;
    pushHistory(item);
    syncBackgroundPanelUI(item);
    renderActive();
  });
  el("colorSwatches").appendChild(btn);
});
el("customColor").addEventListener("change", (e) => {
  const item = activeItem();
  if (!item) return;
  item.bg.type = "color";
  item.bg.color = e.target.value;
  pushHistory(item);
  syncBackgroundPanelUI(item);
  renderActive();
});

GRADIENT_PRESETS.forEach((preset) => {
  const btn = document.createElement("button");
  btn.className = "gradient-swatch";
  btn.style.background = `linear-gradient(135deg, ${preset.stops[0]}, ${preset.stops[1]})`;
  btn.type = "button";
  btn.setAttribute("aria-label", `Use ${preset.id} gradient background`);
  btn.addEventListener("click", () => {
    const item = activeItem();
    if (!item) return;
    item.bg.type = "gradient";
    item.bg.gradient = preset;
    pushHistory(item);
    syncBackgroundPanelUI(item);
    renderActive();
  });
  el("gradientSwatches").appendChild(btn);
});

document.querySelectorAll(".bg-tabs button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const item = activeItem();
    if (!item) return;
    item.bg.type = btn.dataset.bg;
    pushHistory(item);
    syncBackgroundPanelUI(item);
    renderActive();
  });
});

el("uploadBgBtn").addEventListener("click", () => el("bgImageInput").click());
el("bgImageInput").addEventListener("change", async (e) => {
  const item = activeItem();
  const file = e.target.files[0];
  if (!item || !file) return;
  try {
    item.bg.imageEl = await loadCustomBackground(file);
    item.bg.type = "image";
    pushHistory(item);
    syncBackgroundPanelUI(item);
    renderActive();
    showToast("Custom background applied.", "success", 2400);
  } catch {
    showToast("Couldn't load that background image.", "error");
  }
});

el("blurRange").addEventListener("input", (e) => {
  const item = activeItem();
  if (!item) return;
  item.blurAmount = Number(e.target.value);
  el("blurValue").textContent = e.target.value;
  renderActive();
});

el("featherRange").addEventListener("input", (e) => {
  const item = activeItem();
  if (!item) return;
  item.feather = Number(e.target.value);
  el("featherValue").textContent = `${e.target.value}px`;
  renderActive();
});

el("edgeSmoothToggle").addEventListener("change", (e) => {
  const item = activeItem();
  if (!item) return;
  item.smoothEdges = e.target.checked;
  item.feather = e.target.checked ? Math.max(item.feather, 1) : 0;
  el("featherRange").value = item.feather;
  el("featherValue").textContent = `${item.feather}px`;
  renderActive();
});

function syncBackgroundPanelUI(item) {
  document.querySelectorAll(".bg-tabs button").forEach((btn) => btn.classList.toggle("active", btn.dataset.bg === item.bg.type));
  el("bgColorPanel").style.display = item.bg.type === "color" ? "block" : "none";
  el("bgGradientPanel").style.display = item.bg.type === "gradient" ? "block" : "none";
  el("bgImagePanel").style.display = item.bg.type === "image" ? "block" : "none";
  el("bgBlurPanel").style.display = item.bg.type === "blur" ? "block" : "none";
  document.querySelectorAll(".swatch").forEach((s) => s.classList.toggle("active", item.bg.type === "color" && s.style.background === hexToRgbString(item.bg.color)));
  document.querySelectorAll(".gradient-swatch").forEach((s, i) => s.classList.toggle("active", item.bg.type === "gradient" && GRADIENT_PRESETS[i].id === item.bg.gradient.id));
  el("featherRange").value = item.feather;
  el("featherValue").textContent = `${item.feather}px`;
  el("edgeSmoothToggle").checked = item.smoothEdges;
  el("blurRange").value = item.blurAmount || 14;
  el("blurValue").textContent = item.blurAmount || 14;
}
function hexToRgbString(hex) {
  // matches inline style comparisons; browsers normalize style.background to rgb()
  const c = document.createElement("div");
  c.style.background = hex;
  return c.style.background;
}

/* -------------------------------------------------------------------------
 * Compare slider
 * ---------------------------------------------------------------------- */
createCompareSlider(el("compareView"), compareHandle, compareBeforeLayer);

/* -------------------------------------------------------------------------
 * Actions: process, download, process-all
 * ---------------------------------------------------------------------- */
document.addEventListener("click", (e) => {
  // Delegate a "Remove background" trigger from the dropzone hint area if needed later.
});

async function requireProcessed(item) {
  if (item.status !== "done") {
    await processItem(item);
  }
  return activeItem()?.status === "done";
}

async function download(format) {
  const item = activeItem();
  if (!item) return;
  const ok = await requireProcessed(item);
  if (!ok) return;

  const canvas = document.createElement("canvas");
  canvas.width = item.baseCanvas.width;
  canvas.height = item.baseCanvas.height;
  const bgConfig = format === "png" ? resolveBgConfig(item) : ensureOpaqueBg(item);
  await compositeBackground(canvas, item.resultImage, bgConfig, {
    feather: item.feather,
    originalImage: item.baseCanvas,
    blurAmount: item.blurAmount || 14,
  });

  const mime = format === "jpg" ? "image/jpeg" : format === "webp" ? "image/webp" : "image/png";
  const quality = format === "jpg" ? 0.92 : format === "webp" ? 0.9 : undefined;
  const blob = await canvasToBlob(canvas, mime, quality);
  const baseName = item.name.replace(/\.[^.]+$/, "");
  downloadBlob(blob, `${baseName}-cutline.${format}`);
  showToast(`Downloaded ${format.toUpperCase()}.`, "success", 2400);
}

function ensureOpaqueBg(item) {
  // JPG/WebP don't render transparency reliably across viewers — fall back
  // to white if the user picked "None".
  if (item.bg.type === "transparent") return { type: "color", color: "#ffffff" };
  return resolveBgConfig(item);
}

el("downloadPngBtn").addEventListener("click", () => download("png"));
el("downloadJpgBtn").addEventListener("click", () => download("jpg"));
el("downloadWebpBtn").addEventListener("click", () => download("webp"));

el("processAllBtn").addEventListener("click", async () => {
  const pending = queue.filter((q) => q.status !== "done");
  if (pending.length === 0) {
    showToast("Everything in the batch is already processed.", "info", 2600);
    return;
  }
  for (const item of pending) {
    await processItem(item);
  }
  showToast("Batch processing complete.", "success");
});

el("removeBgBtn").addEventListener("click", () => {
  const item = activeItem();
  if (item) processItem(item);
});
el("downloadToolbarBtn").addEventListener("click", () => download("png"));
el("removeBgBtnOverlay").addEventListener("click", () => {
  const item = activeItem();
  if (item) processItem(item);
});

/* -------------------------------------------------------------------------
 * Boot
 * ---------------------------------------------------------------------- */
renderHistoryStrip();
