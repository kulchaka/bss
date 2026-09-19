/* Apply before styles paint; URL previews override the saved preference. */
(() => {
  const root = document.documentElement;
  const preview = new URLSearchParams(location.search).get('theme');
  let saved;
  try { saved = localStorage.getItem('bss-theme'); } catch { /* Storage may be disabled. */ }
  const initial = ['light', 'dark'].includes(preview) ? preview : saved === 'light' ? 'light' : 'dark';
  root.dataset.theme = initial;
  const preload = document.createElement('link');
  preload.rel = 'preload'; preload.as = 'image';
  preload.href = initial === 'light' ? './assets/bmw-g20-hero.webp' : './assets/bmw-hero.webp';
  document.head.append(preload);
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    const apply = (theme, persist = false) => {
      root.dataset.theme = theme;
      const light = theme === 'light';
      document.querySelectorAll('img[data-light-src]').forEach(image => {
        const src = light ? image.dataset.lightSrc : image.dataset.darkSrc;
        if (image.getAttribute('src') !== src) image.src = src;
      });
      document.dispatchEvent(new Event('bss:themechange'));
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
    const reduce = matchMedia('(prefers-reduced-motion: reduce)');
    const warmed = new Map();
    const warmTheme = theme => {
      const prefix = theme === 'light' ? 'bmw-g20' : 'bmw';
      if (!warmed.has(theme)) warmed.set(theme, Promise.allSettled(['hero', 'hero-lit', 'detail'].map(asset => {
        const image = new Image(); image.src = `./assets/${prefix}-${asset}.webp`;
        return image.decode();
      })));
      return warmed.get(theme);
    };
    let busy = false;
    let activeTransition;
    reduce.addEventListener('change', () => { if (reduce.matches) activeTransition?.skipTransition(); });
    button.addEventListener('pointerenter', () => warmTheme(root.dataset.theme === 'light' ? 'dark' : 'light'), {passive:true});
    button.addEventListener('focus', () => warmTheme(root.dataset.theme === 'light' ? 'dark' : 'light'));
    button.addEventListener('click', async () => {
      if (busy) return;
      const next = root.dataset.theme === 'light' ? 'dark' : 'light';
      busy = true;
      button.setAttribute('aria-busy', 'true');
      try {
        // Bound image preparation so poor connectivity never blocks the theme control.
        await Promise.race([warmTheme(next), new Promise(resolve => setTimeout(resolve, 1200))]);
        if (document.startViewTransition && !reduce.matches) {
          // Settle entrance motion before snapshots to avoid double text at different offsets.
          document.querySelectorAll('.hero-enter,.reveal').forEach(element => {
            element.getAnimations().forEach(animation => {
              if (animation.effect?.getTiming().iterations !== Infinity) animation.finish();
            });
          });
          activeTransition = document.startViewTransition(async () => {
            apply(next, true);
            await Promise.race([
              Promise.allSettled([...document.querySelectorAll('.hero-image, img[data-light-src]')].map(img => img.decode())),
              new Promise(resolve => setTimeout(resolve, 250))
            ]);
          });
          await activeTransition.finished;
        } else {
          root.classList.toggle('theme-fading', !reduce.matches);
          apply(next, true);
          if (!reduce.matches) await new Promise(resolve => setTimeout(resolve, 650));
        }
      } catch {
        apply(next, true);
      } finally {
        root.classList.remove('theme-fading');
        activeTransition = null;
        busy = false;
        button.removeAttribute('aria-busy');
      }
    });
  });
})();
