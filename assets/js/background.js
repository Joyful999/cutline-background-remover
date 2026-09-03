/**
 * background.js — composites a cut-out (transparent PNG) foreground onto a
 * chosen background: solid color, gradient, a custom uploaded image, or a
 * blurred version of the original photo. Also applies soft edge feathering.
 */
import { loadImage } from "./utils.js";

export const GRADIENT_PRESETS = [
  { id: "sunset", stops: ["#f5a623", "#ef5b6f"] },
  { id: "ocean", stops: ["#5b5fef", "#34d399"] },
  { id: "violet", stops: ["#7477f5", "#c084fc"] },
  { id: "mono", stops: ["#2a2c37", "#101116"] },
  { id: "mint", stops: ["#34d399", "#f7f7f6"] },
  { id: "flame", stops: ["#ef5b6f", "#f5a623"] },
];

/**
 * Draws the foreground (a transparent-background image) onto a canvas with
 * the requested background treatment.
 *
 * @param {HTMLCanvasElement} canvas - target canvas, sized to the image already
 * @param {HTMLImageElement} foreground - cut-out image (transparent PNG)
 * @param {object} bg - { type: 'transparent'|'color'|'gradient'|'image'|'blur', ... }
 * @param {object} opts - { feather:number(0-20), originalImage?:HTMLImageElement, blurAmount?:number }
 */
export async function compositeBackground(canvas, foreground, bg, opts = {}) {
  const ctx = canvas.getContext("2d");
  const { width, height } = canvas;
  ctx.clearRect(0, 0, width, height);

  switch (bg.type) {
    case "color": {
      ctx.fillStyle = bg.color || "#ffffff";
      ctx.fillRect(0, 0, width, height);
      break;
    }
    case "gradient": {
      const stops = bg.stops || ["#5b5fef", "#34d399"];
      const grad = ctx.createLinearGradient(0, 0, width, height);
      grad.addColorStop(0, stops[0]);
      grad.addColorStop(1, stops[1]);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, width, height);
      break;
    }
    case "image": {
      if (bg.image) {
        drawCover(ctx, bg.image, width, height);
      }
      break;
    }
    case "blur": {
      if (opts.originalImage) {
        ctx.save();
        ctx.filter = `blur(${opts.blurAmount ?? 14}px)`;
        drawCover(ctx, opts.originalImage, width, height);
        ctx.restore();
      }
      break;
    }
    case "transparent":
    default:
      // leave transparent
      break;
  }

  // Draw the foreground, optionally with a soft feather applied via a blurred
  // alpha mask trick: draw twice, first a blurred copy clipped by itself.
  if (opts.feather && opts.feather > 0) {
    const off = document.createElement("canvas");
    off.width = width;
    off.height = height;
    const offCtx = off.getContext("2d");
    offCtx.filter = `blur(${opts.feather}px)`;
    offCtx.drawImage(foreground, 0, 0, width, height);
    offCtx.filter = "none";
    offCtx.globalCompositeOperation = "source-in";
    offCtx.drawImage(foreground, 0, 0, width, height);
    ctx.drawImage(off, 0, 0);
  } else {
    ctx.drawImage(foreground, 0, 0, width, height);
  }
}

function drawCover(ctx, img, width, height) {
  const imgRatio = img.width / img.height;
  const boxRatio = width / height;
  let sx, sy, sw, sh;
  if (imgRatio > boxRatio) {
    sh = img.height;
    sw = sh * boxRatio;
    sx = (img.width - sw) / 2;
    sy = 0;
  } else {
    sw = img.width;
    sh = sw / boxRatio;
    sx = 0;
    sy = (img.height - sh) / 2;
  }
  ctx.drawImage(img, sx, sy, sw, sh, 0, 0, width, height);
}

/** Load a custom background image file and return an HTMLImageElement. */
export async function loadCustomBackground(file) {
  const url = URL.createObjectURL(file);
  const img = await loadImage(url);
  return img;
}
