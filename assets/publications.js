document.addEventListener('DOMContentLoaded', () => {
  const cards = [...document.querySelectorAll('.pub-card')];
  const container = document.getElementById('filterContainer');
  if (!container) return;
  const search = document.getElementById('publication-search');
  const count = document.getElementById('publication-count');
  const categories = card => (card.dataset.tags || '').split(',').map(t => t.trim());
  const tags = [...new Set(cards.flatMap(categories))].sort((a,b) => {
    const ay = /^\d{4}$/.test(a), by = /^\d{4}$/.test(b);
    return ay && by ? Number(b)-Number(a) : ay ? -1 : by ? 1 : a.localeCompare(b);
  });
  let selected = 'all';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      card.hidden = !((selected === 'all' || categories(card).includes(selected)) && card.textContent.toLocaleLowerCase().includes(query));
      if (!card.hidden) visible++;
    });
    count.textContent = visible ? `${visible} of ${cards.length} publications` : 'No publications match. Try another search or select All Publications.';
    container.querySelectorAll('button').forEach(button => {
      const active = button.dataset.filter === selected;
      button.setAttribute('aria-pressed', String(active));
      button.classList.toggle('active', active);
    });
  }
  ['all', ...tags].forEach(tag => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'filter-btn';
    button.dataset.filter = tag; button.textContent = tag === 'all' ? 'All Publications' : tag;
    button.addEventListener('click', () => { selected = tag; update(); });
    container.append(button);
  });
  search.addEventListener('input', update);
  document.querySelector('.publication-controls').hidden = false;
  update();
});
