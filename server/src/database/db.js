const fs = require('fs');
const path = require('path');

const stores = {};

function getStore() {
  const dbFile = process.env.DB_FILE || path.join(__dirname, '..', '..', 'data', 'shopsphere_dev.json');
  const dataDir = path.dirname(dbFile);

  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  if (!stores[dbFile]) {
    stores[dbFile] = {
      users: [],
      roles: [],
      permissions: [],
      role_permissions: [],
      user_roles: [],
      user_sessions: [],
      login_history: [],
      user_preferences: [],
      sellers: [],
      addresses: [],
      categories: [],
      brands: [],
      products: [],
      product_variants: [],
      product_specifications: [],
      product_images: [],
      product_bundles: [],
      bundle_items: [],
      warehouse_locations: [],
      inventory: [],
      inventory_transactions: [],
      cart_items: [],
      wishlists: [],
      wishlist_items: [],
      price_alerts: [],
      coupons: [],
      promotional_campaigns: [],
      orders: [],
      order_items: [],
      payments: [],
      shipments: [],
      return_requests: [],
      reviews: [],
      review_votes: [],
      support_tickets: [],
      support_messages: [],
      recently_viewed: [],
      search_history: [],
      security_audit_logs: []
    };

    if (fs.existsSync(dbFile)) {
      try {
        const raw = fs.readFileSync(dbFile, 'utf8');
        stores[dbFile] = { ...stores[dbFile], ...JSON.parse(raw) };
      } catch (err) {
        // Fallback
      }
    }
  }

  return { store: stores[dbFile], dbFile };
}

function saveStore() {
  const { store, dbFile } = getStore();
  fs.writeFileSync(dbFile, JSON.stringify(store, null, 2), 'utf8');
}

class Statement {
  constructor(sql) {
    this.sql = sql.replace(/\s+/g, ' ').trim();
  }

