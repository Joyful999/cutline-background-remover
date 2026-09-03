/**
 * processor.js — runs AI background removal fully client-side using
 * @imgly/background-removal (WebAssembly + ONNX runtime under the hood).
 * The library is loaded lazily from a CDN as an ES module the first time
 * it's needed, so the initial page load stays light.
 *
 * Different CDNs bundle this package's WASM/onnxruntime-web dependency
 * slightly differently, and any single one can occasionally fail to
 * resolve it. To make this reliable, we try a short list of CDNs in order
 * and fall through to the next one if a given source fails.
 */

const PACKAGE_VERSION = "1.7.0";
const CDN_SOURCES = [
  `https://esm.sh/@imgly/background-removal@${PACKAGE_VERSION}`,
  `https://cdn.jsdelivr.net/npm/@imgly/background-removal@${PACKAGE_VERSION}/+esm`,
  `https://unpkg.com/@imgly/background-removal@${PACKAGE_VERSION}?module`,
];

let removeBackgroundFn = null;
let loadingPromise = null;

/** Lazily import the @imgly/background-removal package, trying each CDN in turn. */
async function loadLibrary() {
  if (removeBackgroundFn) return removeBackgroundFn;
  if (loadingPromise) return loadingPromise;

  loadingPromise = (async () => {
    const errors = [];
    for (const url of CDN_SOURCES) {
      try {
        const mod = await import(/* @vite-ignore */ url);
        // The package's primary export is a default export, not a named one.
        const fn = mod.default || mod.removeBackground;
        if (typeof fn !== "function") {
          throw new Error(`Loaded ${url} but it did not expose a removeBackground function.`);
        }
        removeBackgroundFn = fn;
        return fn;
      } catch (err) {
        console.error(`[CutLine] Failed to load background-removal engine from ${url}`, err);
        errors.push(`${url} → ${err && err.message ? err.message : err}`);
      }
    }
    loadingPromise = null;
    const detail = errors.join(" | ");
    throw new Error(
      `Could not load the AI background removal engine from any source. Check your internet connection, or check the browser console for details. (${detail})`
    );
  })();

  return loadingPromise;
}

/**
 * Remove the background from an image.
 * @param {File|Blob|string} input - a File/Blob or an image URL / data URL.
 * @param {(progress:{key:string, current:number, total:number})=>void} onProgress
 * @returns {Promise<Blob>} a PNG blob with a transparent background.
 */
export async function removeBackground(input, onProgress) {
  const fn = await loadLibrary();
  try {
    return await fn(input, {
      output: { format: "image/png", quality: 1 },
      progress: (key, current, total) => {
        if (typeof onProgress === "function") onProgress({ key, current, total });
      },
    });
  } catch (err) {
    console.error("[CutLine] Background removal failed while processing the image:", err);
    throw new Error(
      `The AI engine loaded but failed while processing this image (${err && err.message ? err.message : "unknown error"}). Try a different photo, or check the browser console for details.`
    );
  }
}

/** Whether the library has already been fetched (useful for UI hints). */
export function isEngineReady() {
  return Boolean(removeBackgroundFn);
}
