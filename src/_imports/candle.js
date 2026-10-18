// The candle. Where the pointer is, the paper warms and thins, and the
// page's source shows through from underneath. This is the site's only
// script; without it the paper simply stays opaque.
(() => {
  const sheet = document.querySelector(".sheet");
  if (!sheet || !matchMedia("(hover: hover) and (pointer: fine)").matches) return;

  let x = 0, y = 0, queued = false;
  const draw = () => {
    queued = false;
    sheet.style.setProperty("--cx", x + "px");
    sheet.style.setProperty("--cy", y + "px");
  };
  sheet.addEventListener("pointermove", (e) => {
    const box = sheet.getBoundingClientRect();
    x = e.clientX - box.left;
    y = e.clientY - box.top;
    if (!queued) {
      queued = true;
      requestAnimationFrame(draw);
    }
  });
  sheet.addEventListener("pointerenter", () => sheet.classList.add("lit"));
  sheet.addEventListener("pointerleave", () => sheet.classList.remove("lit"));
})();
