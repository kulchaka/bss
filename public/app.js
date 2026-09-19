const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const hero = $('.hero');
const heroImage = $('.hero-image');

Promise.allSettled([heroImage.decode(), document.fonts.ready]).then(() => document.body.classList.add('asset-ready'));
$('#year').textContent = new Date().getFullYear();

// Content remains visible with JavaScript disabled or IntersectionObserver unavailable.
if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); revealObserver.unobserve(entry.target); }
    });
  }, { threshold: .08 });
  $$('.service-card.reveal').forEach((el, index) => el.style.setProperty('--reveal-delay', `${index % 2 * 85}ms`));
  $$('.reveal').forEach(el => revealObserver.observe(el));
  document.body.classList.add('motion-ready');
  const sectionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      $$('.desktop-nav a').forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }), { rootMargin: '-20% 0px -55% 0px' });
  ['services', 'approach', 'process'].forEach(id => sectionObserver.observe(document.getElementById(id)));
}

let frame = 0;
const banner = $('.booking-banner');
function updateScroll() {
  frame = 0;
  if (reducedMotion.matches) return;
  const heroRect = hero.getBoundingClientRect();
  if (heroRect.bottom > 0) hero.style.setProperty('--hero-shift', `${Math.min(30, Math.max(0, -heroRect.top * .045))}px`);
  const bannerRect = banner.getBoundingClientRect();
  if (bannerRect.top < innerHeight && bannerRect.bottom > 0) banner.style.setProperty('--banner-shift', `${Math.max(-35, Math.min(35, (innerHeight / 2 - bannerRect.top) * .045))}px`);
}
addEventListener('scroll', () => { if (!frame && !reducedMotion.matches) frame = requestAnimationFrame(updateScroll); }, { passive: true });
reducedMotion.addEventListener('change', () => {
  hero.style.removeProperty('--hero-shift'); banner.style.removeProperty('--banner-shift');
  $('.detail-frame').style.removeProperty('--tilt-x'); $('.detail-frame').style.removeProperty('--tilt-y');
});
const detail = $('.detail-frame');
detail.addEventListener('pointermove', event => {
  if (reducedMotion.matches || event.pointerType !== 'mouse') return;
  const r = detail.getBoundingClientRect();
  detail.style.setProperty('--tilt-x', `${((event.clientX - r.left) / r.width - .5) * 4}deg`);
  detail.style.setProperty('--tilt-y', `${-((event.clientY - r.top) / r.height - .5) * 4}deg`);
});
detail.addEventListener('pointerleave', () => { detail.style.setProperty('--tilt-x', '0deg'); detail.style.setProperty('--tilt-y', '0deg'); });

const menuButton = $('.menu-toggle');
const menu = $('#mobile-menu');
function setMenu(open) {
  menu.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Закрити меню' : 'Відкрити меню');
}
menuButton.addEventListener('click', () => setMenu(menu.hidden));
$$('a', menu).forEach(link => link.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !menu.hidden) { setMenu(false); menuButton.focus(); } });
matchMedia('(min-width: 801px)').addEventListener('change', event => { if (event.matches) setMenu(false); });

const cards = $$('.service-card');
$$('.filter').forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  $$('.filter').forEach(item => { const active = item === button; item.classList.toggle('active', active); item.setAttribute('aria-pressed', String(active)); });
  $('#service-grid').classList.toggle('is-filtered', filter !== 'all');
  let visible = 0;
  cards.forEach(card => {
    card.classList.remove('filter-enter');
    card.hidden = filter !== 'all' && card.dataset.category !== filter;
    if (!card.hidden) { visible++; card.classList.add('is-visible'); }
  });
  requestAnimationFrame(() => cards.filter(card => !card.hidden).forEach(card => card.classList.add('filter-enter')));
  $('#filter-status').textContent = `${visible} напрями сервісу`;
}));

const services = {
  diagnostics: { code: '01 / DIAGNOSTICS', title: 'Комп’ютерна діагностика', description: 'Щоб визначити наступний крок, спершу потрібно зрозуміти ваш автомобіль.', points: ['Обговорення симптомів та поведінки авто', 'Перевірка електронних систем за запитом', 'Пояснення результатів і наступних кроків'] },
  maintenance: { code: '02 / MAINTENANCE', title: 'Технічне обслуговування', description: 'Регулярна увага до деталей, від яких залежить щоденне відчуття вашого BMW.', points: ['Обговорення пробігу та історії обслуговування', 'Узгодження регламентних робіт і матеріалів', 'Рекомендації щодо наступного обслуговування'] },
  software: { code: '03 / SOFTWARE', title: 'Програмне забезпечення', description: 'Електроніка — частина характеру сучасного BMW. Починаємо з вашої моделі та конкретного завдання.', points: ['Оцінка сумісності з конкретним автомобілем', 'Перевірка запиту щодо програмних функцій', 'Узгодження доступних робіт перед початком'] },
  chassis: { code: '04 / CONTROL', title: 'Ходова та гальма', description: 'Те, що поєднує автомобіль із дорогою та робить кожен рух передбачуваним.', points: ['Обговорення шумів, вібрацій та поведінки авто', 'Перевірка вузлів за вашим запитом', 'Узгодження потрібних робіт і деталей'] }
};
const serviceDialog = $('#service-dialog');
const bookingDialog = $('#booking-dialog');
let selectedService = 'consultation';
let dialogOpener = null;

