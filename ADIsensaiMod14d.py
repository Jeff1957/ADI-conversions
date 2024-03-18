'beginning of python module: ADI tags defined; this is a library 4 ADI pack & unpack'
#ideas for both programs                                            3/18/2024 JRJ
#   - don't output lower than XX record; higher are newer
#   - end date on QSOs is sometimes left out? but not time_off or length
#   - /.local/share/Trash/files/ deleted files area?
#   - don't process unexpected tags, but save new identifiers somewhere

rtDr = '/mnt/chromeos/MyFiles/TstLinux'                       #for os path
line,lastline,lend,nwLn,sep,selL = '','','\r\n','\n',',',0    #last # flags: best 0,5  good short 3,1  echo 2
import asyncore,cgi,doctest,os,pprint,shelve,socket,sys,time  #subroutines for other 2 pgms
import pyhamtools as hBx #or from pyhamtools import LookupLib, Callinfo; missing locator, frequency, qsl ???
import tkinter as tKw
VSlog = hBx.callinfo.logging                    #shortcuts for testing hBx
cols = [0,3,4,8,9,10,12,13,14,31,33,35,40,41]   #pack sequence -1, see processLn1 more info
bgTags = ['QSO','QSL','IOTA','LoTW','MY','QTH','SIG','STX','SAT','RST','INTL','RX','TX','QRZ','DXCC','eQSL','CITY','CNTY','BAND','SKCC',
'COUNTRY','ARRL','ITU','NR','APP','HAM','EOH','EOR',]         #not used
#increases diversity in Case; allow easy classification by eye & standardization; tag portions!
ltTags = ['qso','qsl','iota','lotw','my','qth','sig','stx','sat','rst','intl','rx','tx','qrz','dxcc','eqsl','city','cnty','band','skcc',
'country','arrl','itu','nr','app','ham','eoh','eor',]

tgStr = [ 'QSO_no','','freq','BAND','mode','TX_pwr','','','time_on','call','RST_sent','RST_rcvd','time_off','QTH','name','cw_key','comment',
'QSL_sent_via','QSL_sent','QSL_rcvd','','LoTW_QSL_sent','freq_RX','BAND_RX','contest_id','srx_string','QRZcom_QSO_upload_status',
'eQSL_QSL_sent','rig','RX_pwr','antenna','MY_tzn','','operator','PFX','COUNTRY','DXCC','gridsquare','SAT_name','SFI','QSO_date','state',
'address','QSO_random','lat','lon','notes','','HAMlog_sent', ]  # put data types here 2?  both sparse lookup lists, esp. the 2nd
tgStrL = [ 'qso_no','','','band','','tx_pwr','','','','','rst_sent','rst_rcvd','','qth','','','',
'qsl_sent_via','qsl_sent','qsl_rcvd','','lotw_qsl_sent','freq_rx','band_rx','','','qrzcom_qso_upload_status','eqsl_qsl_sent',
'','rx_pwr','','my_tzn','','','pfx','country','dxcc','','sat_name','sfi','qso_date','','',
'qso_random','','','','','hamlog_sent', ]                     #change to the standard form, here and in miniMy
myDat = [ 'station_callsign','MY_CNTY','MY_lat','MY_lon','MY_DXCC','MY_gridsquare','MY_cq_zone','MY_ITU_zone','MY_rig','MY_state', ]
myDatL = ['','my_cnty','my_lat','my_lon','my_dxcc','my_gridsquare','my_cq_zone','my_itu_zone','my_rig','my_state',] #below +enumerated to upStr
upStr = ['state','MY_state','cont','call','operator','station_callsign','PFX','QSL_sent','QSL_rcvd','MY_tzn']   #upper case
capSt = ['QTH','name','MY_name','COUNTRY','MY_COUNTRY','rig','MY_rig','mode','gridsquare','QSL_sent_via']   #or title?
tgEcpts = ['QSO_len','qso_date_off','cnty','cont','cqz','email','ituz','app_']  #above 2 for values, NOT tags; app_ needs wildcard *?

doySt= [0,31,59,90,120,151,181,212,243,273,304,334,365]         #no leap year, m-1
dyPm = [31,28,31,30, 31, 30, 31, 31, 30, 31, 30, 31]            #feb changes Ly
Wzns = ['Z','A','B','C','D','E','F','G','H','I','K','L','M']    #hours behind UTC, EST is zone R
Ezns = ['Z','N','O','P','Q','R','S','T','U','V','W','X','Y']    #ISO 8601 zones 15d /long, this one -1*
zneS = {'PST':8,'MST':7,'CST':6,'EST':5,'AST':4,'PDT':7,'MDT':6,'CDT':5,'EDT':4,'ADT':3,'UTC':0,'CUT':0,'Zulu':0,'Winter':5,'Summer':4,'Construction':4} #dictionary form
qc,lYr,selL2 = len(cols),True,3         #2024 is one! arrays & data, 49 is significant
dtfile = 'ADI headings fin49o.csv'      #dtfile's not used herein; but see 1st program
dtfile2,vs = 'miniMyL4OM.adi','14d'     #add config file name here?

