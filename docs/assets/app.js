// Progressive enhancement only: every piece of content is in the HTML and readable without this file.
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Compare the findings: collapsed until requested.
  var btn = document.getElementById('compare-btn');
  var panel = document.getElementById('compare-panel');
  if (btn && panel) {
    panel.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      panel.hidden = !open;
    });
  }

  // Show only the requests where the two scores for Opus differ.
  var onlyDiff = document.getElementById('only-diff');
  var table = document.getElementById('score-table');
  if (onlyDiff && table) {
    onlyDiff.addEventListener('change', function () {
      table.classList.toggle('only-diff', onlyDiff.checked);
      if (onlyDiff.checked && btn && btn.getAttribute('aria-expanded') !== 'true') btn.click();
    });
  }

  // Request 12 tabs (WAI-ARIA tabs pattern: arrow keys, Home and End).
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
  }
  if (tabs.length) {
    select(tabs[0], false);
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab, false); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
        else if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === 'Home') next = tabs[0];
        else if (e.key === 'End') next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  }

  // Explanatory motion: start when a section scrolls into view; skipped for reduced motion.
  var observed = document.querySelectorAll('.observe');
  if (reduce || !('IntersectionObserver' in window)) {
    observed.forEach(function (el) { el.classList.add('in-view'); });
    return;
  }
  document.querySelectorAll('.draw').forEach(function (p) {
    if (p.getTotalLength) p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 2);
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in-view'); io.unobserve(en.target); }
    });
  }, { threshold: 0.25 });
  observed.forEach(function (el) { io.observe(el); });
})();
