/**
 * theme.js — dark/light mode with saved preference in localStorage.
 * Falls back to the OS preference (prefers-color-scheme) on first visit.
 */
import { storage } from "./utils.js";

const STORAGE_KEY = "cutline:theme";

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", theme === "dark" ? "#101116" : "#fbfbfa");
}

export function initTheme() {
  const saved = storage.get(STORAGE_KEY);
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = saved || (prefersDark ? "dark" : "light");
  applyTheme(theme);

  const toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.setAttribute("aria-pressed", String(theme === "dark"));
    toggle.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      storage.set(STORAGE_KEY, next);
      toggle.setAttribute("aria-pressed", String(next === "dark"));
    });
  }
}
