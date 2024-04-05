import streamlit as st

cus = """

<style>

#root > div:nth-child(1) > div.withScreencast > div > div > header{
    visibility:hidden;
    }

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-1b9x38r.eczjsme2 > button{
    visibility:hidden;
}
    
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3{
    background:#0e2e16;
}

.title{
    color:#71e388;
    display:flex;
    justify-content:center;
    font-size: 2.5em;
}

.subtitle{
    color:#71e388;
    display:flex;
    justify-content:center;
    font-size: 1.5em;
}

.footer{
    position: fixed;
    bottom: 0em;
    right: 12em;
    color:#71e388;
    font-size: 1.0em;
}

</style>

<span class="title">subCELlular LOcalization predictor</span>
<span class="subtitle">Results Sorter</span>
<span class="footer">By Muhammad Sohaib Hassan (SBB PU Lhr)</span>

"""

st.markdown(cus,unsafe_allow_html=True)

st.sidebar.write("""
            ### Upload FASTA file
""")

st.sidebar.warning("Save your **.FASTA file** as **.txt** file to upload")
fasta = st.sidebar.file_uploader("Upload FASTA (.txt format) ", type=["txt"])
if fasta is not None:
    st.success("FASTA file uploaded")
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

    st.sidebar.write("""
            ### Upload CELLO Result file
    """)

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
    
    cello = st.sidebar.file_uploader("Upload CELLO", type=["txt"])
    if cello is not None:
        st.success("CELLO Result file uploaded ")
        clines = cello.readlines()
        clines_temp = []
        for line in clines:
            line = line.strip().decode('ascii')
            clines_temp.append(line)
        clines = clines_temp

        cats_pos = ["Extracellular","Cytoplasmic","Membrane","CellWall"]
        cats_neg = ["Extracellular","Cytoplasmic","Periplasmic","OuterMembrane","InnerMembrane"]

        isBactGramPositive = False
        for line in clines:
            if "CellWall" in line:
                isBactGramPositive = True
                break
                
        if isBactGramPositive:
            st.success("Bacterial Specie detected to be Gram Positive")
            cats = cats_pos
            gap = 18
        else:
            st.success("Bacterial Specie detected to be Gram Negative")
            cats = cats_neg
            gap = 19
    
        included_cats = st.multiselect('Drop all the Protein Catagories You don\'t want to include in output FASTA file',cats,cats)
        
        cats_info_labels = []
    
        if st.button("Generate FASTA file for seelcted catagories"):
    
            st.write("Crawling to sort proteins into catagories w.r.t their predicted Sub Cellular Location ...")
            
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
                cat_info_label = str(cat)+" : "+str(count)+" proteins ("+str(round(count/totalProteins*100,3))+" %)"
                cats_info_labels.append(cat_info_label)

            st.success("FASTA file generated Successfully")
    
            st.write("""
            ### Catagories Breakdown
            """)
            
            for cat_info_label in cats_info_labels:
                st.text(cat_info_label)
    
            label = "proteins"
            for cat in included_cats:
                label+="_"+cat
                

            st.write("""
            ### Download output FASTA
            """)
                     
            st.download_button(label=label+".fasta",data=output_fasta,file_name=label+".fasta")
