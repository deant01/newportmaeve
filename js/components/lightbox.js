import { addEvent } from '../lib/event-registry.js';

export function initLightbox() {
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightboxImg');
  const lbClose = document.getElementById('lightboxClose');

  function openLightbox(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt || '';
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    lbImg.src = '';
  }

  // Character cards now navigate to their dedicated sheet pages (anchor href),
  // so they are intentionally not wired to the lightbox here.

  // The homepage map now links to the city page (city.html) instead of opening
  // a lightbox. The full-map lightbox lives on the city page itself.
  // (Lightbox kept initialized here in case other elements use it later.)

  addEvent(lb, 'click', closeLightbox);
  addEvent(lbImg, 'click', (e) => e.stopPropagation());
  addEvent(lbClose, 'click', closeLightbox);
  addEvent(document, 'keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
}
