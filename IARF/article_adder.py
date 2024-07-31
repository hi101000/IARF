import sqlite3
import sys
from datetime import date

path = sys.argv[1]
title = sys.argv[2]
day = str(date.today()).split('-')


con = sqlite3.connect("articles.db")
cur = con.cursor()
cur.execute(f"""
            INSERT INTO Articles (Title, Path, Date, Year, Month)  
            VALUES ({title}, {path}, {day[2]}, {day[1]}, {day[0]});
            """)
con.commit()
con.close()