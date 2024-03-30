'test program for library routines: format conversion ADI <--> CSV'
import ADIsensaiMod18d as cB                     #3/28/2024 JRJ
nwLn,vers = '\n','5e'
#increases diversity in Case; easy classification by eye & ensures standardization; tag portions!
#ltTags = ['qso','qsl','iota','lotw','my','qth','sig','stx','sat','rst','intl','rx','tx','qrz','dxcc','eqsl','city','cnty','band','skcc','country','arrl','itu','nr','app','ham','eoh','eor',]
#
print ( nwLn,'  begin subroutine testing 1/2: ',cB.tmRel(),'version: ',vers )   #below were imported from ADIsensaiModxx
print ( cB.solv_tof(13,3,8),cB.solv_tof(22,44,16),cB.solv_tof(23,55,45),cB.solv_tof(17,45,24),cB.solv_tof(2,4,2),cB.solv_tof(7,1,5) ) #passed, add more
print ( cB.LpYrs('1984'), cB.LpYrs('1983'), cB.LpYrs('2000'), cB.LpYrs('2015'), cB.LpYrs('2016') ) #passed
print ( cB.roll_1day('20190227'), cB.roll_1day('20231231'), cB.roll_1day('20221031'), cB.roll_1day('20180625'), cB.roll_1day('19570122'), cB.roll_1day('20160327') )
print ( cB.adv_tm1('1411',4),cB.adv_tm1('1945',5),cB.adv_tm1('2310',4) )
print ( cB.adv_tm1('0331',5),cB.adv_tm1('1411',4),cB.adv_tm1('155',5),cB.adv_tm1('1945',4),cB.adv_tm1('1123',4),cB.adv_tm1('2310',1) )
print ( cB.ele_unpak('qso:2:s',25), cB.ele_unpak('time:4:t',3), cB.ele_unpak('zone:2:e','de'), cB.ele_unpak('abcd',1), cB.ele_unpak('date:4',1335), cB.ele_unpak('rst_sent:3','yes')  )
ab1,xy = ['b','a','d','c','','','z'],[3,4,5,6,7,8,9]
print ( cB.revAset(xy,ab1,False), cB.revAset(xy,ab1,True) )
h,samLs = open('libTestFil.txt','a'),[5,6,7,8,9,10,11,12,13,14]

#out test and close moved
print ( cB.buf_mgr('a','1234',True,False), cB.buf_mgr('1','abcd',False,False), cB.buf_mgr('25','56434828',True,True), cB.buf_mgr('','abcd',True,False) )
print ( cB.getQSOlen('2245','2130'), cB.getQSOlen('1225','1220'), cB.getQSOlen('2349','0002'), cB.getQSOlen('0058','0043') )
print ( cB.tradL4B('rx'), cB.tradL4B('qso'), cB.tradL4B('qrz'), cB.tradL4B('dxcc'), cB.tradL4B('intl'), '|',cB.tradL4B('abcd'),'|' )
print ( cB.multIdx(',','eroi,540,alsk,235'), cB.multIdx('/','gjs/t567/wer=567'), cB.multIdx('<','adf<456>gkfd=45,45<we'), cB.multIdx('>','45>678<995>rty') )
print ( cB.tmStr(), 'paths:', cB.sys.path, 'arguments:', cB.ppArgs(), 'platform:', cB.onWhat(), 'sep:', cB.os.sep, 'line:', cB.os.linesep)
print ( 'The QUICK brown FOX?'.lower(), 'jumped over THE lazy [dogs]'.upper(), 'back! 0123456789'.capitalize() ) #"/><|}{\-=+!@#$%^&*()_+".capitalize() )  issue 1 or more
print ( cB.crt_dic( ['y','z','a','b','f','m'] ) )
print ( cB.LnkLstTst(cB.tgStr,cB.tgStrL,'',True ) ) #, nwLn, cB.LnkLstTst(cB.bgTags,cB.ltTags,'',True ) )
print ( cB.LnkLstTst(cB.myDat,cB.myDatL,'',True ), nwLn, cB.LnkLstTst(cB.ctFlgNm,cB.pgmCtFlgs,'',True), nwLn, cB.cmds )
print ( cB.get_Bol('fftftf'), cB.get_Bol('011010'), cB.rtnPflgs(1), cB.rtnPflgs(2) )
print ( 'binary test:',cB.invB(1),cB.invB(0),cB.invB(3),cB.invB(-5) )

