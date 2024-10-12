seq = input("enter your seq:").lower()
lenrrs=int(input("length of restriction seq at 3':"))
fprimers=[]
rprimers=[]
pprimers=[]
foundppairs=0
maxplen=30
plen=25
def gc(seq):
    g=seq.count("g")
    c=seq.count("c")
    return (g+c)/len(seq)*100
def mt(seq):
    g=seq.count("g")
    c=seq.count("c")
    return (64.9+41*(g+c-16.4)/len(seq))
def rcomp(seq):
    seq=seq[::-1]
    cseq=""
    for b in seq:
        if b=="g":
            cseq+="c"
        elif b=="c":
            cseq+="g"
        elif b=="a":
            cseq+="t"
        else:
            cseq+="a"
    return cseq
while foundppairs==0 and plen<=maxplen:
    i=18
    while i<plen:
        if seq[i-1]=="g" or seq[i-1]=="c":
            tempseq=seq[:i]
            fprimers.append(tempseq)
        i+=1
    i=18
    while i<plen:
        if seq[-i]=="g" or seq[-i]=="c":
            tempseq=seq[-i:]
            tempseq=rcomp(tempseq)
            rprimers.append(tempseq)
        i+=1
    for fp in fprimers:
        for rp in rprimers:
            fpgc=gc(fp)
            rpgc=gc(rp)
            if (fpgc>=40 and fpgc<=60) and (rpgc>=40 and rpgc<=60):
                fpmt=mt(fp)
                rpmt=mt(rp)
                if (fpmt>=50 and fpmt<=60) and (rpmt>=50 and rpmt<=60):
                    delta=float(abs(fpmt-rpmt))
                    if delta<=1:
                        rp=seq[-lenrrs:]+rp[lenrrs:]
                        primersstr=f"{fp}:{round(fpgc,3)}:{round(fpmt,3)}:{len(fp)}:{rp}:{round(rpgc,3)}:{round(rpmt,3)}:{len(rp)}:{round(delta,3)}"
                        pprimers.append(primersstr)
    foundppairs=len(pprimers)
    plen+=1
sorted_primers = sorted(pprimers, key=lambda x: float(x.split(':')[-1]))
for p in sorted_primers:
    pf=p.split(":")
    print(f"forward primer:{pf[0].upper()}:{pf[1]}:{pf[2]}:{pf[3]}")
    print(f"reverse primer:{pf[4].upper()}:{pf[5]}:{pf[6]}:{pf[7]}")
    print(f"delta:{pf[-1]}")
    print("------------")