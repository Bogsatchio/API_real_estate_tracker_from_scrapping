import pandas as pd
import sqlite3


#SQLite database file
db_file = 'real_estate_db.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

#query = "select city, count(*) from real_estate_data group by city"
#query = "select  city, avg(price_sqm) as average_price_sqm, count(distinct, link) as num_of_adverts from real_estate_data group by city;"
#query = "select * from processed_files where file like '%Torun%'"

city = 'Plock'
min_s = 50
max_s = 75
query = f""" 
SELECT strftime('%Y-%m-%d', scrap_time) as scrapped_time, CAST(AVG(price_sqm) AS INTEGER) AS average_price_sqm FROM real_estate_data
WHERE city = '{city}' AND size_m2 > {min_s} AND size_m2 < {max_s}
GROUP BY strftime('%Y-%m-%d', scrap_time)  
"""

print(query)
#query = "select distinct scrap_time from real_estate_data where city='Radom'"

# query = "DELETE FROM processed_files where file like '%Torun%'"
#
# cursor.execute(query)
# conn.commit()
# cursor.close()
# conn.close()


df = pd.read_sql(query, conn)
df.set_index("scrapped_time", inplace=True)
df_json = df.to_dict(orient="index")
df_json = {key: value["average_price_sqm"] for key, value in df_json.items()}

#df.set_index("city", inplace=True)

print(df)
print(df_json)
# json_data = df.to_dict(orient="index")
# print(json_data)

