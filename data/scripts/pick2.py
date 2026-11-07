import json,re,random
from collections import Counter,defaultdict
Y=json.load(open('Y_all.json')); M=json.load(open('M.json')); F=json.load(open('final.json'))
TW='長照2.0銀髮族健康促進'; MAX='健康2.0【挖健康】Max老師'
TWCH=set(json.load(open('ch_files.json')))|{TW,MAX,'悠活健康促進','葉嘉淇'}
def grp(ch): return MAX if ch in(MAX,'瘋狂麥克斯Wow_Max') else ch
def n(s): return re.sub(r'[\s\W_]+','',s.lower().replace('拚','拼').replace('癡','痴').replace('臺','台').replace('洒','灑').replace('田僑仔','田橋仔').replace('梢','稍').replace('按靚','安靚').replace('一朵花','一蕊花').replace('丟丟銅仔','丟丟銅'))
def base(t): return re.sub(r'（.*?）|\(.*?\)','',t).strip()
def posture(t,ch):
    if re.search(r'坐|椅|chair|seated',t,re.I): return '坐姿'
    if re.search(r'站|廣場舞|帶動跳|排舞|舞蹈|健身操|尊巴|zumba|有氧舞',t,re.I): return '站姿'
    if ch in('林維茜 Vicky Lin','澄心悅藝','冰冰老師Candy'): return '坐姿'
    return '站姿'
pool=defaultdict(list)  # song -> candidates
# existing entries (drop Japan, drop foreign-filmed)
for o in F:
    if o['r']=='日本' or o['c'] not in TWCH: continue
    b=base(o['t']).replace('拚','拼')
    pool[b].append(dict(u=o['u'],title=o['t'],ch=o['c'],p=o['g'][0],g=o['g'],old=o['src']=='old',r=o['r'],yt=o.get('yt',o['t'])))
for k,v in M.items():
    for x in v:
        pool[k].append(dict(u=x['u'],title=k,ch=x['ch'],p=posture(x['t'],x['ch']),g=None,old=False,r='歐美' if re.fullmatch(r'[A-Za-z0-9 .,\'!-]+',k) else '台灣',yt=x['t']))
# dedupe ids
for k in pool:
    seen=set(); pool[k]=[c for c in pool[k] if not(c['u'] in seen or seen.add(c['u']))]
from qfilter import check
for k in pool: pool[k]=[c for c in pool[k] if check(c['u'],k) is None]
songs=sorted(k for k in pool if pool[k])
TARGET=int(__import__("sys").argv[1]) if len(__import__("sys").argv)>1 else 400
CAP={TW:0.24,MAX:0.15}; OTHER=0.10
picked=[]; cnt=Counter()
def cap_ok(ch,total):
    g=grp(ch); lim=CAP.get(g,OTHER)*TARGET
    return cnt[g]+1<=lim
known=[s for s in songs if s in Y]; unknown=[s for s in songs if s not in Y]
def run(slist,rounds):
    for rnd in rounds:
        for s in slist:
            if len(picked)>=TARGET: return
            have=[p for p in picked if p['song']==s]
            if rnd==0 and have: continue
            if rnd>0 and len(have)!=1: continue
            cands=pool[s]
            if rnd==1: cands=[c for c in cands if c['p']!=have[0]['p']]
            cands=[c for c in cands if not have or (c['u']!=have[0]['u'] and grp(c['ch'])!=grp(have[0]['ch']))]
            cands=sorted(cands,key=lambda c:(grp(c['ch'])==TW, cnt[grp(c['ch'])], not c['old']))
            for c in cands:
                if cap_ok(c['ch'],TARGET):
                    picked.append(dict(c,song=s)); cnt[grp(c['ch'])]+=1; break
run(known,[0,1,2])
unknown.sort(key=lambda s:-len(pool[s]))
run(unknown,[0])
print(len(picked),'picked;',len(songs),'songs')
print(cnt.most_common())
print('TW share',cnt[TW]/len(picked))
json.dump(picked,open('picked2.json','w'),ensure_ascii=False)
print('unk-year songs:',sum(1 for p in picked if p['song'] not in Y))
