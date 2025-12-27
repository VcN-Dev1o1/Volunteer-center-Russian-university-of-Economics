(() => {
  const hero = document.getElementById('hero');
  if (!hero) return;

  const track = document.getElementById('heroSlides');
  const dotsWrap = document.getElementById('heroDots');
  const prevBtn = document.getElementById('heroPrev');
  const nextBtn = document.getElementById('heroNext');

  const metaEl = document.getElementById('heroMeta');
  const titleEl = document.getElementById('heroTitle');
  const leadEl = document.getElementById('heroLead');
  const btnEl = document.getElementById('heroBtn');
  const cardEl = document.getElementById('heroCard');

  if (!track || !dotsWrap || !metaEl || !titleEl || !leadEl || !btnEl || !cardEl) return;

  const slides = Array.from(track.querySelectorAll('.hero-slide'));
  if (!slides.length) return;

  let index = Math.max(0, slides.findIndex(s => s.classList.contains('is-active')));
  let isAnimating = false;

  // dots
  const dots = slides.map((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'hero-dot' + (i === index ? ' hero-dot--active' : '');
    b.setAttribute('aria-label', `Слайд ${i + 1}`);
    b.addEventListener('click', () => goTo(i));
    dotsWrap.appendChild(b);
    return b;
  });

  function render() {
    track.style.transform = `translate3d(${-index * 100}%, 0, 0)`;

    slides.forEach((s, i) => s.classList.toggle('is-active', i === index));
    dots.forEach((d, i) => d.classList.toggle('hero-dot--active', i === index));

    const s = slides[index];
    const date = s.dataset.date || '';
    const editor = s.dataset.editor || '';
    const title = s.dataset.title || '';
    const lead = s.dataset.lead || '';
    const link = s.dataset.link || '#';

    // лёгкая анимация карточки
    cardEl.classList.add('is-changing');
    window.setTimeout(() => {
      metaEl.textContent = `${date} · ${editor}`;
      titleEl.textContent = title;
      leadEl.textContent = lead;
      btnEl.setAttribute('href', link);

      requestAnimationFrame(() => cardEl.classList.remove('is-changing'));
    }, 160);
  }

  function goTo(i) {
    if (isAnimating) return;
    const nextIndex = (i + slides.length) % slides.length;
    if (nextIndex === index) return;

    index = nextIndex;
    isAnimating = true;
    render();
    window.setTimeout(() => { isAnimating = false; }, 700);
  }

  function next() { goTo(index + 1); }
  function prev() { goTo(index - 1); }

  prevBtn?.addEventListener('click', prev);
  nextBtn?.addEventListener('click', next);

  // swipe (простое — без “drag”)
  let startX = null;
  hero.addEventListener('pointerdown', (e) => { startX = e.clientX; });
  hero.addEventListener('pointerup', (e) => {
    if (startX === null) return;
    const dx = e.clientX - startX;
    startX = null;
    if (Math.abs(dx) < 50) return;
    dx < 0 ? next() : prev();
  });

  render();
})();