#fl4,fl0,fl3=(False,False,True,False,True,False),(True,True,False,True,True,False),(False,True,False,True,True,False)
ctFlgNm = [  'FwD',   'PwMC',  'FSp',   'PwD',   'PnC',   'FAT',   'StdC',  'Std',   'nVb',   'AlT',   'Rev',   'diag' ] #linked to flag arrays+
pgmCtFlgs = ['ttfttf','FTTFTF','100010','ftfttf','FFTFTF','111111','111 1 ','111011','11xx1x','111111','010111','t000t0' ]  #for now, 6 in each

def ele_pak(t,v,d,p,q):     #flag on end for data type                    t,v,d,p,q local
    'creates an ADI datagram from user provided data. 2 control flags'
    l = len(v)              #V value, t a tag string                      l local
    s1 = '<'+t+':'+str(l)   #what type is v?
    if q: s1 = s1+':'+d     #added the data type here
    s1 = s1+'>'+v           #tested, works!                               s1 local
    if p: s1 = s1+' '       #in python3 print is a function!
    if (v=='' or l==0 or t==''):  return ''
    else:  return s1

def ele_unpak(s,v):         #format 't:l(:d)>v'
    'takes apart a TLDV ADI format datagram'
    t,l,d,f ='err',0,'e',False  #set defaults
#    print (s,v)                # change > to a :
    if len(s) == 0:  return (f,t,l,d,v)  #check length first
    tdat = s.split(':')         #3 cols, 2 colons etc.
    
# remove trailing spaces in v if any? done outside, see __
    if len(tdat)==3:    d = tdat[2]
    elif len(tdat)==2:  d = 'n/a'
    elif len(tdat)==1:  return (f,t,l,d,v)
    else:   return (f,t,l,d,v)  #an error too
    if tdat[1]=='':     return (f,t,l,d,v)
    t,l = tdat[0],int(tdat[1])  #failing here #1 null
    if len(str(v))==l:  f = True
    else:  print (72,'  data: inconsistant L- tag',s)
    return (f,t,l,d,v)          #tuple output, v pass thru

def wrt_1line(k1,g1):           #there is no writeline only write...      g,k local
    'writes out a line of text to the screen and a logfile'
    if k1>0:  print (k1,line)   #line is a main global var
    g1.write(lend)
    g1.write(str(abs(k1))+' ')
    g1.write(line)              #diff from 1row, need parameter line input
    return -1                   #appears not to be used

def ele_unpak1(s,v):                                                      #t,l,d local
    'takes apart a TLDV datagram, the latest version'
    t,l,d,f = s,0,'',False      #3w +: +#
    if len(s) <5:  return(True,t,l,d,v)
    if s.find(':') > -1: pass   #ok if 1 or 2
    else:  return(True,t,l,d,v)
    sp = s.split(':')           #well controlled? picks up eor error
    if len(sp)==2:              #no d
        t,l=sp[0],sp[1]
    elif len(sp)==3:            #all of them
        t,l,d=sp[0],sp[1],sp[2]
    else:  f=True               #error flag
    if l=='':  l=0              #numeric
    else:  l = int(str(l))      #is v always string?
    if (len(v)==l) or (len(v.strip())==l):  pass    #ARRL uses // for a comment
    else:  print (98,'  data inconsistant L- tag',s)
    return (f,t,l,d,v)

def wrt_1linA(s,k,g):           #goal: s might be a list?
    'writes out a line of text, or opt string to the screen or a logfile'
    if (s=='') or (s==None):    #invert for true
        wrt_1line(k,g)
    else:                       #not null & not none
        if k>0:  print(k,s)
        g.write(lend)
        g.write(str(abs(k))+' ')
        g.write(str(s))         #g logging file
        g.write(lend)
    return -1

def opn_outp(k):        # originally, samOutput for sample output
    'opens the input (yes) file for conversion back to CSV'
    ks = str(k)         #creates file if; append mode +fiNo/              k local
    return open('hamOutput'+ks+str(selL)+'.adi','a')

