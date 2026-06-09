const SERIES_NAME = 'The Newport Maeve Chronicles';

function createCharCard(character) {
  const card = document.createElement('div');
  card.className = 'char-card';

  const img = document.createElement('img');
  img.src = character.image;
  img.alt = `${character.name} — ${character.role}, a character from ${SERIES_NAME}`;
  img.loading = 'lazy';

  const overlay = document.createElement('div');
  overlay.className = 'char-card-overlay';

  const name = document.createElement('div');
  name.className = 'char-card-name';
  name.textContent = character.name;

  const role = document.createElement('div');
  role.className = 'char-card-role';
  role.textContent = character.role;

  const quote = document.createElement('div');
  quote.className = 'char-card-quote';
  quote.textContent = character.quote;

  overlay.append(name, role, quote);
  card.append(img, overlay);
  return card;
}

export async function initCharacters() {
  const grid = document.querySelector('.char-grid');
  if (!grid) return;

  const response = await fetch('data/characters.json');
  const characters = await response.json();
  grid.replaceChildren(...characters.map(createCharCard));
}
