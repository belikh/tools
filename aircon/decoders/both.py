import re,sys
def load(fn):
    out=[];cur=None
    for line in open(fn):
        m=re.match(r"\[(\d\d:\d\d:\d\d)",line)
        if "Received Raw:" in line:
            cur=[m.group(1) if m else "?",[]]; out.append(cur); body=line.split("Received Raw:")[1]
        elif "remote.raw" in line and cur is not None: body=line.split("]:",1)[1]
        else: continue
        cur[1]+=[int(x) for x in re.findall(r"-?\d+",body)]
    return out
rev=lambda x:int(format(x,"08b")[::-1],2)
def dec(v):
    b="".join("1" if abs(v[j+1])>1000 else "0" for j in range(1,len(v)-1,2))
    return " ".join("%02X"%rev(int(b[k:k+8],2)) for k in range(0,len(b)-7,8))
def distinct(fn):
    res={97:[],129:[]};prev={97:None,129:None}
    for t,v in load(fn):
        if len(v) in res:
            d=dec(v)
            if d!=prev[len(v)]: res[len(v)].append((t,d)); prev[len(v)]=d
    return res
if __name__=="__main__":
    for fn in sys.argv[1:]:
        r=distinct(fn); print("==",fn)
        for n,name in ((97,"RESE 48b"),(129,"SEND 64b")):
            print(name)
            for t,d in r[n]: print("  ",t,d)