def fmt_out(ls,y,f):
    'output a formatted-spaced file, with sep character'
    ll = len(ls)
    ct = ll
    while ct > 0:
        idx = ll-ct             #start at 0
        if f and idx==12:
            y.write('QSO_len')  #what about a legit null?
        else:
            y.write(str(ls[idx]))
        y.write(sep)
        ct += -1                #above, seperator
    y.write(nwLn)
    return ll

def det_newln(s):
    'looks for (detects) the OS newline in a text string'
    se = s[-1]
    return (str(se)==nwLn)  #with \n
    
def det_newlnA(s):
    'looks for the OS newline plus, in a text string'
    se = s[-2:]             #ok, w/ shortcut?                             s[] local
    return (str(se)==lend)  #w \r too

def rem_newln(s1):
    'removes the newline character from a line of read-in text'
    if det_newln(s1):
#        print( 146,'  newline slash n present' )
        return s1[0:-1]     #seems to work
    else:   return s1
    
def lod_tagS():             #binary created more issues
    'loads the tags in a read line for ADI lookup'
    line1 = lastline.split(',')
    line2 = line.split(',') #global in caller?
    del line1[-1]           #works!
    del line2[-1]           #removes \n appended by OS
    return line1+line2      #added more commas to data

def tradL4B(s):             #capitalize, subr; add 1 more
    'with the array pair, trades the l/c for u/c string'
    if s in ltTags:
        id = ltTags.index(s)
        s1 = bgTags[id]     #see lists above, portions of tags
    else:  return ''
    return s1

def multIdx(c,s):           #2nd pgm decoding function
    'for all c in string s, report positions in the list'
    ls = [None]             #init a list
#    print(169,c,s)
    p = s.find(c)           #get 1st one, beginning
    ct,ls = 1,[p]
    while (p>-1):           #last one found
        p = s.find(c,p+1)   #do a next one
        if p > -1:          #found one
            ls += [p]       #add to list
            ct += 1
        else:  pass         #remove Nones
    return (ls,ct)

def lod_dtypes():           #same issues as above
    'in a matching line, gets the ADI datatypes'
    line1 = line.split(',')
    del line1[-1]           #delete stray endings on both
    return line1

def roll_ck(h,ut,dh):           #more general than it needs to be         h local
    'given a hour and timezone calculates if the day has advanced'
    if ut:      return (h>=24)  #false means ok, just checks hours
    pass     #h, dh are integers, ut false now
    if dh==5:   return (h>=19)  #true means rolled
    elif dh==4: return (h>=20)  #can do this in hundreds
    else:    return (h+dh>=24)  #a non Eastern zone?

#def adv_tm(s,f1,f2):        #for EST, only 2 legit cases                 f1,s local
#    'original time shift using flags'
#    f3=(s.find(':')==-1)    #test for no colons
#    if (len(s) == 4):           pass    #remove :
#    elif (len(s)==3 and f3):    pass
#    else:
#        print (199,'  flag in advance time- incorrect format')
#        return -100
#    t = int(s)                                                           t,d local
#    d = 400             #no rollover here, see roll warn
#    if f1: d = 500      #adds 4 or 5 hours
#    if f2:              #alternate zone AST replaces, up USA
#        d = 300
#        if f1: d = 400
#    return t+d          #not rolling sum preserves going back?

def adv_tm1(s,z):       #different flag usage then first
    'adds a time shift to a four digit time- hhmm'
#    print (213,'input: ',s,z)
    f3=(s.find(':')==-1)    #test for no colons                           f2, f3 local
    if (len(s) == 4):           pass    #ditto
    elif (len(s)==3 and f3):    pass
    else:
        print (217,'  flag in advance time1- incorrect format')
        return (-100,False)
    t,d = int(s),100*z
    md = 2400         #starts w/ given zone
    if (t+d >= md):   return (t+d-md,True)
    return (t+d,False)  #assumes only up, like the other

def tme_splt(s):  #needs leading 0's- lower members
    'splits a time string into its component parts from text'
    f1 = ( s.find(':') > -1 )           #sets, if found                   f1 local
    hs,ms,ss='0','0','0'
    if ( (len(s)==8) and f1):           #hh:mm:ss 8 only #'s'
        hs,ms,ss=s[0:2],s[3:5],s[6:]
    elif ( (len(s)==7) and f1):         #h:mm:ss  7
        hs,ms,ss=s[0:1],s[2:4],s[5:]
    elif ( (len(s)==6) and (not f1)):   #hhmmss   6 or h:mmss? last unlikely
        hs,ms,ss=s[0:2],s[2:4],s[4:]
    elif ( (len(s)==5) and (not f1)):   #hmmss    5 likely error, no colon(s)
        hs,ms,ss=s[0],s[1:3],s[3:]
    elif ( (len(s)==5) and f1):         #hh:mm also 5, has a :
        hs,ms=s[0:2],s[3:]
    elif len(s)==4:                     #hhmm     4
        hs,ms=s[0:2],s[2:]
    elif len(s)==3:                     #hmm      3
        hs,ms=s[0:1],s[1:]
    else:
        print(243,'  decoding- unable to split time string')
        ss='66'             #output defaults then
    return (int(hs),int(ms),int(ss))

