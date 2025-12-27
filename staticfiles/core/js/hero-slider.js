document.addEventListener("DOMContentLoaded", () => {
const slides = [
  { bg: "/static/core/img/slide-1.jpg", meta: "...", title: "...", lead: "..." },
  { bg: "/static/core/img/slide-2.jpg", meta: "...", title: "...", lead: "..." },
  { bg: "/static/core/img/slide-3.jpg", meta: "...", title: "...", lead: "..." },
];


  let index = 0;

  const hero = document.getElementById("hero");
  const bg = hero.querySelector(".hero-bg");
  const card = hero.querySelector(".hero-card");
  const dots = document.querySelectorAll(".hero-dot");

  function render(i){
    bg.classList.add("is-fading");
    card.classList.add("is-changing");

    setTimeout(() => {
      bg.src = slides[i].bg;
      card.querySelector(".hero-card__meta").textContent = slides[i].meta;
      card.querySelector(".hero-card__title").textContent = slides[i].title;
      card.querySelector(".hero-card__lead").textContent = slides[i].lead;

      dots.forEach(d => d.classList.remove("hero-dot--active"));
      dots[i].classList.add("hero-dot--active");

      bg.classList.remove("is-fading");
      card.classList.remove("is-changing");
    }, 200);
  }

  dots.forEach(d => {
    d.addEventListener("click", () => {
      index = +d.dataset.i;
      render(index);
    });
  });

  // свайп
  let startX = 0;
  hero.addEventListener("touchstart", e => startX = e.touches[0].clientX);
  hero.addEventListener("touchend", e => {
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) {
      index = dx < 0 ? (index + 1) % slides.length : (index - 1 + slides.length) % slides.length;
      render(index);
    }
  });

  render(index);
});
