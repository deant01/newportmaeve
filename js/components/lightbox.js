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

  document.querySelectorAll('.char-card').forEach(card => {
    addEvent(card, 'click', () => {
      const img = card.querySelector('img');
      if (img) openLightbox(img.src, img.alt);
    });
  });

  document.querySelectorAll('.map-container img').forEach(img => {
    addEvent(img, 'click', () => openLightbox(img.src, img.alt));
  });

  addEvent(lb, 'click', closeLightbox);
  addEvent(lbImg, 'click', (e) => e.stopPropagation());
  addEvent(lbClose, 'click', closeLightbox);
  addEvent(document, 'keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
}
