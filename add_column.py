import sqlite3

conn = sqlite3.connect('instance/glory2yahpub.db')
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE ads ADD COLUMN ad_type VARCHAR(10) DEFAULT "sell"')
    conn.commit()
    print('ad_type column added successfully')
except sqlite3.OperationalError as e:
    print(f'Error: {e}')

conn.close()
