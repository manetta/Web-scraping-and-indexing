
import urllib2
import re
import urlparse
import socket
import httplib
import tokens

# kathe fora pou xrhsimopoioume thn urlopen, xrhsimopoioume handlers na diaxeiristoun to aithma mas
# o default opener exei handlers gia oles tis standard katastaseis, auto pou exoume na kanoume einai na
#dhmiourghsoume enan opener o opoios exei enan handler pou tha diaxeiristei to basic authentication
auth_handler=urllib2.HTTPBasicAuthHandler()

class MyException(Exception):
    pass

# h lista tocrawl periexei arxika tis 5 selides pou exei sth diathesi tou o crawler gia na arxisei na katevazei kai sth sunexeia oles tis pros prospelasi selides
tocrawl=['http://www.wired.com','http://www.uefa.com','http://www.cnn.com','http://www.latimes.com','http://www.nytimes.com']

# h lista crawled periexei mono tis selides gia tis opoies katevasame to periexomeno tous dhladh ikanopoihsan olous tous periorismous tou crawler
crawled=[]

# h lista notcrawled periexei mono tis selides gia tis opoies DEN katevasame to periexomeno tous afou DEN ikanopoihsan olous tous periorismous tou crawler
notcrawled=[]

nxt=[]

# to leksiko inp sto telos tha exei toses theseis oses kai oi selides pou tha katevasoume to periexomeno tous dld 1000
# se kathe thesi tou einai apothikeumena: id istoselidas, to periexomeno ths
inp={}

sum=0
pl_ch=0
idi=0
ch3=False
ch4=False
ch5=False
timeout=2
error=0
err=0
pattern='/[a-zA-Z]+$'
dl=0

# re.compile() Compile ena regular expression pattern se ena regular expression object,
#to opoio mporei na xrhsimopoihthei gia matching xrhsimopoiontas tis match() kai search() methodous
# sth sugkekrimenh periptosh xrhsimopoieite gia na anagnorizei ta links
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')



