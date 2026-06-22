/*
 Character-sheet page entry script.
 Reuses the shared lightbox for gallery slots and the "view full sheet" link.
*/
import { addEvent } from './lib/event-registry.js';

function initSheetLightbox() {
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

  // Gallery slot images
  document.querySelectorAll('.gallery-frame img').forEach(img => {
    img.style.cursor = 'zoom-in';
    addEvent(img, 'click', () => open(img.src, img.alt));
  });

  // "View full character sheet" link
  const viewSheet = document.getElementById('viewSheet');
  if (viewSheet) {
    addEvent(viewSheet, 'click', () => {
      open(viewSheet.getAttribute('data-full'), viewSheet.getAttribute('data-alt'));
    });
  }

  addEvent(lb, 'click', close);
  addEvent(lbImg, 'click', (e) => e.stopPropagation());
  if (lbClose) addEvent(lbClose, 'click', close);
  addEvent(document, 'keydown', (e) => { if (e.key === 'Escape') close(); });
}

document.addEventListener('DOMContentLoaded', initSheetLightbox);
