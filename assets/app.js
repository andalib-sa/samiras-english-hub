(() => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) toggle.addEventListener('click', () => { const open = nav.classList.toggle('open'); toggle.setAttribute('aria-expanded', String(open)); });
  const cards = [...document.querySelectorAll('.resource-card')];
  if (!cards.length) return;
  const search = document.querySelector('#resourceSearch'), skill = document.querySelector('#skillFilter'), level = document.querySelector('#levelFilter'), australian = document.querySelector('#australianFilter'), count = document.querySelector('#resultCount');
  function applyFilters(){
    const q=(search?.value||'').trim().toLowerCase(), sv=skill?.value||'all', lv=level?.value||'all', aus=australian?.checked||false; let visible=0;
    cards.forEach(card=>{const matches=(!q||card.dataset.search.includes(q))&&(sv==='all'||card.dataset.skills.split(' ').includes(sv))&&(lv==='all'||card.dataset.levels.split(' ').includes(lv))&&(!aus||card.dataset.australian==='true');card.classList.toggle('hidden',!matches);if(matches)visible++;});
    if(count)count.textContent=`${visible} resource${visible===1?'':'s'} shown`;
  }
  [search,skill,level,australian].filter(Boolean).forEach(el=>el.addEventListener(el.tagName==='INPUT'&&el.type==='search'?'input':'change',applyFilters));
  const params=new URLSearchParams(location.search); const requested=params.get('skill')||location.hash.replace('#','');
  if(skill&&['listen','speak','read','write','practise'].includes(requested)){skill.value=requested;applyFilters();setTimeout(()=>document.querySelector('.filters')?.scrollIntoView({behavior:'smooth',block:'start'}),60);}else applyFilters();
})();
