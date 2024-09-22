import time
import requests
import sqlite3
from typing import *

end_index = 122589047

def loop(iter:Iterable,new:int=1):
    error_time=0
    for index in iter:
        try:
            code = requests.get(f"https://www.pixiv.net/artworks/{index}").status_code
        except:
            code = 0
        if code == 200:
            if new==1:
                conn.execute(f"INSERT INTO id_index VALUES ({index},1)")
            else:
                conn.execute(f"UPDATE id_index SET status='1' WHERE id={index}")
            print(str(index)+"  ✅")
        elif code == 404:
            if new==1:
                print(str(index)+"  ❌")
            else:
                conn.execute(f"DELETE FROM id_index WHERE id={index}")
        else:
            if new==1:
                conn.execute(f"INSERT INTO id_index VALUES ({index},0)")
            print(str(index)+"  ❓")
            error_time+=1
            time.sleep(3)
        conn.commit()
        if error_time>=10:
            time.sleep(300)
            error_time=0

conn = sqlite3.connect("./index.sqlite")
conn.execute("""CREATE TABLE IF NOT EXISTS id_index (id INT NOT NULL PRIMARY KEY,status INT NOT NULL);""")#status:    0-存疑  1-存在

cursor = conn.cursor()
cursor.execute("SELECT id FROM id_index WHERE status = 0;")
id_list = cursor.fetchall()
loop([x[0] for x in id_list],new=0)

cursor = conn.cursor()
cursor.execute("SELECT MAX(id) FROM id_index;")
max_id = cursor.fetchall()[0][0]
start_index = max_id+1

start_index=start_index
loop(range(start_index,end_index+1))