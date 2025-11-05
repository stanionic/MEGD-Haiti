import sqlite3

conn = sqlite3.connect('glory2yahpub.db')
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE cart_items ADD COLUMN negotiation_status VARCHAR(20) DEFAULT "cart"')
    conn.commit()
    print('negotiation_status column added successfully')
except sqlite3.OperationalError as e:
    print(f'Error: {e}')

conn.close()
