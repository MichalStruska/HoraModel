import numpy as np


#%%
beta_cas = ["12:"]
beta_cas2 = []
for be in beta_cas:
    beta_cas2.append(be.hour+be.minute/60+be.second/3600)
beta_elev=ambi_dat[:,2]

#%%
ratio=(1,6)
switch=18

ztraty_vs=[]
v_rs=[]
v_rs_=[]
poces=[]
poces0=[]
        

Talt=[-5,5,10]
RHalt=[-10,10,20]
Hdry_vsi=[]
ztraty=[]
casti=['A','FA','S','T','H','FH','TO']
Ajs=[0.07,0.07,0.2,0.19,0.05,0.07,0.35]
zmena=[]

minit=ambi_dat[0,6]*60

v_avg=ambi_dat[0,7] # m/s
v_w=0
dist=v_avg*minit*60

t_celk=(minit*60)/(ratio[0]+ratio[1])
t_w=ratio[0]*t_celk
t_r2=ratio[1]*t_celk
t_r=minit*60-t_w
v_r=(dist-v_w*t_w)/t_r
poces0.append([v_w,ratio,switch])

pocet=int((switch/2)+0.5)
length_w=t_w/pocet
length_r=t_r/pocet
zmeny_r,zmeny_w=[],[0]
pocitac0=0

Kskins=[0]
Tcores=[37]
mst=80 # kg -- hmotnost
st=180/100# m -- vyska


alfa=0.41
RHrange=22 # denni rozsah vlhkosti %
RHavg=ambi_dat[0,5] # denni prumerna vlhkost %
tmax=15 # cas Tmax
Trange=17 # denni rozsah teplot C
Tmax=ambi_dat[0,4] # maximalni tyeplota C
Tdiff=5 # rozdil mezi Tmax a denni maximalni Tg C
tst=ambi_dat[0,3]

r=0.15 #reflektance
sigma=5.67*(10**-8) # Stefan-Boltzmann konstanta W m-2 K-4

Clo=0.1 # oblecenost -- Mairiaux
hvap=2426000 # J/kg
a=0.8 # absorbitivita vlasu a kuze
fhair=0.15
ehair=0.8
Khair=10 # W m-2 °C-1 konduktance vlasu

tdelay=435 # s -- time delay
dskin=0.002 # m -- tloustka kuze
rho_skin=1060 # kg*m-3 
cbody=3500 # merna tepelna kapacita J °C-1 kg-1
k=8.3 # konvekcni koeficient W m-2 °C-1
cblood=3850 # J*l-1*C-1 -- volume-specific heat capacity of blood
SkBFs=np.arange(0,0.133,0.0005) # skin blood flow l s-1 mezi 0 a 0.133  Arbitrarne !!!!!!!!!!!!!!!!!!!!!!!!!
SkBF=0 # pocatecni hodnota
Ktis=9 #W m-2 -- tissue conductance
w_min=0.06 # minimum wetedness
RMR= 2.177+(100.055/mst) # ml(O2)/(kg*min)

