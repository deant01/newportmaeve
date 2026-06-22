const SERIES_NAME = 'The Newport Maeve Chronicles';

function createCharCard(character) {
  const card = document.createElement('a');
  card.className = 'char-card';
  if (character.slug) card.href = `characters/${character.slug}.html`;

  // Portrait frame (tall). Tries the portrait image; if it isn't uploaded yet,
  // falls back to a styled "Coming soon" frame so the card never looks broken.
  const frame = document.createElement('div');
  frame.className = 'char-frame';

  const portrait = character.portrait || character.image;
  if (portrait) {
    const img = document.createElement('img');
    img.src = portrait;
    img.alt = `${character.name} — ${character.role}, a character from ${SERIES_NAME}`;
    img.loading = 'lazy';
    img.addEventListener('error', () => {
      img.remove();
      frame.classList.add('is-empty');
      const ph = document.createElement('span');
      ph.className = 'frame-empty';
      ph.textContent = 'Coming soon';
      frame.appendChild(ph);
    });
    frame.appendChild(img);
  } else {
    frame.classList.add('is-empty');
    const ph = document.createElement('span');
    ph.className = 'frame-empty';
    ph.textContent = 'Coming soon';
    frame.appendChild(ph);
  }

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
  card.append(frame, overlay);
  return card;
}

export async function initCharacters() {
  const grid = document.querySelector('.char-grid');
  if (!grid) return;

  const response = await fetch('data/characters.json');
  const characters = await response.json();
  grid.replaceChildren(...characters.map(createCharCard));
}
