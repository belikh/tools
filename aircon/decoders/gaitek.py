import sys,subprocess
exec(open("both.py").read().split('if __name__')[0])
def bits_of(v,bt=104.17):
    out=[]
    for x in v:
        n=round(abs(x)/bt); out+=[0 if x>0 else 1]*max(1,n)
    return out+[1]*20
def uart(bits):
    i=0;res=[]
    while i<len(bits)-9:
        if bits[i]==0:
            res.append(sum(b<<k for k,b in enumerate(bits[i+1:i+9]))); i+=10
        else: i+=1
    return res
def show(fn):
    prev=None
    for t,v in load(fn):
        b=uart(bits_of(v))
        if b[:6]==[0x47,0x41,0x49,0x54,0x45,0x4B] and len(b)>=24:
            f=b[:24]
            if f!=prev:
                x1=f[7]^f[9]^f[11]^f[13]^f[15]; x2=f[8]^f[10]^f[12]^f[14]^f[6]
                ok=(x1==f[16] and x2==f[17])
                print(t," ".join("%02X"%x for x in f[6:18]),"| power",f[7]&1,"mode",f[9]&15,"fan",(f[9]>>4)&3,"cur",f[10],"set",f[11],"b12",f[12],"b13",f[13],"timer",f[14],"chk","OK" if ok else "BAD")
                prev=f
        elif b: print(t,"other:"," ".join("%02X"%x for x in b[:30]))
show(sys.argv[1])
