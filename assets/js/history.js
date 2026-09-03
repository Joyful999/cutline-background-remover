/**
 * history.js — keeps a small "recently processed" thumbnail history in
 * localStorage so returning visitors can see (and re-download) recent work.
 * Only compressed, low-res thumbnails are stored to stay well under quota.
 */
import { storage } from "./utils.js";

const KEY = "cutline:history";
const MAX_ITEMS = 10;
const THUMB_SIZE = 160;

/** Build a small JPEG thumbnail data URL from a canvas/image for storage. */
function makeThumbnail(sourceCanvas) {
  const canvas = document.createElement("canvas");
  const ratio = sourceCanvas.width / sourceCanvas.height;
  canvas.width = ratio >= 1 ? THUMB_SIZE : Math.round(THUMB_SIZE * ratio);
  canvas.height = ratio >= 1 ? Math.round(THUMB_SIZE / ratio) : THUMB_SIZE;
  const ctx = canvas.getContext("2d");
  // checkerboard so transparency reads correctly in the thumbnail
  for (let y = 0; y < canvas.height; y += 8) {
    for (let x = 0; x < canvas.width; x += 8) {
      ctx.fillStyle = (x / 8 + y / 8) % 2 === 0 ? "#eee" : "#fff";
      ctx.fillRect(x, y, 8, 8);
    }
  }
  ctx.drawImage(sourceCanvas, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/png");
}

export function getHistory() {
  return storage.get(KEY, []);
}

export function addHistoryEntry({ name, resultCanvas }) {
  const items = getHistory();
  items.unshift({
    id: Date.now().toString(36),
    name: name || "Untitled",
    thumbnail: makeThumbnail(resultCanvas),
    date: new Date().toISOString(),
  });
  storage.set(KEY, items.slice(0, MAX_ITEMS));
}

export function clearHistory() {
  storage.remove(KEY);
}
