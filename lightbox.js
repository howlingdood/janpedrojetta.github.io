(() => {
  const imgSelector = ".grid img, .featured img";

  // Create lightbox container that matches your CSS (.lightbox + .hidden)
  const lb = document.createElement("div");
  lb.className = "lightbox hidden";
  lb.innerHTML = `
    <span class="close" aria-label="Close">&times;</span>
    <span class="prev" aria-label="Previous">&#10094;</span>
    <img class="lightbox-image" alt="">
    <span class="next" aria-label="Next">&#10095;</span>
  `;
  document.body.appendChild(lb);

  const closeBtn = lb.querySelector(".close");
  const prevBtn = lb.querySelector(".prev");
  const nextBtn = lb.querySelector(".next");
  const imgEl = lb.querySelector(".lightbox-image");

  let currentIndex = -1;

  function allImages() {
    return Array.from(document.querySelectorAll(imgSelector));
  }

  function openAt(index) {
    const imgs = allImages();
    if (!imgs.length) return;

    currentIndex = ((index % imgs.length) + imgs.length) % imgs.length;

    const sourceImg = imgs[currentIndex];
    imgEl.src = sourceImg.src;
    imgEl.alt = sourceImg.alt || "";

    lb.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function close() {
    lb.classList.add("hidden");
    document.body.style.overflow = "";
    imgEl.src = "";
    currentIndex = -1;
  }

  function prev() {
    if (currentIndex === -1) return;
    openAt(currentIndex - 1);
  }

  function next() {
    if (currentIndex === -1) return;
    openAt(currentIndex + 1);
  }

  // Click image -> open (event delegation)
  document.addEventListener("click", (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;

    if (target.matches(imgSelector)) {
      const imgs = allImages();
      const idx = imgs.indexOf(target);
      if (idx !== -1) openAt(idx);
    }
  });

  // Close when clicking background (not the image/buttons)
  lb.addEventListener("click", (e) => {
    if (e.target === lb) close();
  });

  closeBtn.addEventListener("click", close);
  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);

  // Keyboard support
  document.addEventListener("keydown", (e) => {
    if (lb.classList.contains("hidden")) return;

    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") prev();
    if (e.key === "ArrowRight") next();
  });
})();
