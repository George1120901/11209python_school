import requests
import sqlite3
from datetime import datetime
import json
import auth_id

#download data-----------------
def __download_aqi_data()->list[dict]:
    aqi_url = f'https://data.moenv.gov.tw/api/v2/aqx_p_07?formate=json&api_key={auth_id.key}'
    response = requests.get(aqi_url)
    response.raise_for_status()
    print('下載成功')
    data = response.json()
    #print(data)
    with open('data.json','w', encoding='utf-8') as file:
        json.dump(data['records'],file,ensure_ascii=False)
f = open('data.json','r', encoding='utf-8')
list_json=list(f)
#print(f)

#create sqlite table---------------------
def __create_table(conn:sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        '''
		CREATE TABLE IF NOT EXISTS 空氣品質AQI(
            "id" INTEGER,
			"測站名稱" TEXT NOT NULL,
            "測站英文名稱" TEXT NOT NULL,
			"空品區" TEXT NOT NULL,
			"城市" TEXT NOT NULL,
            "鄉鎮" TEXT NOT NULL,
            "測站地址" TEXT NOT NULL,
			"經度" TEXT,
			"緯度" TEXT,
			"測站類型" TEXT NOT NULL,
            "測站編號" TEXT NOT NULL,
            "更新時間" TEXT NOT NULL,
			PRIMARY KEY("id" AUTOINCREMENT),
            UNIQUE(測站名稱,更新時間) ON CONFLICT REPLACE
		);
		'''
    )
    conn.commit()


def __insert_data(conn:sqlite3.Connection,values:list[any])->None:
    cursor = conn.cursor()
    load_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = '''
		REPLACE INTO 空氣品質AQI(測站名稱,測站英文名稱,空品區,城市,鄉鎮,測站地址,經度,緯度,測站類型,測站編號,測站編號,更新時間)
		values(?,?,?,?,?,?,?,?,?,?,?)
	'''
    values.append(load_time) 
    cursor.execute(sql,values)
    conn.commit()

def update_sqlite_data()->None:
    #data = list_json
    data = __download_aqi_data()
    conn = sqlite3.connect("空氣品質AQI.db")
    __create_table(conn)
    for item in data:
    #for n in list_json:
        #__insert_data(conn,values=[n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7],n[8],n[9]])
        ##print(item)
        __insert_data(conn,values=[item['siteid'],item['sitename'], item['siteengname'], item['areaname'], item['county'], item['township'], item['siteaddress'], item['twd97lon'], item['twd97lat'], item['sitetype']])
    conn.close()