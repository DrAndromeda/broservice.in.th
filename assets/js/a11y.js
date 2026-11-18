/* BroService: accessibility enhancements for the mobile menu and sticky contact bar.
   Progressive enhancement only; pages remain usable without this file. */
(function () {
  'use strict';
  var toggle = document.getElementById('menuToggle');
  var drawer = document.getElementById('mobileDrawer');
  var closeBtn = document.getElementById('drawerClose');
  var lastFocus = null;

  if (document.querySelector('.sticky-cta-bar')) {
    document.body.classList.add('has-sticky-cta');
  }
  // Logo is a <div onclick>: make it a real keyboard-operable link.
  var logo = document.querySelector('.logo[onclick]');
  if (logo) {
    logo.setAttribute('role', 'link');
    logo.setAttribute('tabindex', '0');
    logo.setAttribute('aria-label', 'BroService.in.th');
    logo.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); logo.click(); }
    });
  }
  if (!toggle) return;

  function isOpen() {
    // Two template variants: class "open" on the drawer, or inline display:block (injected drawer).
    return !!drawer && (drawer.classList.contains('open') || drawer.style.display === 'block');
  }

  function sync() {
    var open = isOpen();
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      var first = (closeBtn || (drawer && drawer.querySelector('a, button')));
      if (first && typeof first.focus === 'function') first.focus();
    } else if (lastFocus && document.activeElement && drawer && drawer.contains(document.activeElement)) {
      lastFocus.focus();
    }
  }

  toggle.setAttribute('aria-haspopup', 'true');
  if (drawer) {
    if (!drawer.id) drawer.id = 'mobileDrawer';
    toggle.setAttribute('aria-controls', drawer.id);
  }
  toggle.setAttribute('aria-expanded', 'false');

  toggle.addEventListener('click', function () {
    lastFocus = toggle;
    window.setTimeout(sync, 0);
  });
  if (closeBtn) closeBtn.addEventListener('click', function () { window.setTimeout(sync, 0); });

  // Some templates inject the drawer after load; observe it as well.
  var obs = new MutationObserver(function () {
    drawer = document.getElementById('mobileDrawer') || drawer;
    if (drawer && !toggle.getAttribute('aria-controls')) toggle.setAttribute('aria-controls', drawer.id);
    sync();
  });
  obs.observe(document.body, { attributes: true, attributeFilter: ['class', 'style'], subtree: true, childList: true });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    drawer = document.getElementById('mobileDrawer') || drawer;
    if (!isOpen()) return;
    var c = document.getElementById('drawerClose');
    if (c) { c.click(); } else if (drawer) { drawer.style.display = 'none'; }
    toggle.focus();
    window.setTimeout(sync, 0);
  });
})();