def solv_tof(sth,stm,lq):
    'computes time_off, adds small lengths of QSO times'
#    print (sth,stm,lq)     #echo check #s in
    df,eh = False,str(sth)  #input time fragments; df end date flag
    m = stm+lq              #lq max ~120 minutes                          m local
    if m<60:                #done :mm
        em = str(m)         #string out
        if m<10:  em='0'+em     #fix
    else:                   # >= 60, roll hour
        c=m//60             #fix for larger numbers, addd c*40            c local
        if c>1:  print (257,'  flag in solvTof- larger sum than expected',c)
        m += 40             #hr left, min right w/ h:mm, how many 40's
        b = str(m)          #convert to string, width?
        h = int(b[0])       #hour 1 digit only                            b, h local
        em = b[1:]          #recast
#--- min, above; hours below ------
        esm = h+sth         #carry plus :hh 2w?
        if esm < 24:        #check roll hrs
            eh = str(esm)   #done, df same
        else:               # >= 24, new day! ------
            esm += 76       #hour sum /w, 100s comp, how many 76's
            f1 = str(esm)   #convert to string                            f1 local
            eh = f1[1:]     # of dhh
            df = True       #leftmost flag, but 1
    return (eh+em,df)       #time sum at end; date roll would be to _off

def getQSOlen(f,s):     #comes in as strings, process numeric. as hhmm, Not hhmmss
    'to get the QSO length back from end time'
    ed,bg = tme_splt(f),tme_splt(s)     #tuple back
    print (276,'  end first: ',ed,bg)   #echo check
    df,borw = False,True    #flags, forcing borrow
    len1 = 60+ ed[1]-bg[1]  #always? >0, dM+60;             issue, len is a def function!
    if len1 >= 60:          #over 60, didn't borrow!
        len1 += -60         #length in minutes
        borw = False        #100's complement, sorta
    len2 = ed[0]-bg[0]      #hours, dH hours
    if borw:  len2 += -1
    if len2 <0:             #check for day roll
        len2 += 24
        df = True
    min = len1 +60*len2     #desired
    if len1 <10:     ot = '0'+str(len1)
    else:       ot = str(len1)
    return (str(len2)+ot,str(min),df)

def trans_xlt(v,p,g,a,b,c): #translation, Value tyPe taG... maybe here?
    #if true/false convert to Y N. convert case, maybe not?
    if v == 'TRUE':
        v = "Y"         #works ok now
        return (v,p,g)
    if v == 'FALSE':    #most of these are e(numerated) new p
        v = "N"         #boolean comes from Sheets
        return (v,p,g)
    if a:               #add tag time_off; main global
        if g=='QSO_len':
            if v == "":  print(302,'  missing QSO length- cant convert')
            else:
                stt=tme_splt(b)     #echo check stt, Tm4Col main global, row?
                oft=solv_tof(stt[0],stt[1],int(v))
#                print(stt,v,oft)            #look for null somewhere
                v=oft[0]            #check day flag- oft[1]
                if oft[1]:  print (308,'  flag in trans_xlt- day rolled over')
                p,g='t','time_off'          #add #8 to val, replace more input
    # pair are exclusive
    if ((g=='QSO_date') and c):
        nwdat = roll_1day(v)                #process date roll, zone change
        print(312,'  in date subs. old1',v,'new1',nwdat[0],'year',nwdat[1],'month',nwdat[2])  # +2 flags
        v = nwdat[0]                        #wrn #1 flag or rw[1]?
    return (v,p,g)                          #Value, tyPe, taG; p already t
    
def LpYrs(s):               #no century year logic, but 2000 was LY
    'checks if a recent year is a leap year'
    if len(s)==4: pass
    else:  return False
    j = int(s)              #check 1984, 2000, 2016 etc
    return ((j % 4) == 0)
    
def roll_1day(s):               #f1 removed, up in the USA
    '30 days hath Sept, April, June & November, all the rest have 31. Except...'
    g1,h=False,False            #clear year/month rolled flags            g1,h local
    if len(s)==8:   pass        #must be eight
    else:           return ('',g1,h)
    yr,md=s[0:4],s[4:]          #strip off year, save n/c                 s[] local
    dLpF = LpYrs(yr)                #boolean Flag back
    m,d=int(md[0:2]),int(md[2:])    #string to # actual; error, invalid in-day no leap year
    nyr = int(yr)+1             #if needed?
