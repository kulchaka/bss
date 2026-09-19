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

  const hero = document.querySelector('.hero');
  const scene = hero.querySelector('.hero-scene');
  const lit = new Image(1672, 941);
  lit.className = 'hero-image hero-image-lit';
  lit.alt = '';
  lit.src = './assets/bmw-hero-lit.webp';
  const lightButton = document.createElement('button');
  lightButton.type = 'button';
  lightButton.className = 'headlight-toggle';
  lightButton.setAttribute('aria-pressed', 'false');
  lightButton.innerHTML = '<span class="light-icon" aria-hidden="true">◖ ≡</span><span>Світло фар</span><span class="light-state" aria-hidden="true">OFF</span>';
  let lockedLight = false;
  const lightState = active => {
    hero.classList.toggle('headlights-on', active);
    lightButton.querySelector('.light-state').textContent = active ? 'ON' : 'OFF';
  };
  lit.decode().then(() => {
    scene.insertBefore(lit, scene.querySelector('.hero-shade'));
    hero.append(lightButton);
    lightButton.addEventListener('click', () => {
      lockedLight = !lockedLight;
      lightButton.setAttribute('aria-pressed', String(lockedLight));
      lightState(lockedLight);
    });
    hero.addEventListener('pointermove', event => {
      if (event.pointerType !== 'mouse' || lockedLight || reduce.matches) return;
      const rect = hero.getBoundingClientRect();
      lightState((event.clientX - rect.left) / rect.width > .48 && !event.target.closest('button,a'));
    });
    hero.addEventListener('pointerleave', () => lightState(lockedLight));
    reduce.addEventListener('change', () => lightState(lockedLight));
  }).catch(() => { /* Keep original photograph when the optional image fails. */ });

  const hud = document.createElement('div');
  hud.className = 'drive-hud';
  hud.setAttribute('aria-hidden', 'true');
  const marks = Array.from({length: 41}, (_, i) => {
    const angle = (-130 + i * 6.5) * Math.PI / 180;
    const r = i % 5 === 0 ? 78 : 84;
    const point = radius => `${100 + Math.sin(angle) * radius},${100 - Math.cos(angle) * radius}`;
    return `<line x1="${point(r).split(',')[0]}" y1="${point(r).split(',')[1]}" x2="${point(90).split(',')[0]}" y2="${point(90).split(',')[1]}" class="${i > 33 ? 'redline' : ''}"/>`;
  }).join('');
  const numbers = Array.from({length: 9}, (_, i) => {
    const a = (-130 + i * 32.5) * Math.PI / 180;
    return `<text x="${100 + Math.sin(a) * 66}" y="${104 - Math.cos(a) * 66}">${i}</text>`;
  }).join('');
  hud.innerHTML = `<div class="drive-caption">BSS / PRECISION IN MOTION</div><svg viewBox="0 0 200 180"><g class="dial-marks">${marks}</g><g class="dial-numbers">${numbers}</g><g class="dial-needle"><path d="M98 105 100 26 102 105Z"/><circle cx="100" cy="100" r="4"/></g><text class="dial-unit" x="100" y="132">RPM × 1000</text></svg><div class="drive-readout"><span class="drive-mode">SPORT<span>SCROLL DRIVE</span></span><strong class="drive-gear">01</strong><span class="drive-rpm">0800</span></div>`;
  document.body.append(hud);
  const needle = hud.querySelector('.dial-needle');
  const gearText = hud.querySelector('.drive-gear');
  const rpmText = hud.querySelector('.drive-rpm');
  let scheduled = 0;
  const renderDrive = () => {
    scheduled = 0;
    if (reduce.matches) return;
    const total = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const progress = Math.max(0, Math.min(.999999, scrollY / total));
    const phase = progress * 5;
    const gear = Math.floor(phase) + 1;
    const within = phase % 1;
    const rpm = Math.round((gear === 1 ? 800 : 2800) + within * (gear === 1 ? 5600 : 3600));
    needle.style.transform = `rotate(${-130 + rpm / 8000 * 260}deg)`;
    const nextGear = String(gear).padStart(2, '0');
    if (gearText.textContent !== nextGear) {
      gearText.textContent = nextGear;
      gearText.getAnimations().forEach(animation => animation.cancel());
      gearText.animate([{opacity:.25,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:240,easing:'ease-out'});
    }
    rpmText.textContent = String(rpm).padStart(4, '0');
    hud.classList.toggle('is-driving', scrollY > 80);
  };
  const scheduleDrive = () => { if (!scheduled && !reduce.matches && !document.hidden) scheduled = requestAnimationFrame(renderDrive); };
  addEventListener('scroll', scheduleDrive, {passive:true});
  addEventListener('resize', scheduleDrive);
  reduce.addEventListener('change', scheduleDrive);
  document.addEventListener('visibilitychange', scheduleDrive);
  new ResizeObserver(scheduleDrive).observe(document.body);
  scheduleDrive();
})();
