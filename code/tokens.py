#sto arxeio ayto ylopoioyme tin proepexergasia,ti morfosyntaktiki analysi,tin anaparastasi istoselidwn
#se dianysmatiko xwro, tin dimioyrgia kai tin apothikeusi euretirioy

import nltk
import os
import subprocess
import shlex
import math
import time
import xml.etree.ElementTree as ET


#ath_lemma->lsita pou periexei to athroisma twn limmatwn kathe keimenoy
ath_lemma=[]
#pl_lemma->lista gia tin apothikeusi lexikou tou kathe keimenoy me tin syxnotita emfanisis tou kathe
#limmatos
pl_lemma=[]
#lmskk->lista pou periexei to mikos twn xaraktirwn tou katharou keimenou kathe istoselidas
lmskk=[]
xron_kat_evr=0


#i synartisi ayti kaleitai efoson exei sygkentrwthei to epithymito plithos istoselidwn apo kathe keimeno
#xexwrista
def tokenization(i,*a):

    global xron_kat_evr

    #path gia tin apothikeusi twn arxeiwn tou katharou keimenou(path1), tou keimenou pou prokyptei apo
    #morfosyntantiki analysi(path2), twn leimatwn tou keimwnoy(path3)
    path1='C:\\project\\token\\'
    path2='C:\\project\\tagged\\'
    path3='C:\\project\\lemma\\'

    #path gia to PoS Tagger
    tagger_path="C:\\TreeTagger\\TreeTagger\\bin\\tree-tagger.exe"
    parameter_file="C:\\TreeTagger\\TreeTagger\\lib\\english.par"

    #Pos tags gia open class category
    occ=['JJ','JJR','JJS','RB','RBR','RBS','NN','NNS','NNP','NNPS','VB','VBD','VBG','VBN','VBP','VBZ','FW']
    #Pos tags gia closed class category
    ccc=['CD','CC','DT','EX','IN','LS','MD','PDT','POS','PRP','PRP$','RP','TO','UH','WDT','WP','WP$','WRB']

    #lista poy pairnoume stin eisodo
    l1=a[0]
    #keimenoy eisodou istoselidas
    str1=l1[0]
    b=[]
    #metritis gia to plithos twn limmatwn
    lemma=0
    mskk=0
    mmch1=0
    #dic->lexiko gia tin apothikeusi tis syxnotitas emfanisis kathe limmatos se kathe keimeno
    dic={}
    inverted_index={}
    #enlis->lista gia apothikeusi limmatwn
    elis=[]
    url_xm=[]
    #metritis gia to mikos xaraktirwn tou katharou keimenoy
    met=0
    ath=0

    ####################################
    ######### erwtima 2 ################
    ####################################
    #exagwgi katharou keimenoy istoselides
    raw=nltk.clean_html(str1)
    #exagwgi tokenixed keimenou istoselidas
    #tokens->lista se akthe thesi tis opoias yparxei ena string apo to katharo keimeno tis istoselidas
    tokens=nltk.word_tokenize(raw)


    #apothikeuoume to katharo keimeno tis kathe istoselidas se arxeio.ta arxeia periexoyn mia mexi an
    #grammi i ena symvolo ana grammi
    #ta arxeia onomazontai namei.txt opou i einai to id toy keimenoy eisodou
    #dimiourgia tou onomatos tou arxeiou
    filename="name%i.txt" %(i)
    #dimiourgeia toy path sto opoio apothikeuetai to arxeio
    nm=os.path.join(path1,filename)
    #anoigoume to arxeio gia egrafi
    fl=open(nm,'w')
    #se kathe grammi tou arxeiou grafoume mia lexi i ena symvolo apo ayta pou exoyn prokypsei meta to
    #tokenized tou keimenou
    for k in range(len(tokens)):
        st=tokens[k]
        fl.write(st)
        #metrame to plithos twn xaraktirwn tou katharou keimenoy
        met=met+len(st)
        fl.write('\n')
    fl.close()

    #gia kathe istoselida apothikeuoume to mikos twn katharwn lexewn tis sti lista lmskk
    lmskk.append(met)

    ####################################
    ######### erwtima 3 ################
    ####################################
    #dimiourgia arxeiwn(ena gia kathe istoselida) sto opoio apothikeoume to apotelesma tis morfosyntaktikis
    #analysis. ta arxeia ayta onomazontai taggei.txt opou i einai to id toy keimenoy eisodou
    taggename="tagge%i.txt" %(i)
    #dimiourgeia toy path sto opoio apothikeuetai to arxeio
    nmm=os.path.join(path2, taggename)

    #morfostaktiki analysi se kathe arxeio namei.txt xrisimopoiwntas to ergaleio Tree Tagger gia ta Windows
    #to apotelesmat tis morfosyntaktikis analysis apothikeuetai sta arxeia taggei.txt
    #sto telos tis morfosyntaktikis analysis kathe keimeno tis syllogis periexei morfosyntaktiki analysi
    #gia kathe lexi i symvolo tou
    f=os.popen(tagger_path + " -token -lemma \"" + parameter_file + "\" \"" + nm + "\">\"" + nmm + "\"",'r')
    f.read()
    f.close()

    #########################################
    # ksekinhma xronou kataskeus evrethriou #
    #########################################
    t0=time.time()

    ####################################
    ######### erwtima 4 ################
    ####################################    
    #diavasma arxeiou taggei.txt
    f1=open(nmm,'r')
    #rd->lista kathe stoixeio tis opoias einai grammi toy arxeioy
    rd=f1.readlines()
    f1.close()

    
    #dimiourgia arxeiwn lemmai.txt opou i einai to id toy keimenoy eisodou. Sta keimena auta apothikeuontai
    #ta lemmata twn lexewn pou exoun simasiologiko periexomeno kaid en anhkoyn stis stop words
    wswname="lemma%i.txt" %(i)
    nm1=os.path.join(path3,wswname)
    #anoigma toy arxeiou lemmai.txt gia eggrafi
    f2=open(nm1,'w')
    #sto arxeio lemmai.txt apothikeuoume ta limmata pou exoyn prokypsei apo ti morfosyntaktiki analysi kai den
    #anikoun stis stop words.Episis sto arxeio lemmai.txt den apothikeuoyme lexeis poy den anikoyn stis stop
    #words wstoso to limma toy einai <unknonw>
    for l in range(len(rd)):
        ls1=rd[l]
        b=ls1.rsplit('\t')
        #elegxos gia lexeis pou den einai stop-words kai den exoyn limma <unknown>
        if((occ.count(b[1])!=0) and (ccc.count(b[1])==0) and (b[2]!='<unknown>\n')):
            f2.write(b[2])
            #metrame tous orous pou apothikeuoyme sto arxeio lemmai.txt
            lemma=lemma+1
    #to plithos limmatwn keimenoy i to apothikeouoyme sti lista ath_lemma stin thesi i
    ath_lemma.append(lemma)
    f2.close()


    #metrisi toy plithoys kathe monadikou limmatos kathe keimenoy
    f3=open(nm1,'r')
    #lista me stoixeia tis grammes toy arxeiou lemma%i.txt
    lm=f3.readlines()
    f3.close()
    #gia kathe ena apo ta limmata poy periexontai sto arxeio lemma%i.txt metrame ti syxnotita emfanisis toy
    for j in range(len(lm)):
        sp=lm[j].rsplit('\n')
        #i lista enlist periexei ta limmata xwris \n
        elis.append(sp[0])
    for t in range(len(elis)):
        lem=elis[t]
        summ=elis.count(lem)
        #apothikeysi toy plithoys twn limatwn kathe keimenoy se ena lexiko
        dic[lem]=summ
    #lista me dictionary me limmata kathe keimenou
    pl_lemma.append(dic)


    #########################################
    # stamathma xronou kataskeus evrethriou #
    #########################################
    t1=time.time()
    xron_kat_evr=xron_kat_evr+(t1-t0)


    
    ####################################
    ######### erwtima 5 ################
    #################################### 
    #dimioyrgia euretiriou
    #o kwdikas ekteleitai otan exoyn dimiourgithei ola ta limmata gia ola ta keimena


    
    #####################################
    #####################################
    #####################################
    
    if(len(ath_lemma)==1000):

        ####################################
        t2=time.time()
        ####################################
        
        #ypologismos mesou megethoys katharou keimenoy
        for p in range(len(lmskk)):
            mmch1=mmch1+lmskk[p]
        #print len(lmskk)
            
        print 'Meso megethos katharou keimenoy: '


        
        #####################################
        #####################################
        ##############################
        print mmch1/1000

        
        
        for n in range(len(pl_lemma)):
            #gia kathe lexiko stin pl_lemma pairnoyme ta kleidia toy stin lista keys
            keys=pl_lemma[n].keys()
            
            for m in range(len(keys)):
                #kathe ena kleidi tis listas keys to kratame stin proswrini metavliti key
                key=keys[m]
                keim=[]
                buckets=[]
                emf=[]
                #elegxoume kata poso kathe keimeno apo ti syllogi mas periexei to sygkekrimeno
                #kleidi(limma)
                for z in range(len(pl_lemma)):
                    if(pl_lemma[z].has_key(key)==True):
                        #an ena keimeno exei to kleidi topothetoume to id toy keimenoy sti lista keim
                        #sto telos i lista keim tha exei ola ta id twn keimenwn poy exoyn to kleidi
                        keim.append(z)
                        temp_dic=pl_lemma[z]
                        #ar_em_or->lista stin opoia apothikeuoume poses fores emfanizetai to kleidi
                        #se kathe keimeno apo ayta poy vrethike
                        ar_em_or=temp_dic[key]
                        #ypologismos kai apothikeusi tou orou Tfij sti lista emf gia kathe keimeno
                        #pou exei to limma
                        pr=float(ar_em_or)/ath_lemma[z]
                        emf.append(float(ar_em_or)/ath_lemma[z])
                        

                #se posa keimena emfanizetai o oros key
                ln=len(keim)
                #ypologismos orou IDF o opoios einai idios gia ola ta keimena
                #######################################
                #######################################
                ######################################
                idf=math.log(1000/ln, 10)

                #dimiourgia listas buckets opou gia kathe limma apothikeuoume to id tou keimenoy sto
                #opoio emfanizetai kai to antistoivo varos toy sto keimeno ayto
                for w in range(ln):
                    buckets.append(keim[w])
                    buckets.append(emf[w]*idf)


                #dimiourgia anestramenou euretiriou     
                #to anestrameno euretirio tha einai ena lexiko tis morfis {'key':[id1,weight1,...]}
                inverted_index[key]=buckets

        #########################
        t3=time.time()
        xron_kat_evr=xron_kat_evr + (t3-t2)
        print 'O xronos kataskeuhs tou evrethriou einai: '
        print xron_kat_evr
        #########################

        ####################################
        ######### erwtima 6 ################
        ####################################              

        #apothikeusi anestramenou euretiriou sto arxeiou .xml
        root=ET.Element("inverted_index")
        #ii_key->lista pou periexei ola ta limmata tou anestramenou euretiriou
        ii_key=inverted_index.keys()
        #gia kathe ena apo ta parapanw limmata afou to eisagoume sti domi tou anestramenou euretiriou
        #sti synexeia eisagoume to id twn keimenwn pou to periexoun kathws kai to antistoixo varos
        #tou limmatos sto keimeno ayto
        for xx in range(len(inverted_index)):
            km=ii_key[xx]
            lemma=ET.SubElement(root,"lemma")
            lemma.set('name',km)
            ids_list=inverted_index[km]
            for pp in range(len(ids_list)):
                if(pp%2==0):
                    ids_weights=ET.SubElement(lemma,"document")
                    ur=ids_list[pp]
                    wg=ids_list[pp+1]
                    #urll=url_xm[ur]
                    #eggrafi id keimenou
                    ids_weights.set("id",str(ur))
                    #eggrafi varos limmatos sto sygkekrimeno keimeno
                    ids_weights.set("weight",str(wg))
        tree=ET.ElementTree(root)
        #eggrafi tou anestramenou euretiriou sto arxeio C:\\project\\page1.xhtml
        tree.write("C:\\project\\page1.xhtml")
