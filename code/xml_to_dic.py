#sto arxeio auto ginetai i epanafortwsi tou anestrammenou
#euretiriou apo to arxeio .xml opou einai apothikeumeno
#sti synexeia kai meta tin fortwsei tou euretiriou
#ylopoieitai o mixanismos ypovolis erwtimatwn

import time
import xml.etree.ElementTree as et 

#epanafortwsi toy anestrammenou euretiriou
tree=et.parse("C:\\project\\page1.xhtml")

#data einai to mia domi dicionary gia tin apothikeusi tou
#anestramenou euretiriou
data={}
#url_xm->lista gia tin fortwsi twn urls apo to arxeio
url_xm=[]


#epanafortwsi toy anestrammenou euretiriou
for a in tree.getroot().getchildren():
    #i metavliti name krata kathe fora to lemma
    name=a.get('name')
    currlist=[]
    #gia kathe lemma pou apothikeuetai sti metavliti name prospelaunoyme to id
    #kai to weight twn documents pou anikoun sto limma auto
    for atype in a.getchildren():
        currlist.append(atype.get('id'))
        currlist.append(float(atype.get('weight')))
    #kataxwrisi tou limmatos sto euretirio
    data[name]= currlist   

#keys->lista pou krata ta kleidia tou euretiriou
keys=data.keys()


#anagnwsi tou arxeiou url.txt sto opoio exoume apothikeusei ta url pou prospelastikan
file2=open('C:\\project\\url.txt','r')
urls=file2.readlines()
file2.close()
#ta urls apothikeuontai telika sti lista url_xm afou arxika apomakrunomy apo
#ayta ton xaraktira allagis grammis
for tt in range(len(urls)):
    turl=urls[tt].rsplit('\n')
    url_xm.append(turl[0])


