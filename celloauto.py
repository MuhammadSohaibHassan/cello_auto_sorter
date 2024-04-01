import streamlit as st

cus = """
<style>

#root > div:nth-child(1) > div.withScreencast > div > div > header{
    visibility:hidden;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section{
    background:black;
    }

#cello-result-sorter > div > span{
    padding:20px;
    background:black;
    color:darkslategray;
    border-radius:20px;
    }

#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi5 > div > div > div > div:nth-child(7) > div{
    border:3px solid black;
    padding: 10px;
    border-radius:20px;
    }

</style>
"""
st.markdown(cus,unsafe_allow_html=True)
st.title("CELLO Result Sorter")
fasta = st.file_uploader("Upload fasta", type=["txt"])
if fasta is not None:
    st.write("fasta uploaded!!")
    flines = fasta.readlines()
    flines_temp = []
    for line in flines:
        line = line.strip().decode('ascii')
        flines_temp.append(line)
    flines = flines_temp

    cello = st.file_uploader("Upload cello", type=["txt"])
    if cello is not None:
        st.write("cello uploaded!!")
        clines = cello.readlines()
        clines_temp = []
        for line in clines:
            line = line.strip().decode('ascii')
            clines_temp.append(line)
        clines = clines_temp

        bact_type = st.radio(
        "Bacteria Type",
        ["Gram Positive", "Gram Negative"]
        )

        if st.button("Crawl for Sub Cellular Locations"):

            i = 0
            for line in flines:
                if ">" in line:
                    i+=1
            totalProteins = i

            cats_seqs = []
            cats_info_labels = []

            ("\n")
            ("Search Results...")
            ("\n")

            cats_pos = ["Extracellular","Cytoplasmic","Membrane","CellWall"]
            cats_neg = ["Cytoplasmic","Periplasmic","OuterMembrane","Extracellular","InnerMembrane"]

            if bact_type == "Gram Positive":
                cats = cats_pos
                gap = 18

            else:
                cats = cats_neg
                gap = 19

            for i in range(len(cats)):
                cat = cats[i]
                fileo = ""

                j=(len(clines)-12)//gap
                count=0
                for i in range(0,j+1):
                    if cat in clines[(12+(gap*i))-1]:
                        count+=1
                        seqid=">"+clines[(gap*i)][7:]
                        idx=flines.index(seqid)
                        idx+=1
                        seq=""
                        while ">" not in flines[idx]:
                            seq+=flines[idx].strip()
                            if idx<len(flines)-1:
                                idx+=1
                            else:
                                break
                        fileo+=seqid
                        for i in range(0,len(seq),60):
                            seqline = seq[i:i+60]+"\n"
                            fileo+=seqline
                        fileo+="\n"
                
                cats_seqs.append(fileo)
                cat_info_label = str(cat)+" --> "+str(count)+" proteins ("+str(round(count/totalProteins*100,3))+" %)"

                cats_info_labels.append(cat_info_label)

            i=0
            for cat_seq in cats_seqs:
                with st.expander(str(cats_info_labels[i]), expanded=False):
                    i+=1
                    st.code(cat_seq)