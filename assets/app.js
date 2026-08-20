(() => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  const cards = [...document.querySelectorAll('.resource-card')];
  if (!cards.length) return;
  const search = document.querySelector('#resourceSearch');
  const skill = document.querySelector('#skillFilter');
  const level = document.querySelector('#levelFilter');
  const collection = document.querySelector('#collectionFilter');
  const australian = document.querySelector('#australianFilter');
  const count = document.querySelector('#resultCount');

  function applyFilters() {
    const q = (search?.value || '').trim().toLowerCase();
    const skillValue = skill?.value || 'all';
    const levelValue = level?.value || 'all';
    const collectionValue = collection?.value || 'all';
    const ausOnly = australian?.checked || false;
    let visible = 0;
    cards.forEach(card => {
      const matches = (!q || card.dataset.search.includes(q)) &&
        (skillValue === 'all' || card.dataset.skills.split(' ').includes(skillValue)) &&
        (levelValue === 'all' || card.dataset.levels.split(' ').includes(levelValue)) &&
        (collectionValue === 'all' || card.dataset.collection === collectionValue) &&
        (!ausOnly || card.dataset.australian === 'true');
      card.classList.toggle('hidden', !matches);
      if (matches) visible++;
    });
    if (count) count.textContent = `${visible} resource${visible === 1 ? '' : 's'} shown`;
  }

  [search, skill, level, collection, australian].filter(Boolean).forEach(el => {
    el.addEventListener(el.tagName === 'INPUT' && el.type === 'search' ? 'input' : 'change', applyFilters);
  });

  function applyHashSkill(scroll = true) {
    const hashSkill = location.hash.replace('#','');
    if (skill && ['listen','speak','read','write','practise'].includes(hashSkill)) {
      skill.value = hashSkill;
      applyFilters();
      if (scroll) setTimeout(() => document.querySelector('.filters')?.scrollIntoView({behavior:'smooth', block:'start'}), 60);
      return true;
    }
    return false;
  }

  window.addEventListener('hashchange', () => applyHashSkill(true));
  if (!applyHashSkill(true)) applyFilters();
})();