#run same tests with new class names; copied from the library? +meta class statement? make sure methods have access to globals.
class FmCv:                                      #test: wrapper for functions from above
    def ADI_ele_pak(self,p1,p2,p3,p4,p5):        #5 ok
        return cB.ele_pak(p1,p2,p3,p4,p5)
        
    def ADI_unpak1(self,p1,p2):                  #2 ok
        return cB.ele_unpak1(p1,p2)
        
    def fIO_fmt_out(self,p1,p2,p3):              #3 ok
        return cB.fmt_out(p1,p2,p3)

    def Dtme_adv_tm1(self,p1,p2):                #2 ok
        return cB.adv_tm1(p1,p2)
        
    def Dtme_tme_splt(self,p1):                  #1 ok
        return cB.tme_splt(p1)
        
    def Dtme_solv_tof(self,p1,p2,p3):            #3 ok
        return cB.solv_tof(p1,p2,p3)
        
    def Dtme_getQSOlen(self,p1,p2):              #2 ok
        return cB.getQSOlen(p1,p2)
        
    def Dtme_roll_1day(self,p1):                 #1 ok
        return cB.roll_1day(p1)

    def arry_buf_mgr(self,p1,p2,p3,p4):          #4 has a null issue
        return cB.buf_mgr(p1,p2,p3,p4)
        
    def arry_revAset(self,p1,p2,p3):             #3 ok
        return cB.revAset(p1,p2,p3)
        
    def arry_crt_dic1(self,p1,p2):               #2 tried in main pgm
        return cB.crt_dic1(p1,p2)

    def plogs_wrt_1line(self,p1,p2):             #2 last p both file handle, uses global line
        return cB.wrt_1line(p1,p2)
        
    def plogs_wrt_1linA(self,p1,p2,p3):          #3 first is a string, 2nd line number; both ok!
        return cB.wrt_1linA(p1,p2,p3)
        
    def strHd_det_newln(self,p1):                #1 ok
        return cB.det_newln(p1)
        
    def strHd_det_newlnA(self,p1):               #1 ok
        return cB.det_newlnA(p1)
        
    def strHd_rem_newln(self,p1):                #1 ok
        return cB.rem_newln(p1)
        
    def strHd_Npadd(self,p1):                    #1 ok
        return cB.Npadd(p1)
        
    def strHd2_fnd_tg1(self,p1,p2):              #2 both used ok
        return cB.fnd_tg1(p1,p2)
        
    def strHd2_fnd_tg(self,p1,p2):               #2 ditto
        return cB.fnd_tg(p1,p2)
    
    def misc_invB(self,p1):                      #1 ok normal in's
        return cB.invB(p1)
        
    def misc_explr(self,p1,p2):                  #2 ok
        return cB.explr(p1,p2)
        
    def misc_get_Bol(self,p1):                   #1 ok
        return cB.get_Bol(p1)
        
    def Dtme_LpYrs(self,p1):                     #1 ok
        return cB.LpYrs(p1)
        
    def strHd2_rem_ARL(self,p1):                 #1 ok
        return cB.rem_ARL(p1)

#begin testing of this new class
ab = FmCv()
print ( 'class examples 2/2:',nwLn,'2004, leap?',ab.Dtme_LpYrs('2004') )
print ( ' and ARRL test:',ab.strHd2_rem_ARL('abcdef_//_ghijk '),'time:',ab.Dtme_tme_splt('220557') )
print ( ' & boolean test:',ab.misc_get_Bol('10010110'),nwLn,ab.misc_get_Bol('t0t0t0ff0') )
print ( ' and padding test:',ab.strHd_Npadd('abcd '),ab.strHd_Npadd(' efgh'),ab.strHd_Npadd('ijkl') )
print ( ' & invert fx:', ab.misc_invB(1),ab.misc_invB(0),ab.misc_invB(5),ab.misc_invB(-1) )
print ( ' and detect/remove newline:', ab.strHd_det_newln('abcd'), ab.strHd_det_newln('efgh\n'), ab.strHd_det_newlnA('asdf\r\n'), ab.strHd_rem_newln('efgh\n') )
print ( ' & get QSO length:', ab.Dtme_getQSOlen( '2301','2205' ), ab.Dtme_getQSOlen( '0005','2358' ) )
print ( ' ADI tests:',ab.ADI_unpak1('QSO_len:2:n','23'),ab.ADI_ele_pak('QSO_len','23','n',True,True) )

