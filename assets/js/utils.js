/**
 * utils.js — small, dependency-free helper functions shared across modules.
 */

/** Format a byte count into a human readable string. */
export function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes < 0) return "—";
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const i = Math.min(units.length - 1, Math.floor(Math.log(bytes) / Math.log(1024)));
  const value = bytes / Math.pow(1024, i);
  return `${value >= 10 || i === 0 ? Math.round(value) : value.toFixed(1)} ${units[i]}`;
}

/** Debounce a function call. */
export function debounce(fn, wait = 150) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

/** Clamp a number between min and max. */
export function clamp(n, min, max) {
  return Math.min(max, Math.max(min, n));
}

/** Read a File as a data URL, resolving with the string. */
export function fileToDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

/** Load an HTMLImageElement from a URL/dataURL/blob URL. */
export function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = (e) => reject(e);
    img.src = src;
  });
}

/** Safe localStorage getters/setters that never throw (private/blocked storage). */
export const storage = {
  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem(key);
      return raw === null ? fallback : JSON.parse(raw);
    } catch {
      return fallback;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch {
      return false;
    }
  },
  remove(key) {
    try {
      localStorage.removeItem(key);
    } catch {
      /* ignore */
    }
  },
};

/** Convert a canvas to a Blob (Promise wrapper around toBlob). */
export function canvasToBlob(canvas, type = "image/png", quality) {
  return new Promise((resolve) => canvas.toBlob(resolve, type, quality));
}

/** Trigger a client-side download of a Blob. */
export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

/** Generate a short unique id (not cryptographically secure, fine for UI keys). */
export function uid() {
  return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
}

/* -------------------------------------------------------------------------
 * Toast notifications
 * ---------------------------------------------------------------------- */
let toastRegion = null;
function ensureToastRegion() {
  if (toastRegion) return toastRegion;
  toastRegion = document.createElement("div");
  toastRegion.className = "toast-region";
  toastRegion.setAttribute("role", "status");
  toastRegion.setAttribute("aria-live", "polite");
  document.body.appendChild(toastRegion);
  return toastRegion;
}

/**
 * Show a toast notification.
 * @param {string} message
 * @param {"info"|"success"|"error"} type
 * @param {number} duration ms before auto-dismiss (0 = persistent)
 */
export function showToast(message, type = "info", duration = 4200) {
  const region = ensureToastRegion();
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span><button class="close" aria-label="Dismiss notification">&times;</button>`;
  const remove = () => {
    toast.style.animation = "toast-in 160ms ease-out reverse";
    setTimeout(() => toast.remove(), 150);
  };
  toast.querySelector(".close").addEventListener("click", remove);
  region.appendChild(toast);
  if (duration > 0) setTimeout(remove, duration);
  return toast;
}
