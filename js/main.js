/*
 Main entry script

 - Initializes UI modules on DOMContentLoaded.
 - Contains a small font/image preloading helper that waits for the
   hero image and locally-hosted fonts before revealing the hero.
 - Adds `fonts-loaded` to `<html>` when fonts are ready (or on timeout).
*/
import { initCharacters } from './components/characters.js';
import { initSiteLinks } from './components/site-links.js';
import { initLightbox } from './components/lightbox.js';
import { initScrollReveal } from './components/scroll-reveal.js';
import { initScrollHint } from './components/scroll-hint.js';
import { cleanupAll, addEvent } from './lib/event-registry.js';

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([initSiteLinks(), initCharacters()]);
  initLightbox();
  initScrollReveal();
  initScrollHint();
  // Wait for local fonts (Cinzel + Crimson Text) and hero image before revealing hero
  (function waitForFontsAndHero() {
    const bgEl = document.querySelector('.hero-bg');
    const heroUrl = 'assets/images/cover.webp';
    const img = new Image(); img.src = heroUrl; img.decoding = 'async';

    const loadBg = new Promise((resolve) => {
      if (img.complete) return resolve();
      const onLoad = () => { resolve(); img.removeEventListener('load', onLoad); };
      img.addEventListener('load', onLoad, { passive: true });
      // Fallback: don't wait longer than 3s
      setTimeout(resolve, 3000);
    });

    const loadCinzel = (document.fonts && document.fonts.load) ? document.fonts.load('1em "Cinzel"') : Promise.resolve();
    const loadCrimson = (document.fonts && document.fonts.load) ? document.fonts.load('1em "Crimson Text"') : Promise.resolve();

    Promise.all([loadCinzel, loadCrimson, loadBg]).then(() => {
      document.documentElement.classList.add('fonts-loaded');
      if (bgEl) bgEl.classList.add('bg-loaded');
    }).catch(() => {
      document.documentElement.classList.add('fonts-loaded');
      if (bgEl) bgEl.classList.add('bg-loaded');
    });
  })();
});

// Ensure event listeners tracked in the registry are removed when the
// page is hidden, navigated away from, or unloaded.
window.addEventListener('pagehide', () => cleanupAll(), { passive: true });
window.addEventListener('beforeunload', () => cleanupAll());