cB.line = 'The quick brown fox jumped over the lazy dogs back 0123456789'
ab.plogs_wrt_1line(118,h)
ab.plogs_wrt_1linA('test message23',-119,h)   #try fioFmtOutput and writelines

print ( nwLn, 'time off:',ab.Dtme_solv_tof(21,58,7) )
ab.fIO_fmt_out(samLs,h,False)
print ( '  & more time functions:',ab.Dtme_roll_1day('20240229'),ab.Dtme_adv_tm1('1345',4) ) #last param is hrs
print ( ab.arry_revAset(xy,ab1,False), ab.arry_revAset(xy,ab1,True) ) # +reverse asset test; copy example

def fndStr(lt,s):
    ps = s.find(lt)
    return (ps>-1)

def tradL4B(s):   #duplicate from library, for standard case use.  10.0 used here
    'with the array pair- bg lt, trades the l/c form for u/c. used for testing'
    bgTags = ['QSO','QSL','IoTA','LoTW','MY','QTH','SIG','STX','SAT','RST','INTL','RX','TX','QRZ','DXCC','eQSL','CITY','CNTY','BAND','SKCC','COUNTRY','ARRL','ITU','NR','APP','HAM','EOH','EOR',]
    if s in cB.ltTags:
        id = cB.ltTags.index(s)
        s1 = bgTags[id]     #see lists above, portions of tags
    else:  return ''
    return s1

def liLbigChk(ls,eTh):   #little big horn?
    'function to test preferred cap (array: 4-5 to do) data structures'
    print(nwLn,'----------begin new array test:')
    ec = [None,None,None]
    ec[0] = ( 'srx_string','rx' )
    ec[1] = ( 'station_callsign','sig' )
    ec[2] = ( 'ituz','itu')
    ps1ers = 0                          #error counter
    ll = len(ls)-1                      #a list of short strs compute the L
    ct = ll
    sl = len(cB.ltTags)-1               #compute the possible ltTags list length
    ct1 = sl
    while ct >= 0:                      #go thru input list for littles
        ele = ls[ct]
        if ele != '':
            print ( ' pass1, checking:',ele )
            while ct1 >= 0:             #need inner loop 1a
                ref = cB.ltTags[ct1]
#                print ( '  inner loop:',cB.ltTags[ct1], )   #e.g. skip rx in srx
                if fndStr(ref,ele):
                    ps1ers += 1         #report occurance of littles- summing
                    ths1 = (ele,ref)    #error tuple
                    if ths1 in ec:
                        ps1ers += -1
                        print ( '  exception ok:',ths1 )  #exception are ok
                    else:    print ( '  found:',ref,'in:',ele )   #+L2B here
                else:   pass            #use L2B subr: cB.tradL4B(s)
                ct1 += -1
        ct1 = sl
        ct += -1
    if ps1ers > eTh:  return ps1ers       #allow up to 2 errors
    print (' passed test1- littles:',ps1ers,'/',eTh)  #if <= eTh continue
    ct2 = ll                            #start loop2- test for cB.bgTags
    lo = []
    bl = sl  #len(cB.bgTags)-1  #big tags- needs to see or assume same length? sl
    ct3 = bl
    while ct2 >= 0:                         #loop thru input list again
        ele2 = ls[ct2]
        print ( ' pass2, checking:',ele2 )  #look for nulls here too
        while ct3 >= 0:                     #inner loop 2a, same L (as littles)
            ref2 = tradL4B(cB.ltTags[ct3])     #fix me
#            print ( '  inner loop2:',ref2,ele2, )
            if fndStr(ref2,ele2):
                print ( '  found a match@',ct3,'for:',ref2,'in:',ele2 ) #report bigs used & sum
                lo = lo +[ele2]
            ct3 += -1
        ct3 = bl
        ct2 += -1               #report change the stray littles to bigs
    return lo                   #return all the bad elements (and littles)

ab.misc_explr('Python ham tools, top classes:',cB.hBx)      #last below is an issue
print ( liLbigChk( cB.tgStr,1 ) )
print ( liLbigChk( cB.myDat,1 ) )
print ( liLbigChk( cB.upStr,1 ) )
print ( liLbigChk( cB.capSt,1 ) )
print ( liLbigChk( cB.tgEcpts,4 ) )
h.close