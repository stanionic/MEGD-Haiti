# TODO: Implement Shopping Card Update Flow

## 1. Update Models
- [ ] Add `delivery_address` field to `CartItem` model in `models.py`.

## 2. Update Routes in app.py
- [ ] Change `shopping_card_update` route to use `whatsapp` parameter instead of `cart_id`.
- [ ] Update GET logic to determine mode based on negotiation_status.
- [ ] Update POST logic for submitting shipping proposal, sending WhatsApp to seller.
- [ ] Add logic for seller updating shipping and sending back to buyer.
- [ ] Ensure WhatsApp redirects after submissions.

## 3. Update Templates
- [ ] Update `templates/shopping_card_update.html` to handle three modes: enter_shipping, waiting_for_seller, seller_updated.
- [ ] Add forms and buttons accordingly.
- [ ] Update `templates/view_cart.html` to add 'Konfime Achte' button redirecting to `shopping_card_update`.

## 4. Test the Flow
- [ ] Test buyer submitting proposal.
- [ ] Test seller updating price.
- [ ] Test buyer confirming or declining.
- [ ] Ensure mobile responsiveness and WhatsApp integration.

## 5. Final Checks
- [ ] Verify database updates.
- [ ] Check flash messages.
- [ ] Ensure no errors in routes.
