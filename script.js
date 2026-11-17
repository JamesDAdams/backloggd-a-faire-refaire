(function () {
  var grid = document.getElementById('grid');
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
  var search = document.getElementById('search');
  var sortSel = document.getElementById('sort');
  var dirBtn = document.getElementById('dir');
  var countEl = document.getElementById('count');
  var emptyEl = document.getElementById('empty');
  var desc = false;

  /* ---------------------------------------------------------------
     Règle d'affichage des dates de sortie :
       - aucune date connue            -> encart « No date » sur la jaquette
       - jeu pas encore sorti          -> bandeau « Soon » + date affichée
       - sorti il y a moins de 3 mois  -> date affichée
       - sorti il y a plus de 3 mois   -> date masquée
     Calculé à l'ouverture de la page, donc toujours à jour.
  ---------------------------------------------------------------- */
  function applyReleaseRule() {
    var now = new Date();
    var cutoff = new Date(now.getTime());
    cutoff.setMonth(cutoff.getMonth() - 3);

    cards.forEach(function (card) {
      // aucune date de sortie connue -> encart « No date »
      if (card.dataset.tba === '1') {
        card.classList.add('is-nodate');
        card.classList.remove('is-soon', 'is-old');
        return;
      }
      card.classList.remove('is-nodate');

      var raw = card.dataset.release;
      var exact = card.dataset.exact === '1';
      var d = new Date(raw + 'T00:00:00');
      if (isNaN(d)) return;

      var isFuture, isRecent;
      if (exact) {
        isFuture = d > now;
        isRecent = !isFuture && d >= cutoff;
      } else {
        // année seule : on considère « à venir » uniquement si l'année est future
        isFuture = d.getFullYear() > now.getFullYear();
        isRecent = true; // date partielle -> on l'affiche toujours
      }

      card.classList.toggle('is-soon', isFuture);
      card.classList.toggle('is-old', !isFuture && !isRecent);
    });
  }

  // petit fade-in des jaquettes une fois chargées
  cards.forEach(function (c) {
    var img = c.querySelector('img');
    if (img.complete) img.classList.add('loaded');
    else img.addEventListener('load', function () { img.classList.add('loaded'); });
  });

  function apply() {
    var q = search.value.trim().toLowerCase();
    var key = sortSel.value;

    var visible = cards.filter(function (c) {
      return !q || c.dataset.title.indexOf(q) !== -1;
    });

    visible.sort(function (a, b) {
      var r;
      if (key === 'release') r = a.dataset.release.localeCompare(b.dataset.release);
      else if (key === 'title') r = a.dataset.title.localeCompare(b.dataset.title, 'fr');
      else r = Number(a.dataset.order) - Number(b.dataset.order);
      return desc ? -r : r;
    });

    cards.forEach(function (c) { c.remove(); });
    visible.forEach(function (c) { grid.appendChild(c); });

    countEl.textContent = visible.length + ' jeu' + (visible.length > 1 ? 'x' : '') +
      ' affiché' + (visible.length > 1 ? 's' : '');
    emptyEl.hidden = visible.length !== 0;
  }

  search.addEventListener('input', apply);
  sortSel.addEventListener('change', apply);
  dirBtn.addEventListener('click', function () {
    desc = !desc;
    dirBtn.classList.toggle('flip', desc);
    dirBtn.textContent = desc ? '↑' : '↓';
    apply();
  });

  applyReleaseRule();
  apply();
})();