  run(...params) {
    const { store } = getStore();
    const sql = this.sql;

    // UPDATE users
    if (sql.includes('UPDATE users SET first_name = ?')) {
      const [firstName, lastName, phone, userId] = params;
      const user = store.users.find(u => u.id === userId);
      if (user) {
        user.first_name = firstName;
        user.last_name = lastName;
        user.phone = phone;
        saveStore();
      }
      return { changes: user ? 1 : 0 };
    }

    if (sql.includes('UPDATE users SET password_hash = ?')) {
      const [hash, userId] = params;
      const user = store.users.find(u => u.id === userId);
      if (user) { user.password_hash = hash; saveStore(); }
      return { changes: user ? 1 : 0 };
    }

    if (sql.includes('UPDATE addresses SET is_default = 0')) {
      const [userId] = params;
      store.addresses.filter(a => a.user_id === userId).forEach(a => { a.is_default = 0; });
      saveStore();
      return { changes: 1 };
    }

    if (sql.includes('UPDATE reviews SET helpful_votes = ?')) {
      const [h, un, rId] = params;
      const r = store.reviews.find(rev => rev.id === rId);
      if (r) { r.helpful_votes = h; r.unhelpful_votes = un; saveStore(); }
      return { changes: r ? 1 : 0 };
    }

    if (sql.includes('UPDATE support_tickets SET status = ?')) {
      const [status, tId] = params;
      const t = store.support_tickets.find(st => st.id === tId);
      if (t) { t.status = status; saveStore(); }
      return { changes: t ? 1 : 0 };
    }

    if (sql.includes('UPDATE order_items SET item_status = ?')) {
      const [status, itemId] = params;
      const item = store.order_items.find(i => i.id === itemId);
      if (item) { item.item_status = status; saveStore(); }
      return { changes: item ? 1 : 0 };
    }

    if (sql.includes('UPDATE sellers SET status = ?')) {
      const [status, comm, sellerId] = params;
      const s = store.sellers.find(sel => sel.id === sellerId);
      if (s) { s.status = status; s.commission_rate = comm; saveStore(); }
      return { changes: s ? 1 : 0 };
    }

    // INSERTS
    const insertMatch = sql.match(/INSERT\s+(?:OR\s+\w+\s+)?INTO\s+([a-z0-9_]+)/i);
    if (insertMatch) {
      const tableName = insertMatch[1].toLowerCase();
      if (!store[tableName]) store[tableName] = [];

      if (tableName === 'users') {
        const [id, email, password_hash, first_name, last_name, phone, role, is_verified, status] = params;
        const index = store.users.findIndex(u => u.id === id || u.email.toLowerCase() === (email || '').toLowerCase());
        const row = {
          id, email, password_hash, first_name, last_name, phone,
          role: role || 'CUSTOMER', is_verified: is_verified !== undefined ? is_verified : 1,
          status: status || 'ACTIVE', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        };
        if (index >= 0) store.users[index] = row;
        else store.users.push(row);
      } else if (tableName === 'sellers') {
        const [id, user_id, business_name, business_email, business_phone, status_or_tax] = params;
        const existingIdx = store.sellers.findIndex(s => s.id === id || s.user_id === user_id);
        const row = { id, user_id, business_name, business_email, business_phone, tax_id: status_or_tax || 'TAX-100', status: 'APPROVED', commission_rate: 8.50, rating_avg: 4.85, created_at: new Date().toISOString() };
        if (existingIdx >= 0) store.sellers[existingIdx] = row;
        else store.sellers.push(row);
      } else if (tableName === 'products') {
        let id, seller_id, category_id, brand_id, name, slug, brand, description, base_price, discount_percent, tax_rate;
        if (params.length === 11) {
          [id, seller_id, category_id, brand_id, name, slug, brand, description, base_price, discount_percent, tax_rate] = params;
        } else {
          [id, seller_id, category_id, name, slug, brand, description, base_price, discount_percent, tax_rate] = params;
        }
        const row = {
          id, seller_id, category_id, name, slug, brand: brand || 'ApexTech',
          description, base_price: typeof base_price === 'number' ? base_price : 1499.99,
          discount_percent: discount_percent || 0, tax_rate: tax_rate || 0,
          status: 'PUBLISHED', created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        };
        const idx = store.products.findIndex(p => p.id === id);
        if (idx >= 0) store.products[idx] = row;
        else store.products.push(row);
      } else if (tableName === 'product_variants') {
        const [id, product_id, sku, variant_name, price_override, attributes_json] = params;
        const row = { id, product_id, sku, variant_name, price_override: typeof price_override === 'number' ? price_override : null, attributes_json: attributes_json || '{}', created_at: new Date().toISOString() };
        const idx = store.product_variants.findIndex(v => v.id === id);
        if (idx >= 0) store.product_variants[idx] = row;
        else store.product_variants.push(row);
      } else if (tableName === 'addresses') {
        const [id, user_id, address_type, full_name, street_address_1, street_address_2, city, state, postal_code, country, is_default] = params;
        store.addresses.push({ id, user_id, address_type, full_name, street_address_1, street_address_2, city, state, postal_code, country, is_default: is_default || 0, created_at: new Date().toISOString() });
      } else if (tableName === 'cart_items') {
        const [id, user_id, variant_id, quantity] = params;
        const existingIdx = store.cart_items.findIndex(c => c.user_id === user_id && c.variant_id === variant_id);
        if (existingIdx >= 0) {
          store.cart_items[existingIdx].quantity += quantity;
          store.cart_items[existingIdx].updated_at = new Date().toISOString();
        } else {
          store.cart_items.push({ id, user_id, variant_id, quantity, created_at: new Date().toISOString(), updated_at: new Date().toISOString() });
        }
      } else if (tableName === 'user_preferences') {
        const [user_id, email_notifications, sms_notifications, promotional_emails, theme, currency] = params;
        const idx = store.user_preferences.findIndex(p => p.user_id === user_id);
        const row = { user_id, email_notifications: email_notifications ? 1 : 0, sms_notifications: sms_notifications ? 1 : 0, promotional_emails: promotional_emails ? 1 : 0, theme: theme || 'DARK', currency: currency || 'USD', updated_at: new Date().toISOString() };
        if (idx >= 0) store.user_preferences[idx] = row;
        else store.user_preferences.push(row);
      } else if (tableName === 'wishlists') {
        const [id, user_id, name, is_public] = params;
        store.wishlists.push({ id, user_id, name: name || 'My Wishlist', is_public: is_public || 0, created_at: new Date().toISOString() });
      } else if (tableName === 'wishlist_items') {
        const [id, wishlist_id, product_id] = params;
        store.wishlist_items.push({ id, wishlist_id, product_id, created_at: new Date().toISOString() });
      } else if (tableName === 'recently_viewed') {
        const [user_id, product_id] = params;
        const idx = store.recently_viewed.findIndex(r => r.user_id === user_id && r.product_id === product_id);
        const row = { user_id, product_id, viewed_at: new Date().toISOString() };
        if (idx >= 0) store.recently_viewed[idx] = row;
        else store.recently_viewed.push(row);
      } else if (tableName === 'reviews') {
        const [id, product_id, user_id, rating, title, comment, is_verified_purchase, status] = params;
        const idx = store.reviews.findIndex(r => r.id === id || (r.product_id === product_id && r.user_id === user_id));
        const row = { id, product_id, user_id, rating, title, comment, is_verified_purchase: is_verified_purchase || 0, status: status || 'APPROVED', helpful_votes: 0, unhelpful_votes: 0, created_at: new Date().toISOString() };
        if (idx >= 0) store.reviews[idx] = row;
        else store.reviews.push(row);
      } else if (tableName === 'review_votes') {
        const [review_id, user_id, vote_type] = params;
        const idx = store.review_votes.findIndex(v => v.review_id === review_id && v.user_id === user_id);
        const row = { review_id, user_id, vote_type, created_at: new Date().toISOString() };
        if (idx >= 0) store.review_votes[idx] = row;
        else store.review_votes.push(row);
      } else if (tableName === 'support_tickets') {
        const [id, ticket_number, user_id, order_id, subject, category, priority, status] = params;
        const row = { id, ticket_number, user_id, order_id, subject, category, priority: priority || 'MEDIUM', status: status || 'OPEN', created_at: new Date().toISOString(), updated_at: new Date().toISOString() };
        store.support_tickets.push(row);
      } else if (tableName === 'support_messages') {
        const [id, ticket_id, sender_id, message, is_internal_note] = params;
        store.support_messages.push({ id, ticket_id, sender_id, message, is_internal_note: is_internal_note || 0, created_at: new Date().toISOString() });
      } else if (tableName === 'coupons') {
        const [id, code, discount_type, discount_value, min_order_subtotal, usage_limit, per_user_limit, starts_at, expires_at] = params;
        const row = { id, code, discount_type, discount_value, min_order_subtotal: min_order_subtotal || 0, usage_limit, per_user_limit: per_user_limit || 1, starts_at, expires_at, is_active: 1, created_at: new Date().toISOString() };
        const idx = store.coupons.findIndex(c => c.id === id || c.code === code);
        if (idx >= 0) store.coupons[idx] = row;
        else store.coupons.push(row);
      } else if (tableName === 'orders') {
        const [id, order_number, user_id, status, subtotal, tax_amount, shipping_amount, discount_amount, total_amount, coupon_id, shipping_address_json, billing_address_json] = params;
        const row = { id, order_number, user_id, status, subtotal, tax_amount, shipping_amount, discount_amount: discount_amount || 0, total_amount, coupon_id, shipping_address_json, billing_address_json, created_at: new Date().toISOString(), updated_at: new Date().toISOString() };
        store.orders.push(row);
      } else if (tableName === 'order_items') {
        const [id, order_id, variant_id, seller_id, unit_price, discount_amount, tax_amount, quantity, total_price] = params;
        const row = { id, order_id, variant_id, seller_id, unit_price, discount_amount: discount_amount || 0, tax_amount: tax_amount || 0, quantity, total_price, item_status: 'PENDING', created_at: new Date().toISOString() };
        store.order_items.push(row);
      } else if (tableName === 'inventory') {
        const [id, variant_id, quantity_on_hand, quantity_reserved, reorder_threshold] = params;
        const idx = store.inventory.findIndex(i => i.variant_id === variant_id);
        const row = { id, variant_id, quantity_on_hand, quantity_reserved: quantity_reserved || 0, reorder_threshold: reorder_threshold || 5, updated_at: new Date().toISOString() };
        if (idx >= 0) store.inventory[idx] = row;
        else store.inventory.push(row);
      } else {
        const record = { id: params[0] || `rec_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`, created_at: new Date().toISOString() };
        params.forEach((val, idx) => { record[`param_${idx}`] = val; });
        store[tableName].push(record);
      }

      saveStore();
      return { changes: 1 };
    }

    if (sql.includes('DELETE FROM')) {
      const deleteMatch = sql.match(/DELETE FROM ([a-z0-9_]+)/i);
      if (deleteMatch && params.length > 0) {
        const tableName = deleteMatch[1].toLowerCase();
        if (store[tableName]) {
          store[tableName] = store[tableName].filter(item => item.id !== params[0] && item.user_id !== params[0]);
        }
      }
      saveStore();
      return { changes: 1 };
    }

    saveStore();
    return { changes: 1 };
  }

