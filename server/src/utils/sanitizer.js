function sanitizeString(str) {
  if (typeof str !== 'string') return str;
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

function sanitizeObject(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) {
    return obj.map(sanitizeObject);
  }
  const sanitized = {};
  for (const [key, value] of Object.entries(obj)) {
    sanitized[key] = typeof value === 'string' ? sanitizeString(value) : sanitizeObject(value);
  }
  return sanitized;
}

module.exports = {
  sanitizeString,
  sanitizeObject
};
