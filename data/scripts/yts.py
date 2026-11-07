import json,re,subprocess,sys,urllib.parse
def search(q):
    url='https://www.youtube.com/results?hl=zh-TW&gl=TW&search_query='+urllib.parse.quote(q)
    h=subprocess.run(['curl','-s','-m','20','-H','Accept-Language: zh-TW','-A','Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36',url],capture_output=True,text=True).stdout
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',h)
    if not m: return []
    d=json.loads(m.group(1)); out=[]
    def walk(o):
        if isinstance(o,dict):
            if 'videoRenderer' in o:
                v=o['videoRenderer']
                try:
                    out.append(dict(u=v['videoId'],title=''.join(r['text'] for r in v['title']['runs']),ch=v['ownerText']['runs'][0]['text'],len=v.get('lengthText',{}).get('simpleText',''),pub=v.get('publishedTimeText',{}).get('simpleText','')))
                except Exception: pass
            for x in o.values(): walk(x)
        elif isinstance(o,list):
            for x in o: walk(x)
    walk(d); return out
if __name__=='__main__':
    for r in search(sys.argv[1])[:10]: print(r)