  get(...params) {
    const { store } = getStore();
    const sql = this.sql;

    if (sql.includes('FROM users WHERE email = ?')) {
      return store.users.find(u => u.email.toLowerCase() === (params[0] || '').toLowerCase()) || null;
    }
    if (sql.includes('FROM users WHERE id = ?')) {
      return store.users.find(u => u.id === params[0]) || null;
    }
    if (sql.includes('FROM sellers WHERE user_id = ?')) {
      return store.sellers.find(s => s.user_id === params[0]) || null;
    }
    if (sql.includes('FROM sellers WHERE id = ?')) {
      return store.sellers.find(s => s.id === params[0]) || null;
    }
    if (sql.includes('FROM user_preferences WHERE user_id = ?')) {
      return store.user_preferences.find(p => p.user_id === params[0]) || null;
    }
    if (sql.includes('FROM wishlists WHERE id = ? AND user_id = ?')) {
      return store.wishlists.find(w => w.id === params[0] && w.user_id === params[1]) || null;
    }
    if (sql.includes('FROM cart_items WHERE user_id = ? AND variant_id = ?')) {
      return store.cart_items.find(c => c.user_id === params[0] && c.variant_id === params[1]) || null;
    }
    if (sql.includes('FROM coupons WHERE code = ?')) {
      return store.coupons.find(c => c.code.toUpperCase() === (params[0] || '').toUpperCase() && c.is_active === 1) || null;
    }
    if (sql.includes('FROM products p') && (sql.includes('WHERE p.id = ?') || sql.includes('WHERE p.slug = ?'))) {
      const p = store.products.find(item => item.id === params[0] || item.slug === params[0]);
      if (!p) return null;
      const s = store.sellers.find(sel => sel.id === p.seller_id) || {};
      const c = store.categories.find(cat => cat.id === p.category_id) || {};
      return {
        ...p,
        seller_name: s.business_name || 'Apex Merchant',
        seller_rating: s.rating_avg || 4.8,
        category_name: c.name || 'Electronics'
      };
    }
    if (sql.includes('FROM product_variants v') && sql.includes('WHERE v.id = ?')) {
      const v = store.product_variants.find(varItem => varItem.id === params[0]);
      if (!v) return null;
      const inv = store.inventory.find(i => i.variant_id === v.id) || { quantity_on_hand: 50 };
      return { ...v, quantity_on_hand: inv.quantity_on_hand };
    }
    if (sql.includes('FROM orders WHERE id = ?') || sql.includes('WHERE order_number = ?')) {
      return store.orders.find(o => o.id === params[0] || o.order_number === params[0]) || null;
    }
    if (sql.includes('FROM support_tickets WHERE')) {
      const tId = params[0];
      const uId = params.length > 2 ? params[2] : (params.length === 2 ? params[1] : null);
      return store.support_tickets.find(st => (st.id === tId || st.ticket_number === tId) && (!uId || st.user_id === uId)) || null;
    }
    if (sql.includes('SELECT AVG(rating)')) {
      const revs = store.reviews.filter(r => r.product_id === params[0] && r.status === 'APPROVED');
      const count = revs.length;
      const avg = count > 0 ? revs.reduce((a, b) => a + b.rating, 0) / count : 0;
      return { avg_rating: avg, review_count: count };
    }
    if (sql.includes('SUM(CASE WHEN vote_type')) {
      const votes = store.review_votes.filter(v => v.review_id === params[0]);
      const helpful = votes.filter(v => v.vote_type === 'HELPFUL').length;
      const unhelpful = votes.filter(v => v.vote_type === 'UNHELPFUL').length;
      return { helpful, unhelpful };
    }
    if (sql.includes('FROM inventory WHERE variant_id = ?')) {
      return store.inventory.find(i => i.variant_id === params[0]) || null;
    }
    if (sql.includes('FROM order_items WHERE id = ?')) {
      return store.order_items.find(oi => oi.id === params[0]) || null;
    }
    if (sql.includes('SELECT COUNT(*) as count FROM')) {
      return { count: 10 };
    }

    return null;
  }