#---- dom section starts, use Dec as year roll check, new day?            d local
    m1 = m                      #save input month
    m2 = dyPm[m-1]              #days pm
#    print(m1,m2)                                                         m m1 m2 local
    if (m1==2 and dLpF):  m2=29 #override col data
#    print(s,m,d,nyr,dLpF)       #echo check
    if d+1 > m2:                #pre-rolled month 2
        m1,d = m+1,0            #convert dom to string, ns
        h = True                #month rolled
        g1 = (m1>12)            #if true 1/1 of next year else...
        if g1:                  #rolled year too
            m1=1
            yr = str(nyr)       #next year, print note?
    else:  pass                 #month didnt roll
    d += 1                      #ok to roll just a day
    ds,ms = str(d),str(m1)      #d and m2 convert 2str but pad
    if len(ds)==1:  ds = "0"+ds
    if len(ms)==1:  ms = "0"+ms     #pad singles
#---- doy section, lower probability of year roll <0.5% but...
#    dy = d+doySt[m-1]+1    #convert to next day of year
    md = ms+ds
    return (yr+md,g1,h)         #year rolled, false no issue w/ year

def revAset(iL1,vL2,g):         #1st is a list of int's to be dragged along
    'reverses a set assuming a string list V with index included'
    if g:
        ct = len(vL2)        #to create iL1 if can be int & in-order
        cSv = ct
        while ct > 0:
            ix = cSv-ct
            iL1[ix]=ix          #over writes the input
            ct += -1
    la,lb = len(iL1),len(vL2)   #lower case L
    if la == lb:  pass  #good
    else:
        print (368,'  entering data: ',iL1,vL2)
        return (vL2,iL1,True)   #an input error
    idx = la-1                  #start 1 less than size
    s21,iL2,vL1 = ['m']*la,['n']*la,['o']*la    # init the other arrays s21...
#    print (s21,s21s,iL2,vL1)
    while idx >=0:
        tmp = int(iL1[idx])
        tmp1 = str(tmp)
#        print (tmp1,vL2[idx])
        s21[idx] = vL2[idx]+ '|'+ tmp1
#        print ('in loop1',s21)
        idx += -1
#    print (380,'end 1st loop',s21)
    s21.sort()                  #sorts in place
    idx = lb-1                  #restart
    while idx >=0:
        pr = s21[idx].split('|')   #left is 0, right is 1
        iL2[idx],vL1[idx] = pr[0],int(pr[1])
        idx += -1
    return (iL2,vL1,False)
    
def buf_mgr(s,b,lef,adv):
    'manages a 1D queue with pop, push, R L, advance, etc. Null issue!'
    sp = str(s) #b is an incoming string
    if adv:
        if sp == '':    #pop, from left- easier
            if lef:
                ps = b.find(sep)
                if ps > -1:     #discard sep
                    sp = b[0:ps]
                    b = b[ps+1:]
                else:    pass   #null
                print (399,'  pop L',sp,'new b',b)
                return (b,sp)   #need tuple; no pop R needed if push L,R
            else:
#                print (402,'  advance only- no data')
                if len(b)==0:    pass
                else:    b = b+sep
        else:                       #push
            if lef:
#                wrt_1linA('  push L- lef True',-407,gg)
                b = sp+sep+b        #add on left
            else:
#                print(410,'  push R- lef False')
                if b == '':
                    b = sp          #new
                else:
                    b = b+sep+sp    #push right?
    else:
        if sp == '':                #null
            if lef:
#                print (418,'  cleared buffer, was:',b)
                return ''
            else:  print(420,'  read buffer, is:',b)
        else:                       #sp exists
            if lef:
#                print(423,'  add left',sp)
                b = sp+b
            else:
#                print(426,'  add right-default',sp)
                b = b+sp            #default
    return b

def fnd_tg(s,ln):       #find tag subr; pos 1 < than tag, see #1 version b
    if s=='':  return (False,1,s)
    s = '<'+s           #not found -1; needs < for tag too
    p2 = ln.find(s)     #the read line global
    f1 = (p2 > -1)      #ignores L...  ARRL & QRZ have different formats
    return (f1,p2+1,s)  #tuple back, p2' of tag start!

def fnd_tg1(s,ln):      #find ADI tag; pos 1 < than tag
    'improvement on find for ADI tags, which uses the colon end too'
    if s=='':  return (False,1,s)
    s = '<'+s+':'       #wrap param for tag2
    p2 = ln.find(s)     #the read line in parameter, not found -1
    f1 = (p2 > -1)      #ARRL & QRZ have different formats
    #issue: tags with a similar suffix, but a different ending!
    return (f1,p2+1,s)  #tuple back, s', p2' tag start!
 
