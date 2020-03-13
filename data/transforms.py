import sqlite3
import pandas as pd

conn = sqlite3.connect('./data/wine_data.sqlite')
c = conn.cursor()

df = pd.read_sql("select country, variety, price, rating, color from wine_data" , conn)

row_count = pd.read_sql("select count(*) as rows from wine_data", conn)


top_df = pd.read_sql("select variety, count(variety) as counts, avg(price) as avgPrice, avg(rating) as avgRating from wine_data group by variety order by counts desc limit 8", conn)
top_df = top_df.round(2)
bottom_df = pd.read_sql("select variety, count(variety) as counts, avg(price) as avgPrice, avg(rating) as avgRating from wine_data group by variety order by counts asc limit 8", conn)
bottom_df = bottom_df.round(2)

percent = pd.read_sql("select count(variety) counts, variety from wine_data group by variety", conn)
percent['contribution'] =  percent['counts'] / row_count['rows'][0] * 100
percent['remainder'] = 100 - percent['contribution']

variety = set(df['variety'])
