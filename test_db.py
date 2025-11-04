import sqlite3

conn = sqlite3.connect('glory2yahpub.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('Tables:', tables)

# Check if ads_owner table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ads_owner'")
ads_owner_table = cursor.fetchone()
print('ads_owner table exists:', ads_owner_table is not None)

# Check columns in ads_owner if it exists
if ads_owner_table:
    cursor.execute("PRAGMA table_info(ads_owner)")
    columns = cursor.fetchall()
    print('ads_owner columns:', columns)

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = cursor.fetchall()
print('All tables:', all_tables)

conn.close()