def crt_dic(ls):    #based on a 2nd program segment
    'creates a simple dictionary for more than 1 value'
    j0 = len(ls)
    kvl = [None]*j0    #next step join two lists- real dict
    while j0 > 0:               #last 2 are line arrays
        k0 = j0-1               #loads 0 last
        kvl[k0] = (ls[k0],k0)  #temp tuple
        j0 += -1
    return dict(kvl)

def crt_dic1(ky,vl):    #based on a 2nd program segment
    'creates a proper key value pair dictionary'
    j0 = len(ky)
    if len(vl) < j0:    return {}
    dl = [None]*j0      #next join two lists- real dict
    while j0 > 0:                   #last 2 are line arrays
        k0 = j0-1                   #loads 0 last
        dl[k0] = (ky[k0],vl[k0])    #temp tuple
        j0 += -1
    return dict(dl)
cmds = crt_dic1(ctFlgNm,pgmCtFlgs)

def LnkLstTst(ls1,ls2,nully,f):
    'tests 2 linked lists 4 standard details & creates the bigger dictionary'
    f2,f3,hi = False,False,0    #NOT, sparse flags
    dname = 'no match'          #default
    f1 = ( len(ls1)==len(ls2) )
    if not f1:  return (f1,f2,0,hi,f3,0,dname)
    hi = len(ls1)               #they match, use list 1
    ct,ct2,ct3 = hi,1,1         #or 5% of list length +/-
    while ct > 0:
        id = hi-ct              #up from 0; see null types
        if ls1[id] == nully:  ct2 += -1
        else:  ct2 += 1
        if ls2[id] == nully:  ct3 += -1
        else:  ct3 += +1        #ie None,'', or 0
        ct += -1
    if ct2 > 0:  f2=True        #defaults to 1st list
    if ct3 > 0:  f3=True
    if ct2 >= ct3:
        if f:  dname = crt_dic(ls1) #dname the created dictionary
    else:       #print to test alignment of the data streams
        if f:  dname = crt_dic(ls2)
    return (f1,f2,ct2/hi,hi,f3,ct3/hi,dname) #match L, sparse-1, full+1, dict bigger1

def std_case(k,lin,g1):    #need a standard format so matching happens! use k?
    'makes the ADI data insensitive to case- the key to the 2nd program'
    ls,vl,tg,rs,tp = [],[],[],[],[]    #null lists for below; save found tag indexes
    lin = lin.lower()                  #get rid of the pesky comma w/ tilde or accent?
    #wrt_1linA(lin,489,g1)              #first view of
    ll = len(tgStrL)   #same as upper?
    hi = ll
    while ll > 0:       #loop thru l/c elements, lower --> std form
        idx = hi-ll                         #starts at 0 in l/c elements
        ti = fnd_tg1(tgStrL[idx],lin) #use sub2, is tagL there?
        if ti[0]:                           #some low MISSing; no change needed!
            ls += [idx]                     #save found index for use elsewhere?
            lin = lin.replace(tgStrL[idx],tgStr[idx],1)  #replace w/ std
        else:
            if ti[2] != '':  pass           #or print found?
#                print (500,'not found: |',ti[2],'|','in standardize')  #sticks w/ old value?
        ll += -1                            #next 1, idx goes ^
    bg = multIdx('<',lin)     #get all the begin markers- <eor> last
    ed = multIdx('>',lin)     #and the end's; the L's should match; all tuples
    cn = multIdx(':',lin)     #info markers, some :'s may Bin values, or dtypes
        #perform tests 1 & 2, if fails use #3 (req.); need 1 for all tags
    if bg[1] == ed[1]:  l2=bg[1]         #can't split group at end of line! n pairs/line
    else:                                   #check lists for L, : must be btw the first 2.
        print ( 516,'  error in standardize- different list L/ line?',bg[1],ed[1],cn[1] )
        return str(bg[1])  #check 3 values; patterns: <:> <::> ok, >:< not, <eor>, others- not
