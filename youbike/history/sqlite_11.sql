select distinct 站點名稱,max(更新時間) as 更新時間,行政區,地址,總車輛數,可借,可還
from 台北市youbike
group by  站點名稱
order by 更新時間 DESC
HAVING 站點名稱 like '%三%'