import os
import time
import youtube_dl
from fs import *

os.environ["http_proxy"] = "http://127.0.0.1:12333"
os.environ["https_proxy"] = "http://127.0.0.1:12333"

##  Use youtube-dl to get url   ##
def getUrl(u):
    url='https://www.youtube.com/watch?v='+u
    
    ydl_opts={}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url,download=False)
    
    for m in meta['formats']:
        if m['format_id']=='140':
            info=m
    return(info['url'])


##  Use ffmpeg to download video segments   ##
def ffDown(url,ts,optstr):
    cmd='ffmpeg -ss {} -i "{}" -t 10 -f wav {}.wav'.format(ts,url,optstr)
    # print(cmd)
    os.system(cmd)


##  Get Selected Segments From Data Set
#   "ds":
#       'e' -> eval_segments
#       'b' -> balanced_segments
#       'u' -> unbalanced_segments
#   "name":
#       'Snoring' & 'Wheeze'
#   "l"
#       Number of segments to get, 0 to scan the whole dataset.
#       Default value is 100

name='Snoring'
ds='b'
seg=getSeg(ds,name,0)

##  Loop through the video ids to download  ##
fail=[]
for s in seg:
    try:
        vid=s[0][:-1]
        ts=int(eval(s[1][:-1]))
        url=getUrl(vid)
        optstr='{0}/{0}_{1}_{2}'.format(name,ds,vid)
        ffDown(url,ts,optstr)
        time.sleep(3)
    except:
        fail.append(vid)
        continue

mssg='Download completed, video id:"{}", total {} segments are failed to download.'.format(','.join(fail),len(fail))
print(mssg)
