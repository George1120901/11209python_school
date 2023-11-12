import requests
import psycopg2
import threading
import key


# 1.---------------download AQ2.5 data.json--------------
def download_data() -> dict:
    
    aqi_url = f"https://data.moenv.gov.tw/api/v2/aqx_p_02?language=zh&api_key={key.key}"
    response = requests.get(aqi_url)
    response.raise_for_status()
    print('下載成功')
    data=response.json()
    return data
# 1.end-----------------------------------------------------


# 2.---------------create TABLE of sql---------------------
def create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        '''
		CREATE TABLE IF NOT EXISTS taiwan_pm25(
			"id"	SERIAL,
            "城市名稱"	TEXT NOT NULL,
            "縣市名稱"	TEXT NOT NULL,
            "pm25"	INTEGER,
            "時間"	TEXT NOT NULL,
			PRIMARY KEY("id"),
            UNIQUE(城市名稱,時間)
		);
		'''
    )
    conn.commit()
    cursor.close()
    print('Created')
# 2.end-----------------------------------------------------


# 3.---------------Insert data into TABLE----------------------
def insert_data(conn, values: list) -> None:
    cursor = conn.cursor()
    sql = '''
        INSERT INTO TW_pm25(城市名稱, 縣市名稱, pm25, 時間) 
        VALUES(%s,%s,%s,%s)
        ON CONFLICT (城市名稱,時間) DO NOTHING   
    '''
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
# 3.end-----------------------------------------------------

n=0
# 4.---------------Insert data into postgresql-----------------
def update_render_data() -> None:
    data = download_data()
    conn = psycopg2.connect(database=pw.DATABASE,
                                user=pw.USER, 
                                password=pw.PASSWORD, host=pw.HOST, 
                                port="5432")
    create_table(conn)


    for item in data['records']: 
        insert_data(conn,values=[item['site'],item['county'],item['pm25'],item['datacreationdate']])
    
    global n
    if n<10:
       timer = threading.Timer(60*60, update_render_data)
       timer.start()
       n+=1
    else:
        print(f'資料{n}次更新完畢')    
        conn.close()
# 4.end-----------------------------------------



if __name__ == '__main__':
    update_render_data()
