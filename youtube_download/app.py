# 使用模組
from pytube import YouTube
# yt = YouTube('https://www.youtube.com/watch?v=27ob2G3GUCQ')
yt = YouTube('https://youtube.com/live/W7-hxMT-ey0')

# 影片格式分析
print(yt.title)           # 影片標題
print(yt.length)          # 影片長度 ( 秒 )
print(yt.author)          # 影片作者
print(yt.channel_url)     # 影片作者頻道網址
print(yt.thumbnail_url)   # 影片縮圖網址
print(yt.views)           # 影片觀看數
# 分析
# print(yt.streams)
print(yt.streams.all())  # 影片支援哪些畫質
print(len(yt.streams))
for st in yt.streams:
  print(st)

# 下載第1個影片
yt.streams.filter().get_highest_resolution().download(
    output_path='C:/Users/User/Documents/youtube', filename='python_2311129A.mp4')
# yt.streams.get_by_itag(137).download(output_path='C:/Users/User/Documents/youtube', filename='python_230920P.mp4')
# yt.streams.filter().get_by_resolution('1080p').download(output_path='C:/Users/User/Documents/youtube', filename='python_230911P-1.mp4')
# yt.streams.filter().get_by_resolution('360p').download(filename='oxxostudio_360p.mp4')
# 下載 480p 的影片畫質
print('downdload完成')
#yt.streams[0].download('python')