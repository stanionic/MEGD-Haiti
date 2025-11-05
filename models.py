from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ad(db.Model):
    __tablename__ = 'ads'

    ad_id = db.Column(db.String(36), primary_key=True)
    user_whatsapp = db.Column(db.String(20), nullable=False)
    media_type = db.Column(db.String(10), nullable=False, default='images')  # 'images' or 'video'
    images = db.Column(db.Text)  # Comma-separated filenames for images
    video = db.Column(db.String(255))  # Filename for video
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100))  # New title field
    ad_type = db.Column(db.String(10), nullable=False, default='sell')  # 'publish' or 'sell'
    payment_status = db.Column(db.String(20), default='pending')
    payment_proof = db.Column(db.String(255))
    admin_status = db.Column(db.String(20), default='under_review')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    batch_id = db.Column(db.String(36))
    price_gkach = db.Column(db.Integer, default=100)  # Price in Gkach coins

class Batch(db.Model):
    __tablename__ = 'batches'

    batch_id = db.Column(db.String(36), primary_key=True)
    ads = db.Column(db.Text, nullable=False)
    open_graph_data = db.Column(db.Text)
    facebook_share_url = db.Column(db.Text)
    share_count = db.Column(db.Integer, default=0)
    click_rewards = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserGkach(db.Model):
    __tablename__ = 'user_gkach'

    id = db.Column(db.Integer, primary_key=True)
    user_whatsapp = db.Column(db.String(20), nullable=False, unique=True)
    gkach_balance = db.Column(db.Integer, default=0)
    gkach_requests = db.Column(db.Text)  # JSON string for pending requests
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GkachRate(db.Model):
    __tablename__ = 'gkach_rates'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False, unique=True)  # e.g., 'HTG', 'USD'
    rate_per_gkach = db.Column(db.Float, nullable=False)  # How much currency per 1 Gkach
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Delivery(db.Model):
    __tablename__ = 'deliveries'

    delivery_id = db.Column(db.String(36), primary_key=True)
    ad_id = db.Column(db.String(36), db.ForeignKey('ads.ad_id'), nullable=True)  # Nullable for multiple ads
    buyer_whatsapp = db.Column(db.String(20), nullable=False)
    seller_whatsapp = db.Column(db.String(20), nullable=False)
    delivery_cost = db.Column(db.Integer, default=0)  # In Gkach
    total_price = db.Column(db.Integer, nullable=False)  # Ad price + delivery cost
    status = db.Column(db.String(20), default='negotiating')  # negotiating, accepted, confirmed
    otp = db.Column(db.String(4))  # 4-digit OTP for confirmation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    # New fields for cart functionality
    cart_items = db.Column(db.Text)  # JSON string for multiple cart items
    delivery_address = db.Column(db.Text, nullable=True)  # Store delivery address here

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('ads.ad_id'))  # ad_id as product_id
    quantity = db.Column(db.Integer, default=1)
    shipping_fee_set = db.Column(db.Boolean, default=False)
    shipping_fee = db.Column(db.Float, default=0.0)
    negotiation_status = db.Column(db.String(20), default='cart')  # 'cart', 'buyer_submitted', 'seller_updated'
    cart_id = db.Column(db.String(36), nullable=True)  # Unique ID for each cart submission
    delivery_address = db.Column(db.Text, nullable=True)  # Store delivery address

class Ads_Owner(db.Model):
    __tablename__ = 'ads_owner'

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.String(36), db.ForeignKey('ads.ad_id'), nullable=False)
    buyers_whatsapp = db.Column(db.String(20), nullable=True)
    publishers_whatsapp = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.String(36), db.ForeignKey('deliveries.delivery_id'), nullable=False)
    sender_whatsapp = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
