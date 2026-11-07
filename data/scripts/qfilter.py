import json,re
PROP=re.compile(r'球|彈力|啞鈴|毛巾|絲巾|斗笠|扇|棍|棒子|彩棒|搖鈴|鈴鼓|手搖鈴|鼓|杯子|紙杯|杯杯|傘|彩帶|彩球|礦泉水|寶特瓶|報紙|樂器|烏克|陶笛|響板|木魚|三角鐵|呼拉圈|繩|手帕|竹竿|筷|器材|道具|沙包|氣球|撲克|卡片|紙|椰子殼|鍋|碗|dumbbell|band|ball|towel|scarf|prop|drum|ukulele|stick',re.I)
PERC=re.compile(r'打擊|percussion',re.I)
Q={}
for l in open('quality.tsv'):
    p=l.rstrip('\n').split('\t')
    if len(p)<4: continue
    u,h,w,t=p
    try: s=min(int(h),int(w))
    except: s=0
    Q[u]=dict(short=s,title=t)
BL=set(['c4mKvsQUtS8', 'G2ewHwi5qYY'])
PERF=re.compile(r'展演|舞蹈秀|舞蹈隊|舞蹈團|團康|才藝|表演')
def check(u,song):
    if u in BL: return 'blacklist'
    q=Q.get(u)
    if q and PERF.search(q['title']): return 'performance'
    if not q: return 'nometa'
    if q['short']<480: return f"lowres{q['short']}"
    t=q['title']
    for k in [song]+re.findall(r'《([^》]+)》',t): t=t.replace(k,'') if k else t
    m=PROP.search(t)
    if m: return 'prop:'+m.group(0)
    if PERC.search(t) and '身體打擊' not in q['title'] and 'Body Percussion' not in q['title']: return 'percussion'
    return None
json.dump(Q,open('Q.json','w'),ensure_ascii=False)
