import json,re,os,subprocess,concurrent.futures as cf
P=json.load(open('picked2.json')); Y=json.load(open('Y_all.json')); SG=json.load(open('singers.json'))
for k,v in json.load(open('years_agent.json')).items():
    if v.get('conf') in('high','mid') and v.get('who') and k not in SG: SG[k]=v['who']
for f in('add_years.json','extra_years.json'):
    for k,v in json.load(open(f)).items():
        if v[1] and k not in SG: SG[k]=v[1]
prev={o['u'] for o in json.load(open('final.json'))}
TW='長照2.0銀髮族健康促進'
CHN={'🌹Anny Chi🌹':'Anny Chi 紀念恩（樂活音樂趣）','asy8088':'員山公園健康操（asy8088）','瘋狂麥克斯Wow_Max':'健康2.0【挖健康】Max老師','apple Lin (林秀霞老師)':'林秀霞老師','陳采婕-起子':'起子老師（陳采婕）','Yana亞娜':'Yana 亞娜'}
FOREIGN_CJK={'江南style'}
def tags(T,p):
    g=[p]
    g.append('有道具' if re.search(r'彈力|啞鈴|毛巾|絲巾|斗笠|扇|棍|球|鈴|彩帶|彩棒|鼓|杯子|傘|dumbbell|band|ball',T,re.I) else '無道具')
    if re.search(r'伸展|拉筋|舒緩|yoga|stretch',T,re.I): g.append('伸展')
    if re.search(r'肌力|肌耐力|彈力帶|啞鈴|dumbbell|核心|腹肌|深蹲|瘦手臂|大腿',T,re.I): g.append('肌力')
    if re.search(r'帶動跳|廣場舞|帶動唱|排舞',T): g.append('帶動跳')
    if re.search(r'椅子舞|椅子操|椅子運動|坐姿|chair',T,re.I): g.append('椅子舞')
    if re.search(r'腦|認知|記憶|手語|手眼|協調|打擊|節奏|percussion',T,re.I): g.append('動腦')
    g.append('有氧'); return g
out=[]
for p in P:
    s=p['song']
    if p['old'] and p['g']: g=p['g']; t=p['title']
    else: g=tags(p['yt'],p['p']); t=s
    foreign=(not re.search(r'[\u4e00-\u9fff]',s)) or s in FOREIGN_CJK or p['r']=='歐美'
    y=Y.get(s); y=-1 if y is None else y
    d=dict(t=t,r='外語' if foreign else '華台語',c=CHN.get(p['ch'],p['ch']),g=g,u=p['u'],y=y)
    if s in SG and SG[s] and SG[s] not in t: d['s']=SG[s]
    if p['u'] not in prev: d['n']=1
    out.append(d)
def ok(d):
    o=subprocess.run(['curl','-s','-m','15','https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='+d['u']],capture_output=True,text=True).stdout
    return o.startswith('{')
with cf.ThreadPoolExecutor(16) as ex: good=list(ex.map(ok,out))
bad=[d['t'] for d,k in zip(out,good) if not k]; out=[d for d,k in zip(out,good) if k]
print('unplayable dropped:',bad)
json.dump(out,open('final2.json','w'),ensure_ascii=False,indent=0)
def js(d):
    c='TW' if d['c']==TW else ('MAX' if d['c']=="健康2.0【挖健康】Max老師" else json.dumps(d['c'],ensure_ascii=False))
    s=f"{{t:{json.dumps(d['t'],ensure_ascii=False)},r:\"{d['r']}\",c:{c},g:{json.dumps(d['g'],ensure_ascii=False)},u:\"{d['u']}\",y:{d['y']}"
    if 's' in d: s+=f",s:{json.dumps(d['s'],ensure_ascii=False)}"
    if 'n' in d: s+=",n:1"
    return s+"}"
data="[\n"+",\n".join(js(d) for d in out)+"\n]"
h=open('template.html').read().replace('__DATA__',data).replace('__TOTAL__',str(len(out)))
open(os.path.expanduser('~/Claude/教案/oldsongdance/index.html'),'w').write(h)
from collections import Counter
print(len(out),'TW',sum(d['c']==TW for d in out)/len(out))
print(Counter(d['r'] for d in out),Counter(d['g'][0] for d in out),Counter(('unk' if d['y']<0 else 'folk' if d['y']<1930 else d['y']//10*10) for d in out),'new',sum('n' in d for d in out))
