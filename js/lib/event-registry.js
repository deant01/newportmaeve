// Simple event registry to track added listeners and allow cleanup
const registry = [];

export function addEvent(target, type, handler, options) {
  if (!target || !type || !handler) return;
  target.addEventListener(type, handler, options);
  registry.push({ target, type, handler, options });
  return () => removeEvent(target, type, handler, options);
}

export function removeEvent(target, type, handler, options) {
  if (!target || !type || !handler) return;
  try {
    target.removeEventListener(type, handler, options);
  } catch (e) {
    // ignore
  }
  for (let i = registry.length - 1; i >= 0; i--) {
    const r = registry[i];
    if (r.target === target && r.type === type && r.handler === handler) {
      registry.splice(i, 1);
      break;
    }
  }
}

export function cleanupAll() {
  for (let i = registry.length - 1; i >= 0; i--) {
    const { target, type, handler, options } = registry[i];
    try {
      target.removeEventListener(type, handler, options);
    } catch (e) {}
    registry.pop();
  }
}

export default { addEvent, removeEvent, cleanupAll };
