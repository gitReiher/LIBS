import pandas as pd
import numpy as np
import math
import re
import plotly.graph_objects as go

#plotting function using plotly
def pltconfig(fig,elem):
    
    fig.update_layout(title=dict(text=" Spectrum "+str(elem) ,x=0.5, xanchor='center',font_size=30,y=0.9 ),
                  plot_bgcolor='#f4f4f4',legend=dict(x=0.75,y=0.9,bordercolor='black',borderwidth=1,font_size=15) ,
                  showlegend=True,font_family='arial',
                  xaxis=dict(title=dict(text=r'$\large \lambda\ (nm)$',font_size=17), range =[200,600] ),                   
                  yaxis=dict(title=dict(text=r'$\Large \text{ Intensity  (a.u.)}$',font_size=30)),
                  )
    fig.update_layout(autosize=False, width=800, height=500)
    fig.show(config={'scrollZoom': True,'editable': True})
    
#Gaussian broadening of emission lines    
def _1Gauss(x, amp, cen,wid):
    return (amp*np.exp(-(x-cen)**(2)/(wid**2))/np.sqrt(np.pi)/np.abs(wid))
def _NGauss(x,I,wvls,wid):
    f=0
    for i in range(len(wvls)):
        f+=_1Gauss(x,I[i],float(wvls[i]),float(wvls[i])/wid)
    return f    
# read emission lines data
def readlines(elem,ion1,ion2):
    maindir='/home/reiher/Documents/Pesquisa, extensão e material extra/LIBS/Simulando espectros/dadosNIST/linhas_emissao/'
    if ion1<=ion2:
        try:
            df=pd.read_csv(maindir+elem+' '+str(ion1)+'.csv')
            df.drop( [df["gA(s^-1)"].index[i] for i in df["gA(s^-1)"].index if math.isnan(df["gA(s^-1)"].values[i])] ,axis=0,inplace=True)
            df["Ek(eV)"].replace(regex=r'[^\d.]+',value='',inplace=True)
            df["ritz_wl_air(nm)"].replace(regex=r'[^\d.]',value='',inplace=True)
            df["Ek(eV)"]=pd.to_numeric(df["Ek(eV)"],downcast="float")
            df.reset_index()
            return [df[["Ek(eV)","gA(s^-1)","ritz_wl_air(nm)"]]]+readlines(elem,ion1+1,ion2) 
        except pd.errors.EmptyDataError:
            return [pd.DataFrame(data=[[0,0,0]],columns=["Ek(eV)","gA(s^-1)","ritz_wl_air(nm)"] )]+readlines(elem,ion1+1,ion2)
    else:
        return []
# read energy levels data
def readlevels(elem,ion1,ion2):
    non_decimal = re.compile(r'[^\d.]+')
    if ion1<=ion2:
        try:
            df=pd.read_csv('/home/reiher/Documents/Pesquisa, extensão e material extra/LIBS/Simulando espectros/dadosNIST/niveis_energia/'+elem+" "+str(ion1)+'.csv')
            df.drop(df[df["Level (eV)"]==" "].index,axis=0,inplace=True)
            for i in range(len(df["Level (eV)"].values)):
                df["Level (eV)"].values[i]=non_decimal.sub('',str(df["Level (eV)"].values[i]))
            df=df.reset_index()
            index= df[df["Term"]=="Limit"].index.values[0]
            df["En. Ion."]=df.iloc[index]["Level (eV)"]
            return [df]+readlevels(elem,ion1+1,ion2)
        except pd.errors.EmptyDataError:
            return [pd.DataFrame(data=[[0,0,0]],columns=["Ek(eV)","gA(s^-1)","ritz_wl_air(nm)"] )]+readlevels(elem,ion1+1,ion2)
    else:
        return []
# Partition function calculator    
def Z(df,Tev):
    Z=0
    for i in range(len(df["g"])):
        g=float(df["g"].values[i])
        Ei=df["Level (eV)"].values[i]
        if not math.isnan(g) :
            Z+=g*np.exp(-float(Ei)/Tev)       
    return Z
# Saha equation between two different ions        
def Saha(dflev,ion1,ion2,Tev,ne):
    return Z(dflev[ion2],Tev)/Z(dflev[ion1],Tev)/ne*np.exp(-float(dflev[ion1].iloc[0]["En. Ion."])/Tev)*4.8294*10**(15)*(Tev/8.61733034e-05)**(3/2)
# Calculates LTE for each element
def fracspectrum(elem,frac,ion1,ion2,Tev,ne,fig1):
    ion1,ion2=np.int64(ion1),np.int64(ion2)
    
    #calling NIST's database
    dflevels=readlevels(elem,ion1,ion2)
    dflines=pd.concat(readlines(elem,ion1,ion2),axis=0,keys=[*range(ion1,ion2+1)])
    
    #applying LTE conditions to ion concentrations
    xrel=[Saha(dflevels,i,i+1,Tev,ne) for i in range(ion1,ion2)]
    xpar=[0]
    for j in range(ion2-ion1+1):
        xpar.append((1-np.sum(xpar))/(1+np.sum([np.prod(xrel[0+j:i]) for i in range(1+j,len(xrel)+1) ]) )   )

    #plot parameters
    linf=200 
    lsup=1200
    wid=1000
    # Intensity values according to boltzmann distribution
    I= frac*dflines.loc[:]["gA(s^-1)"]*np.exp(-dflines.loc[:]["Ek(eV)"]/Tev)/[Z(dflevels[i],Tev) for i in dflines.index.codes[0]]*[xpar[i+1] for i in dflines.index.codes[0] ]
    
    fig = go.Figure()
    for j in range(ion1,ion2+1):
        try:
            y=_NGauss(np.linspace(linf,lsup,10000),I.loc[j].values,dflines.loc[j]["ritz_wl_air(nm)"].values,wid)
            fig.add_trace(go.Scatter(x=np.linspace(linf,lsup,10000),y= y ,mode="lines",name=str(elem)+" "+str(j) ) )
            fig1.add_trace(go.Scatter(x=np.linspace(linf,lsup,10000),y= y ,mode="lines",name=str(elem)+" "+str(j) ) )
        except KeyError:
            continue
    fig.add_trace(go.Scatter(x=np.linspace(linf,lsup,10000),y=_NGauss(np.linspace(linf,lsup,10000),I.values,dflines["ritz_wl_air(nm)"].values,wid) ,mode="lines",name=str(elem)+" total" ) )
    fig.update_layout(xaxis_range=[linf,lsup])
    pltconfig(fig,elem)
    return [dflines["ritz_wl_air(nm)"], I]
# Calls LTE spectra for element mixtures
def spectrum(df,Tev,ne):
    l=[]
    fig1=go.Figure()
    for i in df.columns:
        aux=fracspectrum(i,*df[i].values,Tev,ne,fig1)
        l.append(aux)
  
    pltconfig(fig1,"All")
    linf=200
    lsup=1200
    wid=1000
    Isum=0
    for i in range(len(l)):
        Isum+= _NGauss(np.linspace(linf,lsup,50000),l[i][1].values,l[i][0].values,wid)   
    fig1.add_trace(go.Scatter(x=np.linspace(linf,lsup,50000),y= Isum ,mode="lines",name=" total" ))
    pltconfig(fig1,"Summed")

#example:
#df=pd.DataFrame(data=[])
#df["Zn"]=[0.3,0,2]
#df["Cu"]=[0.7,0,2]
#spectrum(df,1,1e+17)