#------------------- startovni hodnoty
#------------------- Matice
Tskins=[]
Mruns=[]
Eskins,Hflows=[],[]
RWLs=[]
SLs=[]
Thairs=[]
Tskin_cel=[]
macts=[mst]
Tairs=[]
RHs=[]
betas=[]
SkBF_rec=[]
Ss=[]
frs=[]
Mwalks=[]
ws=[]
#%%
#------------------- 
pocit=0
SL=0
for cas in np.arange(0,int(minit*60)):
    if cas in zmeny_w:
        w_r='w'
    if cas in zmeny_r:
        w_r='r'
    while beta_cas2[pocit]<tst+(cas/3600):
        pocit+=1
    
    # if cas<len(SkBFs):
    #     SkBF=SkBFs[cas]
    # else:
    #     SkBF=SkBFs[-1]
    
    mact=macts[-1]-SL
    A=((mact**0.425)*((st*100)**0.725)*71.84)/10000 # m2 -- plocha tela
    if w_r=='r':
        v=v_r
    elif w_r=='w':
        v=v_w     
        
    beta=90-beta_elev[pocit] # mezi 0 a 180 -- elevace slunce ve stupnich -- musi byt zenit (tj. 90-beta)
    fr=4.8276*(10**(-7))*(beta**3)-((8.1371*10**(-5))*(beta**2))+(9.6369*(10**(-4))*beta)+0.3036
    frs.append(fr)
    t=tst+(cas/3600)#denni hodina behu h
    T200=(Trange/2)*np.sin((2*np.pi*(t+tmax))/24)+Tmax-(Trange/2)
    Tg=((1.4*Trange)/2)*np.sin((2*np.pi*(t+tmax+1))/24)+Tmax+Tdiff-(1.4*Trange)/2
    T_air=T200+alfa*(Tg-T200)
    RH=(RHrange/2)*np.sin((2*np.pi*(t-2))/24)+RHavg #60 # relativni vlhkost vzduchu %
    Mrun=(0.41*(v**2)+1.357*v+5.331)*mact
    Mruns.append(Mrun)
    Mwalk=(2*RMR+5.6*(v_w**2)*st)*mact
    Mwalks.append(Mwalk)
    if w_r=='r':
        M=Mruns[-1]
    elif w_r=='w':
        M=Mwalks[-1]
    
    Rg=sigma*(Tg+273)**4
    S=1121*(np.cos(((beta)/180)*np.pi)-0.08251) #!!!!!!!!!!!!!!!!! nemuze tu byt +90
    s=S/9
    Rsky=213+5.5*T200
    P_air=0.61121*(math.e**((18.678-T_air/234.5)*T_air/(257.14+T_air)))*(RH/100)
    if cas==0:
        Tskin=30+0.138*T_air+0.254*P_air-0.571*v+1.28*(10**(-3))*M-0.553*Clo
        Tskins.append(Tskin)    
    
    e_resp=0.0173*M*(5.87-P_air)
    RWL=e_resp/hvap
    
    Cresp=0.0014*M*(T_air-34)
    
    mskin=A*dskin*rho_skin
    mcore=mact-mskin
    
    Tskin=Tskins[-1]
    Kblood=(SkBF*cblood)/A
    if cas in zmeny_vse:
        pocit_c=0
        while zmeny_vse[pocit_c]!=cas:
            pocit_c+=1
        Kskin0=Kskins[-1]
        Kskin_=Ktis+Kblood
        tlag=cas-zmeny_vse[pocit_c]
        Kskin=Kskin0+(Kskin_-Kskin0)*np.sin(np.arccos(1-(tlag/tdelay)))
    else:
        Kskin=Ktis+Kblood
    Kskins.append(Kskin)
    
    T_core=Tcores[-1]
    
    Hflow=Kskin*A*(T_core-Tskin)
    dTcore= (M+Cresp-e_resp-Hflow)/(cbody*mcore)
    Tcores.append(T_core+dTcore)
    if dTcore>0 and SkBF<0.133:
        SkBF=SkBF+0.0001
    elif dTcore<0 and SkBF>0:
        SkBF=SkBF-0.0001
    else:
        pass
    SkBF_rec.append(SkBF)
    Hdryjs=[]
    for j in np.arange(0,7):
        Tk=Tskins[-1]
        Tskinj=Tskins[-1]
        Aj=Ajs[j]*A
        Qrj=sigma*(Tk**4)
        Qabsj=fr*a*S+0.5*(a*s+a*r*(S+s)+Rsky+Rg)
        Cskinj=k*(np.sqrt(v))*(T_air-Tk)
        if j == 5:
            Thair=((Cskinj-Qrj+Qabsj)/Khair)+Tskinj
            Thairs.append(Thair)
        Hdryj=(Qabsj-Qrj+Cskinj)*Aj
               
        
        Hdryjs.append(Hdryj)
    
    P_skin=0.61121*(math.e**((18.678-Tskin/234.5)*(Tskin/(257.14+Tskin))))
    Hdry=sum(Hdryjs)
    Emax=(P_skin-P_air)*(v**(1/2))*A*124*(fhair*(ehair-1)+1)
    w_req=(Hflow+Hdry)/Emax
    w=0.94*w_req+w_min # wetedness
    if w>1:
        w=1
    ws.append(w)
    Eskin=Emax*w
    SL=(Eskin/(fhair*(ehair-1)+1))/hvap
    d_Tskin=(Hdry-Eskin+Hflow)/(cbody*mskin)
    Tskins.append(Tk+d_Tskin)
    
    
    Eskins.append(Eskin)
    Hflows.append(Hflow)
    RWLs.append(RWL)
    SLs.append(SL)
    Tskin_cel.append(Tskin)
    betas.append(beta)
    Tairs.append(T_air)
    RHs.append(RH)
    Ss.append(S)
    

ztrata=sum(RWLs)+sum(SLs)
ztraty.append(ztrata)
Hdry_vsi.append(Hdryj)
#print(jedin[jed,0])
print([v_w,ratio,switch])

plt.plot(Tcores)
# plt.figure()
# plt.plot(Tskins)
# plt.title(jedin[jed,0]+'_Tskin')
#print(Hdryj)
# plt.figure()
# plt.plot(SkBF_rec,color='green')
# plt.title(jedin[jed,0]+'_SkBF')
#print('--------------------------')
poces.append([v_w,ratio,switch])

      