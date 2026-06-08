import { initCharacters } from './components/characters.js';
import { initSiteLinks } from './components/site-links.js';
import { initLightbox } from './components/lightbox.js';
import { initScrollReveal } from './components/scroll-reveal.js';
import { initScrollHint } from './components/scroll-hint.js';
import { cleanupAll } from './lib/event-registry.js';

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([initSiteLinks(), initCharacters()]);
  initLightbox();
  initScrollReveal();
  initScrollHint();
});

// Ensure event listeners tracked in the registry are removed when the
// page is hidden, navigated away from, or unloaded.
window.addEventListener('pagehide', () => cleanupAll(), { passive: true });
window.addEventListener('beforeunload', () => cleanupAll());
