import threading
import requests
import sqlite3
from datetime import datetime
import key



# download data----------------------------------------------------------------

def download_aqi_data() -> list:
    aqi_url = f'https://data.moenv.gov.tw/api/v2/aqx_p_07?formate=json&api_key={key.key}'
    response = requests.get(aqi_url)
    response.raise_for_status()
    print('下載成功')
    data = response.json()



# create sql able---------------------------------------
def create_table(conn: sqlite3.Connection):
    print("判斷2 ok")
    sql= '''
		CREATE TABLE IF NOT EXISTS "空氣品質監測站"(
            "id" INTEGER,
            "測站編號" INTEGER,	
			"測站名稱" TEXT NOT NULL,
            "測站英文名稱" TEXT NOT NULL,
			"空品區" TEXT NOT NULL,
			"城市" TEXT NOT NULL,
            "鄉鎮" TEXT NOT NULL,
            "測站地址" TEXT NOT NULL,
			"經度" INTEGER,
			"緯度" INTEGER,
			"測站類型" TEXT NOT NULL,
            "更新時間" TEXT NOT NULL,
			PRIMARY KEY("id" AUTOINCREMENT),
            UNIQUE(測站名稱,更新時間) ON CONFLICT REPLACE
		)
		'''
    cursor=conn.cursor()
    cursor.execute(sql)    
    conn.commit()
    print("判斷3 ok")

def insert_data(conn: sqlite3.Connection, values: list):
    
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')  
    sql = '''
		REPLACE INTO '空氣品質監測站"("測站編號","測站名稱","測站英文名稱","空品區","城市","鄉鎮","測站地址","經度","緯度","測站類型","更新時間")
		VALUES(?,?,?,?,?,?,?,?,?,?,?)
	'''
    values.append(current_time)
    cursor.execute(sql, values)
    cursor.close() 
    conn.close()
    conn.commit()
    


def update_sqlite_data():
    data = download_aqi_data()
    print("判斷4 ok")
    conn = sqlite3.connect("空氣品質監測站.db")
    create_table(conn)
    print("判斷5 ok")
    for item in data:
        insert_data(conn,values=[item['siteid'],item['sitename'], item['siteengname'], item['areaname'], item['county'], item['township'], item['siteaddress'], item['twd97lon'], item['twd97lat'], item['sitetype']])
        print(item)

        print("更新完成")
    conn.close()
    print("判斷6 ok")


