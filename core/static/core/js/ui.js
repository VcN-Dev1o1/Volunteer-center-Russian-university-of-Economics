(() => {
  const menuToggle = document.querySelector('.js-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const searchToggles = document.querySelectorAll('.js-search-toggle');
  const searchPanel = document.getElementById('search-panel');
  const searchInput = document.getElementById('site-search');

  const closeMenu = () => {
    if (!mobileMenu || !menuToggle) return;
    mobileMenu.hidden = true;
    menuToggle.setAttribute('aria-expanded', 'false');
  };

  const openMenu = () => {
    if (!mobileMenu || !menuToggle) return;
    mobileMenu.hidden = false;
    menuToggle.setAttribute('aria-expanded', 'true');
  };

  menuToggle?.addEventListener('click', () => {
    if (!mobileMenu) return;
    const isOpen = !mobileMenu.hidden;
    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  const closeSearch = () => {
    if (!searchPanel || !searchToggles.length) return;
    searchPanel.hidden = true;
    searchToggles.forEach((toggle) => toggle.setAttribute('aria-expanded', 'false'));
  };

  const openSearch = () => {
    if (!searchPanel || !searchToggles.length) return;
    searchPanel.hidden = false;
    searchToggles.forEach((toggle) => toggle.setAttribute('aria-expanded', 'true'));
    window.setTimeout(() => searchInput?.focus(), 10);
  };

  searchToggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      if (!searchPanel) return;
      const isOpen = !searchPanel.hidden;
      if (isOpen) {
        closeSearch();
      } else {
        openSearch();
      }
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    closeMenu();
    closeSearch();
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;

    if (mobileMenu && !mobileMenu.hidden) {
      if (!mobileMenu.contains(target) && !menuToggle?.contains(target)) {
        closeMenu();
      }
    }

    if (searchPanel && !searchPanel.hidden) {
      if (!searchPanel.contains(target) && ![...searchToggles].some((toggle) => toggle.contains(target))) {
        closeSearch();
      }
    }
  });
})();