#    print (510,bg,ed,cn)

    cnn = cn[1]+1                           #1 less : due to eor; values given below?
    if cnn > l2:    rato = cnn/l2           #ratio of course
    elif cnn < l2:  rato = -1               #unexpected error condx, trap? or 0
    else:           rato = 1                #always 1 less colon, none in end of record
    dtypcnn = (rato > 1.5)                  #a guess, w/ dtypes+; log this?
    if dtypcnn:  print( k,'data types suspected- standardize: extra colons:',rato )
    
    k2,k3 = 0,0  #an integer, below strings
    for k1 in myDatL:                  #iterate on lower myData, some are MISSing
        if k1 != '':
            lin = lin.replace(k1,myDat[k2],1)   #if null skip
        k2 += 1     #goes up with k1 1 step
                    #capitalize, base it on the tag; all lists like above thus changeable
    
    wrt_1linA(lin,534,g1)                #2nd view of
    hi2 = ed[1]     #counted > symbols, or values, should also equal beginning
    while l2 > 1:           #start while, on end index
        idx2 = hi2-l2       #values portion- last1 has no next (<). Maybe, use end of line?
        idx21 = idx2 +1     #goes to the end, but stops @2
        vl += [lin[(ed[0][idx2]+1):bg[0][idx21]]]   #get corresponding value for pairs
        tg += [lin[(bg[0][idx2]+1):ed[0][idx2]]]    #and the tag (inside too)- save for later
        tp += (tg[idx2],vl[idx2])
        l2 += -1                            #tags determine action on values; use 'in' again?
    print ( 543,'extracted t&v: ',tp )      #strip inside tg? +1 would be at end of string...
    if len(tg)==0:  return str(l2)          #nothing found
    
    for j1 in tg:                           #loop thru found tags, should be 1 or more
        j2 = j1.split(':')                  #remove innards of < :l(:t)>
        fd,os1,os2 = True,'',''             #below are exclusive; add '>'?
        if j2[0] in upStr:
            os1 = '>'+vl[k3].upper()
            lin = lin.replace('>'+vl[k3],os1,1)
        elif j2[0] in capSt:
            os2 = '>'+vl[k3].title()
            lin = lin.replace('>'+vl[k3],os2,1)
        else:                               #above, alter value
            #os1,os2 = '',''
            fd = False
#            print ( 532,'value not changed 4: ',tg[k3],'standardize',j2[0] )
        print ( 551,j1,j2,'os1 & 2:',os1,'|',os2,'|' )
        rs += [fd]                          #store each result, then?
        k3 += 1                             #next
    wrt_1linA(lin,562,g1)                    #3rd/last view of
    print (563,rs,'values')                 #boolean list
    return lin   #use the case list & caps, for both: see csub library
    
def rem_ARL (vl):   #splits off ARRL comment
    'removes but saves the ARRL comment field part of V'
    p = vl.find('//')
    f = (p>-1)      #found
    if f:
        v2 = vl.split('//')     #in half, are 3 possible?
        return (f,v2[0],v2[1])  #both halves
    return (f,vl,'none')
    
def get_Bol (s):                #creates boolean list
    'creates a boolean list given a prototype string of ch.'
    ct,lo = -len(s),[]
    while ct < 0:
        c = s[ct]
        vl = ( c=='T' or c=='t' or c=='1' )
        lo += [vl]
        ct += 1
    print (583,'  loaded program control flags:',lo,'from:',s)
    return (lo)
    
def rtnPflgs(pn):       #gets a control set, either pgm 1/2
    'uses boolean subroutine to pick a program control flag set'
    if (pn > 2) or (pn < 1):  return ''
    pn += -1                    #makes boolean, see new invert below
    if pn:  idx = selL2+6       #pgm number 2
    else:  idx = selL           #1st program
    print ( 592,'code:',ctFlgNm[idx] )
    return get_Bol(pgmCtFlgs[idx])

def ovrrFlgs(pgm,cmNo):     #use selL to get the set (first 6 in the array)
    print ( '  the default command Set is:', cmNo )
    pgm += -1 #convert to boolean
    if pgm:  print ( 598,'the other choices are:',ctFlgNm[6:] )
    else:    print ( 599,'the other choices are:',ctFlgNm[0:6] )    #1st of the array program 1; use pgm here
    uin = input('do you want to override the current flags? y/n ')
    if uin != 'y':  return ''                                   #do nothing
    ui2 = input('enter Mnemonic command string? ~3 ch. ')        #new nemonic another input
    if pgm:  rs = cmds.get(ui2,'Std')   #dictionary: key nemonic/ val cmds
    else:  rs = cmds.get(ui2,'PwD')
    si = cSub.pgmCtFlgs.index(rs)       #update local set. And global below
    return (rs,si)                      #new string/ default; tf equiv.

def Npadd(s):   #detects wh spc issue Wrt L
    'tests for no padding in a string'
    w,wo = len(s),len(s.strip())
    return (w==wo)              #for values
    
def invB(n):  #uses binary addition to complement
    'inverts a simple binary number thru addition'
    if n < 0: return 0  #an error
    n += 1              #invert inc
    if n > 1: return 0
    return 1

#add subroutines based on import module values
def tmStr():
    return time.asctime()
    
