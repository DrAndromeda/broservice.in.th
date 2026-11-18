/* Consent-gated analytics for BroService (progressive enhancement, no dependencies). */
(function () {
  'use strict';
  var cfg = window.BROSERVICE_CONFIG || {};
  var GA = (cfg.ga4MeasurementId || '').trim();
  var FB = (cfg.metaPixelId || '').trim();
  if (!GA && !FB) return;                       // nothing configured: stay completely inert

  var KEY = 'bs_consent';
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { text: 'We would like to use analytics to understand which pages are useful. It is off unless you accept.', yes: 'Accept', no: 'Decline', settings: 'Cookie settings', label: 'Analytics consent' },
    ru: { text: 'Мы хотели бы использовать аналитику, чтобы понимать, какие страницы полезны. Она выключена, пока вы не согласитесь.', yes: 'Принять', no: 'Отклонить', settings: 'Настройки cookie', label: 'Согласие на аналитику' },
    th: { text: 'เราต้องการใช้การวิเคราะห์เพื่อดูว่าหน้าใดมีประโยชน์ และจะปิดไว้จนกว่าคุณจะยอมรับ', yes: 'ยอมรับ', no: 'ปฏิเสธ', settings: 'ตั้งค่าคุกกี้', label: 'ความยินยอมสำหรับการวิเคราะห์' },
    he: { text: 'נשמח להשתמש בניתוח נתונים כדי להבין אילו עמודים שימושיים. הכלי כבוי אלא אם תסכימו.', yes: 'אישור', no: 'דחייה', settings: 'הגדרות עוגיות', label: 'הסכמה לניתוח נתונים' }
  }[lang] || null;
  T = T || { text: '', yes: 'Accept', no: 'Decline', settings: 'Cookie settings', label: 'Analytics consent' };
  if (!T.text) T = { text: 'We would like to use analytics to understand which pages are useful. It is off unless you accept.', yes: 'Accept', no: 'Decline', settings: 'Cookie settings', label: 'Analytics consent' };

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* ignore */ } }
  var optOut = (navigator.globalPrivacyControl === true) || navigator.doNotTrack === '1' || window.doNotTrack === '1';

  function loadScript(src, cb) { var s = document.createElement('script'); s.async = true; s.src = src; if (cb) s.onload = cb; document.head.appendChild(s); }
  function start() {
    if (GA) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      window.gtag('config', GA, { anonymize_ip: true });
      loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA));
    }
    if (FB) {
      /* Meta Pixel base code */
      (function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
        t = b.createElement(e); t.async = true; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', FB); window.fbq('track', 'PageView');
    }
  }

  function banner() {
    if (document.getElementById('bs-consent')) return;
    var d = document.createElement('div');
    d.id = 'bs-consent'; d.setAttribute('role', 'region'); d.setAttribute('aria-label', T.label);
    d.innerHTML = '<p></p><div><button type="button" data-v="granted"></button><button type="button" data-v="denied"></button></div>';
    d.querySelector('p').textContent = T.text;
    var b = d.querySelectorAll('button'); b[0].textContent = T.yes; b[1].textContent = T.no;
    d.addEventListener('click', function (e) {
      var v = e.target && e.target.getAttribute && e.target.getAttribute('data-v');
      if (!v) return; set(v); d.remove(); if (v === 'granted') start();
    });
    document.body.appendChild(d); b[0].focus();
  }

  // Privacy pages: replace the "no analytics" statement with the accurate one.
  function privacy() {
    [].forEach.call(document.querySelectorAll('[data-no-analytics]'), function (e) { e.hidden = true; });
    [].forEach.call(document.querySelectorAll('[data-analytics-notice]'), function (e) { e.hidden = false; });
  }
  function settingsLink() {
    var links = document.querySelectorAll('[data-consent-settings]');
    [].forEach.call(links, function (a) { a.hidden = false; a.textContent = T.settings; a.addEventListener('click', function (e) { e.preventDefault(); try { localStorage.removeItem(KEY); } catch (x) {} banner(); }); });
  }

  function init() {
    privacy(); settingsLink();
    if (optOut) return;
    var c = get();
    if (c === 'granted') start(); else if (c !== 'denied') banner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
