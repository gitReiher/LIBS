import scrapy
import pandas as pd
from periodictable import *

class QuotesSpider(scrapy.Spider):
    name = "niveis"
    # Reads desired atomic number
    Z=int(input("Atomic Number: ") )
    # translates Z into the element symbol
    element=str(elements[Z])
    l=[]
    # builds a list of links to scrap
    for i in range(4):
        if i<Z: 
            l.append('https://physics.nist.gov/cgi-bin/ASD/energy1.pl?encodedlist=XXT2&de=0&spectrum='+element+"+"+str(i)+'&submit=Retrieve+Data&units=1&format=3&output=0&page_size=15&multiplet_ordered=0&conf_out=on&term_out=on&level_out=on&unc_out=1&j_out=on&g_out=on&lande_out=on&perc_out=on&biblio=on&temp=')
        else:
            break
    start_urls =l

    def parse(self, response):
        element=self.element
        Z=self.Z
        #opens file to save the data
        file=open('/home/reiher/Documents/Pesquisa, extensão e material extra/LIBS/Simulando espectros/dadosNIST/niveis_energia/'+elemento+" "+str(response.url[80+len(elemento)])+'.csv','w')
        
        table = response.xpath('/html/body/p/text()').get()
        table= table.replace("\"","")
        table = [x.split('\t') for x in table.split('\n') ]
        df = pd.DataFrame(data=table[1:],columns=table[0])
        print(df.columns)
        
        # exceptions envolving partition functions
        if Z==1:
            df.drop([df['Configuration'].index[i] for i in df['Configuration'].index[1:-1] if not df['Configuration'].values[i].isnumeric()   ],axis=0,inplace=True)   
        if Z==int(response.url[80+len(element)])+1:
            dfz= pd.DataFrame(columns=df.columns,index=[0])
            dfz['Level (eV)']=0
            dfz['g']=1
            dfz['Term']='Limit'
            dfz.to_csv('/home/reiher/Documents/Pesquisa, extensão e material extra/LIBS/Simulando espectros/dadosNIST/niveis_energia/'+elemento+" "+str(Z)+'.csv')    
        print(df)
        df.to_csv(file)    
                        
        file.close()