def ppArgs():
    return sys.argv
    
def tmRel():
    return time.time()
    
def onWhat():
    return sys.platform
    
def explr(s,v):
    print (s, '----------', nwLn, dir (v), nwLn, v.__doc__ )
    print ('  end of:',v.__name__, nwLn)
    return -1

# subroutine testing:
if __name__ == '__main__':
    print ( '  begin subroutine testing: ',tmRel(),'version: ',vs )
    print ( solv_tof(13,3,8),solv_tof(22,44,16),solv_tof(23,55,45),solv_tof(17,45,24),solv_tof(2,4,2),solv_tof(7,1,5) ) #passed, but add more
    print ( LpYrs('1984'), LpYrs('1983'), LpYrs('2000'), LpYrs('2015'), LpYrs('2016') ) #passed
    print ( roll_1day('20190227'), roll_1day('20231231'), roll_1day('20221031'), roll_1day('20180625'), roll_1day('19570122'), roll_1day('20160327') )
    print ( adv_tm1('1411',4),adv_tm1('1945',5),adv_tm1('2310',4) )
    print ( adv_tm1('0331',5),adv_tm1('1411',4),adv_tm1('155',5),adv_tm1('1945',4),adv_tm1('1123',4),adv_tm1('2310',1) )
    print ( ele_unpak('qso:2:s',25), ele_unpak('time:4:t',3), ele_unpak('zone:2:e','de'), ele_unpak('call:5:s',222), ele_unpak('abcd',1), ele_unpak('date:4',1335), ele_unpak('rst_sent:3','yes')  )
    ab,xy = ['b','a','d','c','','','z'],[3,4,5,6,7,8,9]
    print ( revAset(xy,ab,False), revAset(xy,ab,True) )
    h,samLs = open('libTestFil.txt','a'),[5,6,7,8,9,10,11,12,13,14]
    fmt_out(samLs,h,False)
    h.close()
    print ( buf_mgr('a','1234',True,False), buf_mgr('1','abcd',False,False), buf_mgr('25','56434828',True,True), buf_mgr('44','eeeeee',False,False), buf_mgr('','qewpuiower',False,True), buf_mgr('','abcd',True,False), buf_mgr('','r4t5y6u7',False,False), buf_mgr('','asde,493902,54jks,ghj',True,True) )
    print ( getQSOlen('2245','2130'), getQSOlen('1225','1220'), getQSOlen('2349','0002'), getQSOlen('0058','0043') )
    print ( tradL4B('rx'), tradL4B('qso'), tradL4B('qrz'), tradL4B('dxcc'), tradL4B('intl'), '|',tradL4B('abcd'),'|' )
    print ( multIdx(',','eroi,540,alsk,235'), multIdx('/','gjs/t567/wer=567'), multIdx('<','adf<456>gkfd=45,45<we'), multIdx('>','45>678<995>rty') )
    print ( tmStr(), 'paths:', sys.path, 'arguments:', ppArgs(), 'platform:', onWhat(), 'sep:', os.sep, 'line:', os.linesep)
    print ( 'The QUICK brown FOX?'.lower(), 'jumped over THE lazy [dogs]'.upper(), 'back! 0123456789'.capitalize() ) #"/><|}{\-=+!@#$%^&*()_+".capitalize() )  issue 1 or more
    print ( crt_dic( ['y','z','a','b','f','m'] ) )
    print ( LnkLstTst(tgStr,tgStrL,'',True ), nwLn, LnkLstTst(bgTags,ltTags,'',True ) )
    print ( LnkLstTst(myDat,myDatL,'',True ), nwLn, LnkLstTst(ctFlgNm,pgmCtFlgs,'',True), nwLn, cmds )
    print ( get_Bol('fftftf'), get_Bol('111111'), get_Bol('011010'), get_Bol('TFFFTF'), rtnPflgs(1), rtnPflgs(2) )
    print ( 'binary test:',invB(1),invB(0),invB(3),invB(-5) )
else:
    print ( __name__,__doc__,nwLn,'new command dictionary:',cmds,nwLn )
    print ( dir (hBx), nwLn, '  end of:', hBx.__name__, nwLn )
    print ( 'callinfo',nwLn, dir (hBx.callinfo),nwLn,nwLn, hBx.callinfo.__doc__ )    #below based on this start
    print ( explr ('hamtools: Callinfo',hBx.Callinfo), explr('& LookupLib',hBx.LookupLib), explr('tK based cgi',tKw)                             )
    print ( explr ('callinfo & logging:',hBx.callinfo.logging), explr('... & date time',hBx.callinfo.datetime), explr('... & timezone',hBx.callinfo.timezone) )