import streamlit as st

cus = """
<style>

#root > div:nth-child(1) > div.withScreencast > div > div > header{
    visibility:hidden;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section{
    background:purple;
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

col1,col2=st.columns(2)
with col1:

    fasta = st.file_uploader("Upload fasta", type=["txt"])
    if fasta is not None:
        st.success("FASTA file uploaded")
        flines = fasta.readlines()
        flines_temp = []
        for line in flines:
            line = line.strip().decode('ascii')
            flines_temp.append(line)
        flines = flines_temp

with col2:
    cello = st.file_uploader("Upload cello", type=["txt"])
    if cello is not None:
        st.success("CEELO Result file uploaded ")
        clines = cello.readlines()
        clines_temp = []
        for line in clines:
            line = line.strip().decode('ascii')
            clines_temp.append(line)
        clines = clines_temp

if fasta is not None and cello is not None:

    i = 0
    for line in flines:
        if ">" in line:
            i+=1
    totalProteins = i

    st.success(f"{totalProteins} protein sequences have been imported successfully")

    st.divider()

    bact_type = st.radio(
    "Organism",
    ["Gram Positive", "Gram Negative"]
    )

    cats_pos = ["Extracellular","Cytoplasmic","Membrane","CellWall"]
    cats_neg = ["Cytoplasmic","Periplasmic","OuterMembrane","Extracellular","InnerMembrane"]

    if bact_type == "Gram Positive":
        cats = cats_pos
        gap = 18

    else:
        cats = cats_neg
        gap = 19

    included_cats = st.multiselect('Drop all the Protein Cataories You don\'t want to include in output',cats,cats)
    
    cats_info_labels = []

    if st.button("Generate output file"):

        ("Crwaling file for selected protein catagories...")

        output_fasta=""

        for i in range(len(included_cats)):
            fileo=""
            cat = included_cats[i]

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
            
            output_fasta+=fileo
            cat_info_label = str(cat)+" --> "+str(count)+" proteins ("+str(round(count/totalProteins*100,3))+" %)"
            cats_info_labels.append(cat_info_label)

        for cat_info_label in cats_info_labels:
            st.success(cat_info_label)
        
        label = "proteins"
        for cat in included_cats:
            label+="_"+cat

        st.download_button(label=label+".fasta",data=output_fasta,file_name=label+".fasta")
