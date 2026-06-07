import { initCharacters } from './components/characters.js';
import { initSiteLinks } from './components/site-links.js';
import { initLightbox } from './components/lightbox.js';
import { initScrollReveal } from './components/scroll-reveal.js';

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([initSiteLinks(), initCharacters()]);
  initLightbox();
  initScrollReveal();
});