function openDialog(dialog, opener) {
  dialogOpener = opener;
  dialog.showModal();
  document.body.classList.add('dialog-open');
}
$$('dialog').forEach(dialog => {
  $('.dialog-close', dialog).addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    if (!document.querySelector('dialog[open]')) {
      document.body.classList.remove('dialog-open');
      if (dialogOpener?.isConnected) dialogOpener.focus({ preventScroll: true });
    }
  });
});
cards.forEach(card => card.addEventListener('click', () => {
  selectedService = card.dataset.service;
  const info = services[selectedService];
  $('#service-dialog-code').textContent = info.code;
  $('#service-dialog-title').textContent = info.title;
  $('#service-dialog-description').textContent = info.description;
  $('#service-dialog-points').replaceChildren(...info.points.map(point => { const li = document.createElement('li'); li.textContent = point; return li; }));
  openDialog(serviceDialog, card);
}));

function openBooking(opener, service = 'consultation') {
  const focusTarget = menu.contains(opener) ? menuButton : opener;
  setMenu(false);
  $('#booking-form-view').hidden = false;
  $('#booking-summary-view').hidden = true;
  bookingDialog.setAttribute('aria-labelledby', 'booking-dialog-title');
  $('#booking-service').value = service;
  $('#copy-status').textContent = '';
  openDialog(bookingDialog, focusTarget);
}
$$('.book-trigger').forEach(button => button.addEventListener('click', () => openBooking(button)));
$('#service-book').addEventListener('click', () => {
  const originalOpener = dialogOpener;
  serviceDialog.close();
  openBooking(originalOpener, selectedService);
});

let preparedText = '';
$('#booking-form').addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const name = String(data.get('name')).trim();
  const model = String(data.get('model')).trim();
  // Native validation handles missing fields; whitespace-only strings need an explicit check.
  for (const [key, value] of [['name', name], ['model', model]]) {
    const field = event.currentTarget.elements.namedItem(key);
    field.setCustomValidity(value ? '' : 'Будь ласка, заповніть це поле.');
    if (!value) { field.reportValidity(); return; }
  }
  const service = services[data.get('service')]?.title || 'Потрібна консультація';
  const message = String(data.get('message')).trim();
  const rows = [['ВАШЕ ІМ’Я', name], ['АВТОМОБІЛЬ', model], ['НАПРЯМ', service]];
  if (message) rows.push(['ДЕТАЛІ', message]);
  $('#booking-summary').replaceChildren(...rows.map(([label, value]) => {
    const wrap = document.createElement('div');
    const dt = document.createElement('dt'); dt.textContent = label;
    const dd = document.createElement('dd'); dd.textContent = value;
    wrap.append(dt, dd); return wrap;
  }));
  preparedText = `BSS / запит на сервіс\nІм’я: ${name}\nBMW: ${model}\nПослуга: ${service}${message ? `\nДеталі: ${message}` : ''}`;
  $('#booking-form-view').hidden = true;
  $('#booking-summary-view').hidden = false;
  bookingDialog.setAttribute('aria-labelledby', 'booking-summary-title');
  $('#booking-summary-title').focus();
  bookingDialog.scrollTop = 0;
});
$$('input', $('#booking-form')).forEach(input => input.addEventListener('input', () => input.setCustomValidity('')));
$('#edit-request').addEventListener('click', () => {
  $('#booking-summary-view').hidden = true;
  $('#booking-form-view').hidden = false;
  bookingDialog.setAttribute('aria-labelledby', 'booking-dialog-title');
  $('#copy-status').textContent = '';
  $('#booking-form input').focus();
});
$('#copy-request').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(preparedText); $('#copy-status').textContent = 'Запит скопійовано. Запис на сервіс ще не створено.'; }
  catch { $('#copy-status').textContent = 'Копіювання недоступне. Ви можете виділити й скопіювати деталі вище.'; }
});