#mixanismos ypovolis erwtimatwn
while 1 == 1:

    print "Dose thn leksi pou thleis na anazhthseis: "
    #var->lista me tous orous tou erwtimatos pou edwse o xristes kata tin ypovoli tou erwtimatos
    var = raw_input("Search: ")
    print "you entered ", var
    print '\n'
    t0=time.time()
    #search_list->lista se kathe thesi tis opoias periexontai oi oroi tou erwtimatos    
    search_list=var.rsplit(' ')
    
    #temp_dic->topiko lexiko gia tin apothikeusi twn orwn tou erwtimatos
    temp_dic={}
    #gia kathe ena apo tous dosmenous orous apothikeuoyme se morfi lexikou
    #ton oro kai tin lista me ta id tis syllogis kai ta antistoixa vari sto topiko lexiko temp_dic
    #se periptwsi pou den yparxei o oros aytos sti sullogi mas prosthetoyme
    #mia lista pou periexei to stoixeio -1
    for k in range(len(search_list)):
        if(keys.count(search_list[k])!=0):
            #st1->lista me id kai vari tou dosmenou kathe fora orou
            st1=data[search_list[k]]
            temp_dic[search_list[k]]=st1
        else:
            temp_dic[search_list[k]]=[-1]

    #stin periptwsi auti elegxoume an mas exei dothei enas i perissoteroi oroi sto erwtima
    if(len(search_list)==1):
        #elegxoume an o monadikos oros tou erwtimatos yparxei sto ereutirio mas
        if(temp_dic[search_list[0]].count(-1)==0):
            twg=[]
            ttwg=[]
            tid=[]
            #ean yparxei o oros tou erwtimatos ektypwnoyme to url tou keimenou sto opoio
            #vrisketai kai ta antistoixa vari taxinomimena kata auxousa seira varwn
            for k in range(len(temp_dic[search_list[0]])):
                if(k%2==0):
                    tid.append(temp_dic[search_list[0]][k])
                    twg.append(temp_dic[search_list[0]][k+1])

            for k in range(len(twg)):
                ttwg.append(twg[k])
            twg.sort()
            for k in range(len(twg)):
                th=ttwg.index(twg[k])
                intt=int(tid[th])
                url1=url_xm[intt]
                print 'id:' + url1 + '\t\t' + 'weight:' + str(twg[k])                   
                    
        #o oros den yparxei sto euretirio mas           
        else:
            print 'To limma den yparxei'
 
    #exoun dothei perissoteroi tou enos oroi sto erwtima mas   
    else:
        #sun_keim->lista me ids keimenwn pou periexoyn tous orous pou dothikan stin eisodo
        sun_keim=[]
        #gia kathe oro tou erwtimatos vriskoyme ta id tis sullogis sta opoio aytos
        #yparxei kai gia kathe ena apo ayta ta id elegxoume an yparxei kai sti lista twn ids
        #twn ypoloipwn orwn toy erwtimatos
        for i in range(len(search_list)):
            lemma_list=temp_dic[search_list[i]]
            for m in range(len(lemma_list)):
                est=0
                if(m%2==0):
                    tm=lemma_list[m]
                    for l in range(len(search_list)):
                        #kathe fora pou ena id yparxei sti lista twn ids twn ypoloipwn
                        #orwn auxanoume tin metavliti est kata 1
                        if(temp_dic[search_list[l]].count(tm)>0):
                            est=est+1;
                    #mono stin periptwsi poy ena id vrethike se oles tis listes twn ids
                    #olwn twn orwn kai efoson i lista sun_keim den periexei idi
                    #to id auto kataxwroume to id tou keimenoy stin lista sun_keim
                    if((est==len(search_list))and sun_keim.count(tm)==0):        
                        sun_keim.append(tm)

        #i lista sun_keim einai adeia->den exei vrethei keimeno pou na periexei olous tous
        #orous tou erwtimatos               
        if(len(sun_keim)==0):
            print 'To dosmeno limma den yparxei'
        #oi oroi vrethikan se kapoia ids keimwnwn opote ektypwnoyme ta antistoixa urls kai
        #ta vari toys
        else:
            print 'To limma yparxei sta parakatw keimena'
            #wgh->lista pou krata ta vari gia kathe id keimenoy pou vrethike
            wgh=[]
            twgh=[]
            init=0
            #stin periptwsi pou exoume parapanw apo enan orous to varos prokyptei apo to
            #athroisma twn varwn twn epimerous orwn
            for j in range(len(search_list)):
                lm=search_list[j]
                ls_wg=temp_dic[lm]
                #arxika gia kathe ena apo tous orous tou erwtimatos apothikeuoume ta vari tou
                #gia sta keimena pou autos emfanizetai sti lista wgh
                if(init==0):
                    for t in range(len(sun_keim)):
                        th=ls_wg.index(sun_keim[t])
                        wgh.append(ls_wg[th+1])
                        init=1
                #sti synexeia gia kathe ena apo toys ypoloipous orous prosthetoume ta vari tous
                #stin thesi pou arxika topothetisame to varos tou prwtou orou tou erwtimatos
                else:
                    jj=0
                    for f in range(len(sun_keim)):
                        th=ls_wg.index(sun_keim[f])
                        wgh[jj]=wgh[jj]+ls_wg[th+1]
                        jj=jj+1

            #xrisi tis proswrinis listas twgh gia tin apothikeusi twn varwn tis listas wgh
            for j in range(len(wgh)):
                twgh.append(wgh[j])
            #taxinomisi tis listas wgh
            wgh.sort()            
            #emfanisi twn url kai twn antistoixwn varwn poy periexoyn tous orous tou erwtimatos            
            for j in range(len(wgh)):
                thes=twgh.index(wgh[j])
                intt=int(sun_keim[thes])
                url1=url_xm[intt]
                print 'id:' + url1 + '\t\t' + 'weight:' + str(wgh[j])

        #gia kathe ena apo tous orous tou erwtimatos emfanizoyme ta urls sta opoia yparxei kai
        #to varos tou se auto taximonimeno kata auxousa seira varwn
        print '\n'
        print 'Gia kathe ena apo ta dosmena limmata tha einai:'
        for u in range(len(search_list)):
            twg=[]
            ttwg=[]
            tid=[]
            print '\n'
            print 'Gia to lemma ' + search_list[u]
            print '\n'
            if(temp_dic[search_list[u]].count(-1)==0):
                for kk in range(len(temp_dic[search_list[u]])):
                    if(kk%2==0):
                        tid.append(temp_dic[search_list[u]][kk])
                        twg.append(temp_dic[search_list[u]][kk+1])

                for k in range(len(twg)):
                    ttwg.append(twg[k])

                twg.sort()

                for k in range(len(twg)):
                    th=ttwg.index(twg[k])
                    intt=int(tid[th])
                    url1=url_xm[intt]
                    print 'id:' + url1 + '\t\t' + 'weight:' + str(twg[k]) 
            #emfanizetai otan kapoio apo tous orous tou erwtimaos den yparxei sti syllogi
            else:
                print 'To limma den yparxei'

    t1=time.time()
    xronos=t1-t0
    print 'Xronos anazhthshs: ', xronos
    
    #exodos apo to mixanismo ypovolis erwtimatwn            
    print '\n'
    print "if you want to exit, type <exit> ... to continue press <enter>"
    ex = raw_input()
    if ex=="exit":
        break
