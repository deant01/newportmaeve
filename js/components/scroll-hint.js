// Scroll hint: scroll to the next section when clicked (and support keyboard)
import { addEvent } from '../lib/event-registry.js';

export function initScrollHint() {
  const hint = document.querySelector('.scroll-hint');
  if (!hint) return;

  // ensure it's keyboard-focusable and looks clickable
  hint.tabIndex = hint.tabIndex >= 0 ? hint.tabIndex : 0;
  hint.style.cursor = 'pointer';

  function scrollToNextSection() {
    const currentSection = hint.closest('section, main, [id]');
    let el = currentSection ? currentSection.nextElementSibling : null;
    while (el && el.nodeType === 1 && el.tagName.toLowerCase() !== 'section' && !el.id) {
      el = el.nextElementSibling;
    }
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      // fallback: scroll down one viewport
      window.scrollBy({ top: window.innerHeight, behavior: 'smooth' });
    }
  }

  addEvent(hint, 'click', scrollToNextSection);
  addEvent(hint, 'keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      scrollToNextSection();
    }
  });
}
