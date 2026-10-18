// The light switch. Until it's clicked, the page follows the system's
// light or dark preference (that part is CSS). A click picks the other one
// and remembers it. This runs in <head>, so a saved choice applies before
// the page is drawn.
(() => {
  const root = document.documentElement;
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  } catch {}

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".theme-toggle");
    if (!button) return;
    button.hidden = false;
    button.addEventListener("click", () => {
      const dark = root.dataset.theme
        ? root.dataset.theme === "dark"
        : matchMedia("(prefers-color-scheme: dark)").matches;
      root.dataset.theme = dark ? "light" : "dark";
      try {
        localStorage.setItem("theme", root.dataset.theme);
      } catch {}
    });
  });
})();
