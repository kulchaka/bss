/* Apply before styles paint; URL previews override the saved preference. */
(() => {
  const root = document.documentElement;
  const preview = new URLSearchParams(location.search).get('theme');
  let saved;
  try { saved = localStorage.getItem('bss-theme'); } catch { /* Storage may be disabled. */ }
  const initial = ['light', 'dark'].includes(preview) ? preview : saved === 'light' ? 'light' : 'dark';
  root.dataset.theme = initial;
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    const apply = (theme, persist = false) => {
      root.dataset.theme = theme;
      const light = theme === 'light';
      button.setAttribute('aria-pressed', String(light));
      button.title = light ? 'Увімкнути темну тему' : 'Увімкнути світлу тему';
      document.querySelector('meta[name="theme-color"]')?.setAttribute('content', light ? '#f4f5f7' : '#080a0d');
      if (persist) {
        try { localStorage.setItem('bss-theme', theme); } catch { /* Theme still works without storage. */ }
        const url = new URL(location.href);
        if (url.searchParams.has('theme')) {
          url.searchParams.set('theme', theme);
          history.replaceState(null, '', url);
        }
      }
    };
    button.hidden = false;
    apply(initial);
    button.addEventListener('click', () => apply(root.dataset.theme === 'light' ? 'dark' : 'light', true));
  });
})();
