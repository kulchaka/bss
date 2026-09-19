/* Independent decorative layer; core navigation and forms never depend on it. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const syncVisibility = () => document.body.classList.toggle('page-asleep', document.hidden);
  document.addEventListener('visibilitychange', syncVisibility);
  syncVisibility();
  document.querySelectorAll('.hero,.services,.process').forEach(section => {
    const light = document.createElement('div');
    light.className = 'studio-light';
    light.setAttribute('aria-hidden', 'true');
    section.prepend(light);
  });
})();
