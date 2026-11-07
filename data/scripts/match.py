import json,re
Y=json.load(open('years_known.json'))
for k,v in json.load(open('years_agent.json')).items():
    if v.get('conf') in('high','mid') and v.get('y'): Y[k]=v['y']
for k,v in json.load(open('add_years.json')).items(): Y[k]=v[0]
JP={k for k in Y if re.search(r'[぀-ヿ]',k)}|{'櫻桃小丸子','戀愛中的幸運餅乾','あめふり'}
F0=json.load(open('final.json'))
JP|={re.sub(r'（.*?）|\(.*?\)','',o['t']).strip() for o in F0 if o['r']=='日本'}|{'東京音頭','北酒場','炭坑節','花笠音頭','ソーラン節','津軽海峡・冬景色'}
JP|={k for k,v in json.load(open('add_years.json')).items() if v[2]=='日本'}
for k in list(Y):
    if k in JP: Y.pop(k)
Y.pop('冬天裡的一把火＋熱情的沙漠',None)
EXTRA=json.load(open('extra_years.json')) if __import__('os').path.exists('extra_years.json') else {}
Y.update({k:v[0] for k,v in EXTRA.items()})
json.dump(Y,open('Y_all.json','w'),ensure_ascii=False)
def n(s): return re.sub(r'[\s\W_]+','',s.lower().replace('拚','拼').replace('癡','痴').replace('臺','台').replace('洒','灑'))
keys=sorted(Y,key=lambda k:-len(n(k)))
EX=re.compile(r'律動|操|舞|運動|有氧|帶動|椅子|據點|樂齡|健康|銀髮|長者|長輩|暖身|伸展|zumba|dance|fitness|文健站|日照|長照|音樂療育|音樂輔療|節奏|體適能|workout|aerobic|彈力|毛巾|手指|手語',re.I)
BAD=re.compile(r'舞會|舞孃|真心之夜|鍵盤|表揚|AMARTE|烏克麗麗|陶笛|吹奏|彈唱|合奏|演奏|薩克斯|口琴|鋼琴|吉他|二胡|直播|講座|比賽|決賽|初賽|複賽|競賽|成果|發表會|表演|婚禮|演出|晚會|尾牙|運動會|幼兒|兒童|小朋友|國小|幼稚園|親子|教學分解|分解動作|卡拉|KTV|伴唱|MV|合輯|串燒|組曲|聯唱|日翻中|學日語|英語學唱',re.I)
files=json.load(open('ch_files.json')); files['長照2.0銀髮族健康促進']='ch_tw.tsv'; files['健康2.0【挖健康】Max老師']='ch_max.tsv'
M={}
for ch,f in files.items():
    for l in open(f):
        p=l.rstrip('\n').split('\t')
        if len(p)<3: continue
        u,t,d=p
        try:d=float(d)
        except:continue
        if not(90<=d<=480) or BAD.search(t) or not EX.search(t): continue
        nt=n(t)
        for k in keys:
            nk=n(k)
            if len(nk)<2 or nk not in nt: continue
            if len(nk)<=3:
                pat=r'(^|[\s\d《「〔【\[（(｜|~＃#@\-—:：“"\'.、])'+re.escape(k)+r'($|[\s》」〕】\]）)｜|~＃#\-—:：”"\'.、!！（(]|\d)'
                if not re.search(pat,t,re.I): continue
            if True:
                M.setdefault(k,[]).append(dict(u=u,t=t,d=int(d),ch=ch)); break
json.dump(M,open('M.json','w'),ensure_ascii=False)
from collections import Counter
cc=Counter(); 
for k,v in M.items():
    for x in v: cc[x['ch']]+=1
print(len(M),'songs matched'); print(cc.most_common())
print('songs without non-TW videos:',[k for k,v in M.items() if all(x['ch'] in('長照2.0銀髮族健康促進',) for x in v)][:80])
