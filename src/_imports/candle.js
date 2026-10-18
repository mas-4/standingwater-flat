// The candle. Hold the pointer over the words and a flame lights above
// them: the paper warms and thins, and the page's source shows through
// from underneath. Only over the letters themselves, not blank paper.
// Without this script the paper simply stays opaque.
(() => {
  const sheet = document.querySelector(".sheet");
  if (!sheet || !matchMedia("(hover: hover) and (pointer: fine)").matches) return;

  // Is (x, y) on a letter? Find the text position under the point, then
  // check that the point is inside the box of the character on either side.
  const range = document.createRange();
  const overGlyph = (x, y) => {
    let node, offset;
    if (document.caretPositionFromPoint) {
      const pos = document.caretPositionFromPoint(x, y);
      if (pos) [node, offset] = [pos.offsetNode, pos.offset];
    } else if (document.caretRangeFromPoint) {
      const r = document.caretRangeFromPoint(x, y);
      if (r) [node, offset] = [r.startContainer, r.startOffset];
    }
    if (!node || node.nodeType !== Node.TEXT_NODE || !sheet.contains(node)) return false;
    for (const i of [offset - 1, offset]) {
      if (i < 0 || i >= node.length || /\s/.test(node.data[i])) continue;
      range.setStart(node, i);
      range.setEnd(node, i + 1);
      for (const box of range.getClientRects())
        if (x >= box.left && x <= box.right && y >= box.top && y <= box.bottom) return true;
    }
    return false;
  };

  let x = 0, y = 0, queued = false, dousing = 0;
  const draw = () => {
    queued = false;
    const box = sheet.getBoundingClientRect();
    sheet.style.setProperty("--cx", x - box.left + "px");
    sheet.style.setProperty("--cy", y - box.top + "px");
    if (overGlyph(x, y)) {
      clearTimeout(dousing);
      dousing = 0;
      sheet.classList.add("lit");
    } else if (!dousing && sheet.classList.contains("lit")) {
      // A moment's grace, so it doesn't strobe across the spaces between words
      dousing = setTimeout(() => {
        sheet.classList.remove("lit");
        dousing = 0;
      }, 350);
    }
  };
  sheet.addEventListener("pointermove", (e) => {
    [x, y] = [e.clientX, e.clientY];
    if (!queued) {
      queued = true;
      requestAnimationFrame(draw);
    }
  });
  sheet.addEventListener("pointerleave", () => {
    clearTimeout(dousing);
    dousing = 0;
    sheet.classList.remove("lit");
  });
})();
