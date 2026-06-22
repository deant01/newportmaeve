/*
 City page entry script. Reuses the shared lightbox for the "view full map" link.
*/
import { addEvent } from './lib/event-registry.js';

function initCityLightbox() {
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightboxImg');
  const lbClose = document.getElementById('lightboxClose');
  if (!lb || !lbImg) return;

  function open(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt || '';
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    lbImg.src = '';
  }

  const viewMap = document.getElementById('viewMap');
  if (viewMap) {
    addEvent(viewMap, 'click', () => {
      open(viewMap.getAttribute('data-full'), viewMap.getAttribute('data-alt'));
    });
  }

  // Optional: clicking a district image opens it in the lightbox too
  document.querySelectorAll('.district-frame img').forEach(img => {
    img.style.cursor = 'zoom-in';
    addEvent(img, 'click', () => open(img.src, img.alt));
  });

  addEvent(lb, 'click', close);
  addEvent(lbImg, 'click', (e) => e.stopPropagation());
  if (lbClose) addEvent(lbClose, 'click', close);
  addEvent(document, 'keydown', (e) => { if (e.key === 'Escape') close(); });
}

function initDistrictReveal() {
  const cards = document.querySelectorAll('.district-card');
  if (!cards.length) return;

  // If reduced motion is preferred, show everything immediately.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    cards.forEach(c => c.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  cards.forEach(c => observer.observe(c));
}

document.addEventListener('DOMContentLoaded', () => {
  initCityLightbox();
  initDistrictReveal();
});
