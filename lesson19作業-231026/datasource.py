import requests
import sqlite3
from datetime import datetime
import key



# download data----------------------------------------------------------------

def __download_aqi_data() -> list:
    aqi_url = f'https://data.moenv.gov.tw/api/v2/aqx_p_07?formate=json&api_key={key.key}'
    response = requests.get(aqi_url)
    response.raise_for_status()
    print('下載成功')
    data = response.json()



# create sql able---------------------------------------
def __create_table(conn: sqlite3.Connection):
    
    sql= '''
		CREATE TABLE IF NOT EXISTS 空氣品質監測站(
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


def __insert_data(conn: sqlite3.Connection, values: list):
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    sql = '''
		REPLACE INTO '空氣品質監測站"("測站編號","測站名稱","測站英文名稱","空品區","城市","鄉鎮","測站地址","經度","緯度","測站類型","更新時間")
		VALUES(?,?,?,?,?,?,?,?,?,?,?)
	'''
    values.append(current_time)
    cursor.execute(sql, values)
    conn.commit()


def update_sqlite_data():
    data = __download_aqi_data()
    conn = sqlite3.connect("空氣品質監測站.db")
    __create_table(conn)
    for item in data['records']:
        __insert_data(conn,values=[item['siteid'],item['sitename'], item['siteengname'], item['areaname'], item['county'], item['township'], item['siteaddress'], item['twd97lon'], item['twd97lat'], item['sitetype']])

        print(item)

        print("更新完成")

    conn.close()
