from script import main
import sqlite3

sqliteConnection = sqlite3.connect(r'traceroute/db.sqlite3')
cursor = sqliteConnection.cursor()


result = main()
query = f"insert into tracert_delay_info(address, delay, hop) values ('{result['address']}', '{result['delay_number']}', '{result['hop_number']}');"

cursor.execute(query)
sqliteConnection.commit()