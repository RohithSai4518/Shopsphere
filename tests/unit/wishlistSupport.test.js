const assert = require('assert');
const test = require('node:test');

process.env.NODE_ENV = 'test';
process.env.DB_FILE = './data/test_wishlistSupport.json';

const WishlistService = require('../../server/src/services/wishlistService');
const ReviewService = require('../../server/src/services/reviewService');
const SupportService = require('../../server/src/services/supportService');
const InventoryLedgerService = require('../../server/src/services/inventoryLedgerService');
const { seedDatabase } = require('../../server/src/database/seed.js');

test('Wishlist, Review, Support & Ledger Integration Tests', async (t) => {
  seedDatabase();

  const userId = 'usr_customer_001';

  await t.test('1. Should create custom wishlist and add item', () => {
    const wishlists = WishlistService.createWishlist(userId, 'Holiday Tech List', false);
    assert.ok(wishlists.length > 0);
    const target = wishlists.find(w => w.name === 'Holiday Tech List');
    assert.ok(target);

    const updated = WishlistService.addItem(userId, target.id, 'prd_laptop_01');
    assert.ok(updated);
  });

  await t.test('2. Should record product review and handle helpful votes', () => {
    const rev = ReviewService.createReview(userId, {
      productId: 'prd_earbuds_02',
      rating: 5,
      title: 'Amazing sound quality',
      comment: 'Deep bass and clear highs'
    });
    assert.ok(rev.reviewId);

    const vote = ReviewService.voteReview(userId, rev.reviewId, 'HELPFUL');
    assert.strictEqual(vote.helpful, 1);
  });

  await t.test('3. Should open support ticket and handle agent reply thread', () => {
    const ticket = SupportService.createTicket(userId, {
      subject: 'Order Tracking Help',
      category: 'ORDER_ISSUE',
      priority: 'HIGH',
      initialMessage: 'When will my laptop ship?'
    });

    assert.ok(ticket.ticketId);
    assert.strictEqual(ticket.status, 'OPEN');

    const details = SupportService.getTicketDetails(userId, ticket.ticketId);
    assert.strictEqual(details.messages.length, 1);
  });

  await t.test('4. Should record stock inventory ledger transaction', () => {
    const tx = InventoryLedgerService.recordTransaction('var_laptop_01_32gb', 'RECEIPT', 25, 'RESTOCK', 'RESTOCK-99', 'Warehouse restock');
    assert.ok(tx.txId);
    assert.ok(tx.newQuantityOnHand >= 25);
  });
});
