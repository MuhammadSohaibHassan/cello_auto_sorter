import streamlit as st

cus = """
<style>

#root > div:nth-child(1) > div.withScreencast > div > div > header{
    visibility:hidden;
    }
    
#root > div:nth-child(1) > div{
    background:green;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3{
    background:#0e2e16;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-1b9x38r.eczjsme2 > button{
    visibility:hidden;
}

.title{
    color:#71e388;
    display:flex;
    justify-content:center;
    font-size: 2.5 em;
}

.subtitle{
    color:#71e388;
    display:flex;
    justify-content:center;
    font-size: 1.5 em;
}

</style>

<span class="title">subCELlular LOcalization predictor</span>
<span class="subtitle">Results Sorter</span>

"""
st.markdown(cus,unsafe_allow_html=True)
st.sidebar.title("CELLO Result Sorter")

st.sidebar.warning("Save your **.FASTA file** as **.txt** file to upload")
fasta = st.sidebar.file_uploader("Upload fasta", type=["txt"])
if fasta is not None:
    st.sidebar.success("FASTA file uploaded")
    flines = fasta.readlines()
    flines_temp = []
    for line in flines:
        line = line.strip().decode('ascii')
        flines_temp.append(line)
    flines = flines_temp

    i = 0
    for line in flines:
        if ">" in line:
            i+=1
    totalProteins = i

    st.success(f"{totalProteins} protein sequences have been imported successfully")

    st.sidebar.warning("""
    ### Important!!!
    * Open your FASTA file in a text editor and copy all the sequence text by pressing **Ctrl+A**
    * Follow the link **[CELLO v.2.5](http://cello.life.nctu.edu.tw/)**
    * Select your Organism type (Gram Positive , Gram Negative)
    * Paste the copied FASTA sequence text in the text field (make sure to delete dummy seq already present there)
    * Hit **Submit**
    * On next page Titling **"CELLO RESULTS"** , Copy all the text displayed by pressing **Ctrl+A**
    * Now creat a .txt file , paste this copied text and save it with name of your choice
    * Now this is the file to upload here
    """)
    
    cello = st.sidebar.file_uploader("Upload cello", type=["txt"])
    if cello is not None:
        st.sidebar.success("CEELO Result file uploaded ")
        clines = cello.readlines()
        clines_temp = []
        for line in clines:
            line = line.strip().decode('ascii')
            clines_temp.append(line)
        clines = clines_temp

if fasta is not None and cello is not None:

    st.sidebar.divider()

    bact_type = st.sidebar.radio(
    "Organism",
    ["Gram Positive", "Gram Negative"]
    )

    st.sidebar.divider()

    cats_pos = ["Extracellular","Cytoplasmic","Membrane","CellWall"]
    cats_neg = ["Cytoplasmic","Periplasmic","OuterMembrane","Extracellular","InnerMembrane"]

    if bact_type == "Gram Positive":
        cats = cats_pos
        gap = 18

    else:
        cats = cats_neg
        gap = 19

    included_cats = st.sidebar.multiselect('Drop all the Protein Cataories You don\'t want to include in output FASTA file',cats,cats)
    
    cats_info_labels = []

    if st.sidebar.button("Generate FASTA file for seelcted catagories"):
        
        output_fasta=""

        for i in range(len(included_cats)):
            fileo=""
            cat = included_cats[i]

            j=(len(clines)-13)//gap
            count=0
            for i in range(0,j+1):
                if cat in clines[(13+(gap*i))-1]:
                    count+=1
                    seqid=">"+clines[(gap*i)+1][7:]
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
            cat_info_label = str(cat)+" : "+str(count)+" ("+str(round(count/totalProteins*100,3))+" %)"
            cats_info_labels.append(cat_info_label)

        st.success("FASTA file generated Successfully")

        ("---")
        
        ("""
        ### Catagories Breakdown
        """)
        
        for cat_info_label in cats_info_labels:
            st.text(cat_info_label)

        label = "proteins"
        for cat in included_cats:
            label+="_"+cat
            
        ("---")

        ("""
        ### Download output FASTA
        """)
                 
        st.download_button(label=label+".fasta",data=output_fasta,file_name=label+".fasta")
