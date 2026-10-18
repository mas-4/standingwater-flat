// The light switch. Until it's flipped, the page follows the system's
// light or dark preference (that part is CSS). Flipping it picks the other
// one and remembers it. This runs in <head>, so a saved choice applies
// before the page is drawn.
(() => {
  const root = document.documentElement;
  const system = matchMedia("(prefers-color-scheme: dark)");
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  } catch {}

  const isDark = () => (root.dataset.theme ? root.dataset.theme === "dark" : system.matches);

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".theme-toggle");
    if (!button) return;
    const show = () => button.setAttribute("aria-checked", String(isDark()));
    button.hidden = false;
    show();
    system.addEventListener("change", show);
    button.addEventListener("click", () => {
      root.dataset.theme = isDark() ? "light" : "dark";
      try {
        localStorage.setItem("theme", root.dataset.theme);
      } catch {}
      show();
    });
  });
})();