# to while tha ekteleite oso h lista tocrawl pou periexei tis pros prospelasi selides den einai adeia
# kai den exoume ftasei akoma tis 1000 selides pou einai o stoxos mas
while ((len(tocrawl)!=0)and(sum<1000)):
    
    # apothikeoume sth metavlith url to proto stoixeio ths listas tocrawl
    url=tocrawl.pop(0)
    
    # elenxoume an h pros prospelash selida pou einai apothikeumenh sth metavlith url exei hdh prospelastei
    ch1=crawled.count(url)
    ch2=notcrawled.count(url)

    # an h selida den exei prospelastei pote ksana sto parelthon, dld den vriskete oute sti lista crawled
    # me tis selides tis opoies prospelasame kai katevasame to periexomeno tous alla oute kai sthn lista not crawled
    # me tis selides tis opoies exoume prospelasei alla gia diaforous logous den mporesame na katevasoume to periexomeno tous
    # px. th plhthos ton xarakthron ths selidas htan <40.000 tote:
    if ((ch1==0)and(ch2==0)):

        # dhmiourgoume mia aithsh (Request object) me to ti theloume na katevasoume
        req=urllib2.Request(url)
        # dhmiourgoume enan URL opener
        opener=urllib2.build_opener(auth_handler)

        # dokimazoume na katevasoume thn plhroforia pou theloume xeirizontas katallhla kai tis eidikes periptoseis
        # kata thn aithsh anoigmatos ths selidas kanoume xrhsh tou timeoute=2 dld o crawler tha kanei timeout se 2 deuterolepta an to server den antapokrinete

        try:
            f=opener.open(req,timeout=2)
        except (urllib2.URLError,httplib.InvalidURL, NameError, urllib2.HTTPError, ValueError): 
            error=1
            print 'Error'
            continue
        
        # an error=0 dld den egine kapoia sfalma tote:    
        if(error==0):
            
            # dokimazoume na diavasoume to periexomeno ths istoselidas, diaxeirizomaste tis selides san arxeia me tis sunarthseis open(), read(), close()
            try:
                rd=f.read()
            except socket.error:
                err=1
                print 'Error----'
            
            # an den exei ginei kapoio lathos tote:
            if(err==0):

                # vriskoume to megethos ths selidas
                ln=len(rd)
                
                # an to megethos ths selidas einai pano apo 40.000 xarakthres tote mas kanei
                if(ln>40000):

                    # auxanoume kata ena ton arithmo ton prospelasimon selidon oi opoies mas kanoun
                    sum=sum+1
                    
                    # apothikeoume sthn metavliti pl_ch to plhthos xarakthros thw trexousas selidas, to pl_ch tha mas bohthisei gia ton upologosmo tou meso megethous se xarakthres ths sulloghs mas
                    pl_ch=pl_ch+ln
                    
                    print sum

                    # xrhsimopoiontas regular expressions emfanizoume ton titlo ths selidas
                    startPos = rd.find('<title>')
                    if startPos != -1:
                        endPos = rd.find('</title>', startPos+7)
                        if endPos != -1:
                            title = rd[startPos+7:endPos]
                            print '\n' + title + '\n'
                
                    # apothikeoume se mia thesi tou leksikou inp to id kai to periexomeno ths selidas
                    # na tonisoume oti oi theseis tou leksikou stis opoies apothikeuonte oi selides tairiazoun me to id tous
                    inp[idi]=[rd]

                    # auksanoume kata 1 to id pou xrhsimopoioume gia na deixnoume monadika mia selida
                    idi=idi+1
                      
                    # dimiourgoume thn lista links h opoia periexei ta links pou entopizontai sto periexomeno ths selidas
                    links = linkregex.findall(rd)

                    print '--------------------' 
                    
                    # xrhsimopoiontas thn methodo urlparse.urlparse() diatrexoume to URL
                    parsed_url=urlparse.urlparse(url)

                    # gia kathe stoixeio ths listas links xrhsimopoiontas regular expressions elenxoume tous periorimous pou exoume thesei ston crawler
                    for i in (links.pop() for _ in xrange(len(links))):
                        if(re.search('.wiki',i)==None and re.search('.#',i)==None):
                            if(re.search(pattern,i)!=None):
                                i='http://' + parsed_url[1] + i
                                ch3=True
                            elif (i.startswith('/') and (i.endswith('.com/')  or i.endswith('.com') or i.endswith('/') or i.endswith('.html/') or i.endswith('.html') or i.endswith('.htm/') or i.endswith('.htm'))):
                                i='http://' + parsed_url[1] + i
                                ch4=True
                            elif (i.startswith('http') and (i.endswith('.com/') or i.endswith('.com')or i.endswith('/') or i.endswith('.html/') or i.endswith('.html') or i.endswith('.htm/') or i.endswith('.htm'))):
                                ch5=True
                            if ((ch3==True) or (ch4==True) or (ch5==True)):
                                if i not in crawled:
                                    if i not in notcrawled:
                                        ch3=False
                                        ch4=False
                                        ch5=False
                                        # an to URL ikanopoiei olous tous periorimous tote eisagete sthn lista tocrawl me tis upo prospelasi selides
                                        tocrawl.append(i)       
                    # eisagoume sthn lista crawled th selida ths opoia apothikeusame to periexomeno afou htan pano apo 40.000 xarakthres
                    crawled.append(url)
                
                # an to megethos ths selidas DEN einai pano apo 40.000 xarakthres tote mas DEN kanei kai apothikeuoume auth th selida sth lista notcrawled
                else:
                    notcrawled.append(url)
            err=0
        error=0

    # h upo eksetash selida exei prospelastei ksana sto parelthon, afou vriskete sth lista crawled 'h sth lista notcrawled 'h kai stis 2 opote den mporoume na thn ksanaxrhsimopoihsoume
    else: 
        print '\nHdi prospelasmeno url \n'


# upologizoume kai ektuponoume to meso megethos se xaraktires tis sullogis ton selidon
mmch=pl_ch/1000
print 'Meso megethos se xaraktires: '
print mmch
       


# dimiourgoume to arxeio url.txt pou periexei mia lista me ta urls pou apoteloun ths sullogh mas
file=open('C:\\project\\url.txt','w')
while(dl<len(crawled)):
    st=crawled[dl]
    file.write(st)
    file.write('\n')
    dl=dl+1
file.close()


# gia toses fores oso kai to mhkos tou leksikou inp dhaldh gia 1000 fores kaloume thn suanrthsh tokenization
# h opoia ulopoiei ta uposuthmata ths Proepeksergasias, ths Morfosunaktikhs analushs kathos kai ths dhmiourgias tou eurethriou
# h sunarthsh tokenization pairnei os pamametro kathe fora to id ths selidas kai to periexomeno ths
for i in range(len(inp)):
    tokens.tokenization(i,inp[i])


