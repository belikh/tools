import re,sys
frames=[];cur=None
for line in open(sys.argv[1]):
    line=re.sub(r"\x1b\[[0-9;]*m","",line)
    m=re.match(r"\[(\d\d:\d\d:\d\d)\.\d+\]",line)
    if "Received Raw:" in line:
        cur=[m.group(1) if m else "?",[]]; frames.append(cur); body=line.split("Received Raw:")[1]
    elif "remote.raw" in line and cur: body=line.split("]:",2)[-1] if False else line.split("remote.raw:",1)[1].split("]:",1)[-1] if "]:" in line else ""
    else: continue
    cur[1]+=[int(x) for x in re.findall(r"-?\d+",body)]
rev=lambda x:int(format(x,"08b")[::-1],2)
prev=None;n=0
for t,v in frames:
    if len(v)<97: continue
    b="".join("1" if abs(v[j+1])>1000 else "0" for j in range(1,len(v)-1,2))
    by=[rev(int(b[k:k+8],2)) for k in range(0,len(b)-7,8)]
    if by!=prev:
        print(t,len(b),"LSB"," ".join("%02X"%x for x in by)); prev=by; n+=1
print("frames",len(frames),"distinct changes",n)
