# TODO: Implement shopping_card_update for Buyer-Seller Shipping Negotiation

## Tasks
- [x] Modify templates/shopping_card_update.html to include shipping_fee field and conditional display based on mode (enter, waiting, updated)
- [x] Modify app.py shopping_card_update route to handle modes and POST logic for buyer submitting proposed shipping
- [ ] Add new route /seller_update_cart/<buyer_whatsapp> in app.py for seller to update shipping price
- [ ] Add new route /decline_cart/<whatsapp> in app.py for buyer to decline purchase
- [ ] Create templates/seller_update_cart.html for seller to update shipping price
- [ ] Modify checkout route in app.py to check negotiation_status == 'seller_updated' before proceeding
- [ ] Update src/notifications.py if needed for cart notifications
- [ ] Test the flow: buyer enters shipping, sends to seller, seller updates, sends back, buyer pays or declines
- [ ] Ensure mobile-responsive design with Bootstrap 5

## Status
- Plan approved. Starting implementation.
