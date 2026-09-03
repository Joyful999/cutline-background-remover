/**
 * editor.js — canvas viewport controls (zoom/pan/fit), geometric transforms
 * (rotate/flip/crop) and the before/after comparison slider.
 */
import { clamp } from "./utils.js";

/**
 * Attaches zoom/pan behaviour to a viewport. `target` is the element that
 * gets transformed (translate + scale); `viewport` is the container that
 * receives wheel/pointer events.
 */
export function createViewport(viewport, target) {
  let scale = 1;
  let x = 0;
  let y = 0;
  let dragging = false;
  let startX = 0;
  let startY = 0;

  function apply() {
    target.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
  }

  function zoomBy(delta, center) {
    const prev = scale;
    scale = clamp(scale + delta, 0.2, 6);
    if (center) {
      // keep the point under the cursor stationary
      const rect = viewport.getBoundingClientRect();
      const cx = center.x - rect.left - rect.width / 2;
      const cy = center.y - rect.top - rect.height / 2;
      x -= cx * (scale / prev - 1);
      y -= cy * (scale / prev - 1);
    }
    apply();
  }

  function fit() {
    scale = 1;
    x = 0;
    y = 0;
    apply();
  }

  viewport.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      zoomBy(-e.deltaY * 0.0015, { x: e.clientX, y: e.clientY });
    },
    { passive: false }
  );

  viewport.addEventListener("pointerdown", (e) => {
    if (scale <= 1) return;
    dragging = true;
    startX = e.clientX - x;
    startY = e.clientY - y;
    viewport.setPointerCapture(e.pointerId);
  });
  viewport.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    x = e.clientX - startX;
    y = e.clientY - startY;
    apply();
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach((evt) =>
    viewport.addEventListener(evt, () => (dragging = false))
  );

  return {
    zoomIn: () => zoomBy(0.2),
    zoomOut: () => zoomBy(-0.2),
    fit,
    reset: fit,
    getScale: () => scale,
  };
}

/**
 * Apply rotate (in 90° steps) and horizontal/vertical flip to a source
 * image, returning a new canvas with the transform baked in.
 * @param {HTMLImageElement|HTMLCanvasElement} source
 * @param {{rotate:number, flipH:boolean, flipV:boolean}} state
 */
export function applyOrientation(source, state) {
  const { rotate = 0, flipH = false, flipV = false } = state;
  const swap = rotate % 180 !== 0;
  const w = source.width || source.naturalWidth;
  const h = source.height || source.naturalHeight;
  const canvas = document.createElement("canvas");
  canvas.width = swap ? h : w;
  canvas.height = swap ? w : h;
  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate((rotate * Math.PI) / 180);
  ctx.scale(flipH ? -1 : 1, flipV ? -1 : 1);
  ctx.drawImage(source, -w / 2, -h / 2, w, h);
  ctx.restore();
  return canvas;
}

/**
 * Crop a source image to a normalized rect {x,y,w,h} (0..1 relative to the
 * image dimensions) and return a new canvas.
 */
export function applyCrop(source, rect) {
  const w = source.width || source.naturalWidth;
  const h = source.height || source.naturalHeight;
  const sx = clamp(rect.x, 0, 1) * w;
  const sy = clamp(rect.y, 0, 1) * h;
  const sw = clamp(rect.w, 0.02, 1) * w;
  const sh = clamp(rect.h, 0.02, 1) * h;
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(sw);
  canvas.height = Math.round(sh);
  const ctx = canvas.getContext("2d");
  ctx.drawImage(source, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
  return canvas;
}

/**
 * Wires up a draggable divider that reveals `beforeEl` on the left and
 * `afterEl` on the right of the handle, clipping the "before" layer.
 */
export function createCompareSlider(wrapEl, handleEl, beforeLayerEl) {
  function setPosition(pct) {
    const clamped = clamp(pct, 0, 100);
    handleEl.style.left = `${clamped}%`;
    beforeLayerEl.style.clipPath = `inset(0 ${100 - clamped}% 0 0)`;
  }
  setPosition(50);

  let dragging = false;
  function fromEvent(e) {
    const rect = wrapEl.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    return ((clientX - rect.left) / rect.width) * 100;
  }
  handleEl.addEventListener("pointerdown", (e) => {
    dragging = true;
    handleEl.setPointerCapture(e.pointerId);
  });
  window.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    setPosition(fromEvent(e));
  });
  window.addEventListener("pointerup", () => (dragging = false));
  wrapEl.addEventListener("click", (e) => {
    if (e.target === handleEl) return;
    setPosition(fromEvent(e));
  });
  handleEl.setAttribute("tabindex", "0");
  handleEl.setAttribute("role", "slider");
  handleEl.setAttribute("aria-label", "Before and after comparison");
  handleEl.setAttribute("aria-valuemin", "0");
  handleEl.setAttribute("aria-valuemax", "100");
  handleEl.addEventListener("keydown", (e) => {
    const current = parseFloat(handleEl.style.left) || 50;
    if (e.key === "ArrowLeft") setPosition(current - 5);
    if (e.key === "ArrowRight") setPosition(current + 5);
  });

  return { setPosition };
}
