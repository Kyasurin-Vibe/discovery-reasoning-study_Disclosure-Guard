// Animated introduction player. Plays once when visible, never loops, pauses when off-screen or
// when the tab is hidden, and handles keys only while focus is inside the player.
(function () {
  var player = document.getElementById('player');
  if (!player) return;
  var scenes = Array.prototype.slice.call(player.querySelectorAll('.scene'));
  var segBox = player.querySelector('.segments');
  var toggleBtn = player.querySelector('[data-act="toggle"]');
  var prevBtn = player.querySelector('[data-act="prev"]');
  var nextBtn = player.querySelector('[data-act="next"]');
  var status = document.getElementById('player-status');
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var idx = 0, playing = !reduced, finished = false, visible = false, started = false;

  // Scene selectors double as the progress bar; the active bar's fill animation is the timer.
  var segs = scenes.map(function (scene, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'seg';
    b.setAttribute('aria-label', 'Scene ' + (i + 1) + ' of ' + scenes.length + ': ' + scene.querySelector('.line').textContent);
    b.innerHTML = '<span><i></i></span>';
    b.style.setProperty('--dur', (+scene.getAttribute('data-dur') || 5000) + 'ms');
    b.addEventListener('click', function () { go(i, true); });
    segBox.appendChild(b);
    return b;
  });
  segs.forEach(function (b, i) {
    b.querySelector('i').addEventListener('animationend', function () {
      if (i !== idx) return;
      if (idx < scenes.length - 1) go(idx + 1, false);
      else { finished = true; playing = false; sync(); }
    });
  });

  // The first scene appears without a fade, so it is never left transparent before rendering starts.
  player.classList.add(reduced ? 'reduced' : 'motion', 'first');

  function sync() {
    var paused = !playing || !visible || document.hidden;
    player.classList.toggle('is-paused', paused);
    toggleBtn.textContent = playing ? 'Pause' : 'Play';
    toggleBtn.setAttribute('aria-label', playing ? 'Pause' : (finished ? 'Play from the beginning' : 'Play'));
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === scenes.length - 1;
  }

  function go(i, announce) {
    if (started && i !== idx) player.classList.remove('first');
    idx = Math.max(0, Math.min(scenes.length - 1, i));
    finished = false;
    scenes.forEach(function (s, k) {
      // Removing and re-adding 'active' restarts the scene's CSS animations.
      s.classList.remove('active', 'settled');
      s.setAttribute('aria-hidden', k === idx ? 'false' : 'true');
    });
    segs.forEach(function (b, k) {
      b.classList.remove('active');
      b.classList.toggle('done', k < idx);
      b.setAttribute('aria-current', k === idx ? 'step' : 'false');
    });
    void player.offsetWidth;
    // A scene opened while paused is shown complete rather than frozen before its first frame.
    if (!playing) scenes[idx].classList.add('settled');
    scenes[idx].classList.add('active');
    segs[idx].classList.add('active');
    if (announce) status.textContent = 'Scene ' + (idx + 1) + ' of ' + scenes.length + ': ' + scenes[idx].querySelector('.line').textContent;
    sync();
  }

  player.addEventListener('click', function (e) {
    var act = e.target.closest && e.target.closest('[data-act]');
    if (!act) return;
    var a = act.getAttribute('data-act');
    if (a === 'toggle') {
      if (finished) { playing = true; go(0, true); return; }
      playing = !playing;
      sync();
    } else if (a === 'next') go(idx + 1, true);
    else if (a === 'prev') go(idx - 1, true);
    else if (a === 'replay') { playing = !reduced; go(0, true); }
  });

  // Keyboard: only while focus is inside the player. Space toggles only when the player itself
  // is focused (buttons keep their native Space/Enter behaviour). Arrows are not captured elsewhere.
  player.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1, true); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1, true); }
    else if ((e.key === ' ' || e.key === 'k') && e.target === player && !reduced) {
      e.preventDefault();
      if (finished) { playing = true; go(0, true); } else { playing = !playing; sync(); }
    }
  });

  // Play once when visible; pause whenever the player leaves the viewport or the tab is hidden.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible && !started) { started = true; go(0, false); }
      sync();
    }, { threshold: 0.35 }).observe(player);
  } else { visible = true; started = true; }
  document.addEventListener('visibilitychange', sync);

  go(0, false);
})();
