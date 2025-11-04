import csv
import os
from flask import Flask
from models import db, Ad

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glory2yahpub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SERVER_NAME'] = 'localhost:5000'  # Configure SERVER_NAME
app.config['PREFERRED_URL_SCHEME'] = 'http'

db.init_app(app)

with app.app_context():
    # Query all approved ads
    approved_ads = Ad.query.filter_by(admin_status='approved').all()

    # Prepare CSV data
    csv_data = []
    for ad in approved_ads:
        title = ad.title or "No Title"
        buttons = "Buy Now"  # Assuming a single button for simplicity
        unique_url = f"http://localhost:5000/shopping_cart/{ad.ad_id}"  # Hardcoded URL
        csv_data.append([title, buttons, unique_url])

    # Write to CSV
    csv_dir = 'csv'
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, 'products.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Buttons', 'Unique URL'])
        writer.writerows(csv_data)

    print(f"CSV generated at {csv_path}")