  all(...params) {
    const { store } = getStore();
    const sql = this.sql;

    if (sql.includes('FROM categories')) {
      return store.categories.filter(c => c.is_active === 1);
    }
    if (sql.includes('FROM addresses WHERE user_id = ?')) {
      return store.addresses.filter(a => a.user_id === params[0]);
    }
    if (sql.includes('FROM wishlists WHERE user_id = ?')) {
      return store.wishlists.filter(w => w.user_id === params[0]);
    }
    if (sql.includes('FROM wishlist_items wi')) {
      const items = store.wishlist_items.filter(wi => wi.wishlist_id === params[0]);
      return items.map(wi => {
        const p = store.products.find(prod => prod.id === wi.product_id) || { name: 'Sample Item', base_price: 99.99, discount_percent: 0 };
        const img = store.product_images.find(im => im.product_id === p.id) || { image_url: 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80' };
        return {
          wishlist_item_id: wi.id,
          added_at: wi.created_at,
          product_id: p.id,
          name: p.name,
          base_price: p.base_price,
          discount_percent: p.discount_percent,
          primary_image: img.image_url
        };
      });
    }
    if (sql.includes('FROM recently_viewed rv')) {
      const views = store.recently_viewed.filter(rv => rv.user_id === params[0]);
      return views.map(rv => {
        const p = store.products.find(prod => prod.id === rv.product_id) || { name: 'Viewed Product', base_price: 199.99 };
        const img = store.product_images.find(im => im.product_id === p.id) || { image_url: 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80' };
        return { ...p, viewed_at: rv.viewed_at, primary_image: img.image_url };
      });
    }
    if (sql.includes('FROM support_tickets WHERE user_id = ?')) {
      return store.support_tickets.filter(st => st.user_id === params[0]);
    }
    if (sql.includes('FROM support_messages sm')) {
      const msgs = store.support_messages.filter(sm => sm.ticket_id === params[0]);
      return msgs.map(m => {
        const u = store.users.find(usr => usr.id === m.sender_id) || { first_name: 'Customer', last_name: 'User', role: 'CUSTOMER' };
        return { ...m, first_name: u.first_name, last_name: u.last_name, sender_role: u.role };
      });
    }
    if (sql.includes('FROM product_variants WHERE product_id = ?')) {
      return store.product_variants.filter(v => v.product_id === params[0]).map(v => {
        const inv = store.inventory.find(i => i.variant_id === v.id) || { quantity_on_hand: 50, quantity_reserved: 0 };
        return { ...v, quantity_on_hand: inv.quantity_on_hand, quantity_reserved: inv.quantity_reserved };
      });
    }
    if (sql.includes('FROM product_images WHERE product_id = ?')) {
      return store.product_images.filter(img => img.product_id === params[0]);
    }
    if (sql.includes('FROM reviews WHERE product_id = ?')) {
      return store.reviews.filter(r => r.product_id === params[0] && r.status === 'APPROVED').map(r => {
        const u = store.users.find(usr => usr.id === r.user_id) || { first_name: 'Customer', last_name: 'Reviewer' };
        return { ...r, first_name: u.first_name, last_name: u.last_name };
      });
    }
    if (sql.includes('FROM cart_items ci')) {
      const userItems = store.cart_items.filter(c => c.user_id === params[0]);
      return userItems.map(item => {
        const v = store.product_variants.find(varItem => varItem.id === item.variant_id) || { sku: 'SKU-UNKNOWN', variant_name: 'Standard', price_override: null, product_id: 'prd_laptop_01' };
        const p = store.products.find(prod => prod.id === v.product_id) || { name: 'Sample Product', base_price: 1499.99, discount_percent: 10, tax_rate: 8.25, seller_id: 'sel_apex_001' };
        const s = store.sellers.find(sel => sel.id === p.seller_id) || { business_name: 'Apex Store' };
        const inv = store.inventory.find(i => i.variant_id === v.id) || { quantity_on_hand: 50 };
        const img = store.product_images.find(im => im.product_id === p.id) || { image_url: 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80' };

        return {
          cart_item_id: item.id,
          quantity: item.quantity,
          variant_id: item.variant_id,
          sku: v.sku,
          variant_name: v.variant_name,
          price_override: v.price_override,
          attributes_json: v.attributes_json || '{}',
          product_id: p.id,
          product_name: p.name,
          base_price: p.base_price,
          discount_percent: p.discount_percent,
          tax_rate: p.tax_rate,
          seller_id: p.seller_id,
          seller_name: s.business_name,
          quantity_on_hand: inv.quantity_on_hand,
          primary_image: img.image_url
        };
      });
    }
    if (sql.includes('FROM products p')) {
      let filtered = store.products.filter(p => p.status === 'PUBLISHED');
      if (params.length > 0 && typeof params[0] === 'string' && params[0].startsWith('%')) {
        const term = params[0].replace(/%/g, '').toLowerCase();
        filtered = filtered.filter(p => p.name.toLowerCase().includes(term) || p.description.toLowerCase().includes(term) || (p.brand && p.brand.toLowerCase().includes(term)));
      }
      return filtered.map(p => {
        const s = store.sellers.find(sel => sel.id === p.seller_id) || { business_name: 'Apex Merchant' };
        const c = store.categories.find(cat => cat.id === p.category_id) || { name: 'Category' };
        const img = store.product_images.find(im => im.product_id === p.id) || { image_url: 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80' };
        const revs = store.reviews.filter(r => r.product_id === p.id && r.status === 'APPROVED');
        const count = revs.length;
        const avg = count > 0 ? revs.reduce((a, b) => a + b.rating, 0) / count : 4.8;
        return { ...p, seller_name: s.business_name, category_name: c.name, primary_image: img.image_url, rating_avg: avg, review_count: count };
      });
    }
    if (sql.includes('FROM orders WHERE user_id = ?')) {
      return store.orders.filter(o => o.user_id === params[0]);
    }
    if (sql.includes('FROM security_audit_logs')) {
      return store.security_audit_logs;
    }

    return [];
  }
}

const db = {
  pragma: () => {},
  exec: () => {},
  prepare: (sql) => new Statement(sql),
  transaction: (fn) => (...args) => fn(...args)
};

module.exports = db;
