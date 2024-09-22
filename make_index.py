import time
import requests, sqlite3



conn = sqlite3.connect("./index.sqlite")
conn.execute("""CREATE TABLE IF NOT EXISTS id_index (id INT NOT NULL PRIMARY KEY,status INT NOT NULL);""")#status:    0-存疑  1-存在
with open('./history',"r") as f:
    start_index,end_index = f.read().split(",")[0:2]
start_index=int(start_index)
end_index=int(end_index)

error_time=0
for index in range(start_index,end_index+1):
    try:
        code = requests.get(f"https://www.pixiv.net/artworks/{index}").status_code
    except:
        code = 0
    if code == 200:
        conn.execute(f"INSERT INTO id_index VALUES ({index},1)")
        print(str(index)+"  ✅")
    elif code == 404:
        print(str(index)+"  ❌")
    else:
        conn.execute(f"INSERT INTO id_index VALUES ({index},0)")
        print(str(index)+"  ❓")
        error_time+=1
        time.sleep(3)
    with open('./history',"w") as f:
        f.write(str(index)+","+str(end_index))
    conn.commit()
    if error_time>=10:
        time.sleep(300)
        error_time=0