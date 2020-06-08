import scrapy
import unicodedata #https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
import pandas as pd
from periodictable import *
class QuotesSpider(scrapy.Spider):
    name = "lines"
    # reads desired inputs
    Z,lowerwl,upperwl=input("Z, lowerwl, upperwl:").split(", ")
    Z=int(Z)
    element=str(elements[Z])
    # building the links that will be scrapped
    lista=[]
    for i in range(0,4):
        teil1='https://physics.nist.gov/cgi-bin/ASD/lines1.pl?spectra='+element+' '
        teil2='&limits_type=0&low_w='+lowerwl+'&upp_w='+upperwl+'&unit=1&submit=Retrieve+Data&de=0&format=3&line_out=0&remove_js=on&en_unit=1&output=0&bibrefs=1&page_size=15&show_obs_wl=1&show_calc_wl=1&unc_out=1&order_out=0&max_low_enrg=&show_av=2&max_upp_enrg=&tsb_value=0&min_str=&A_out=1&f_out=on&S_out=on&intens_out=on&max_str=&allowed_out=1&forbid_out=1&min_accur=&min_intens=&conf_out=on&term_out=on&enrg_out=on&J_out=on&g_out=on'
        if i<Z:
            lista.append(teil1+str(i)+teil2)
            
    start_urls =lista
    
    def parse(self, response):
        element=self.element
        file=open('/home/reiher/Documents/Pesquisa, extensão e material extra/LIBS/Simulando espectros/dadosNIST/linhas_emissao/'+element+' '+str(response.url[58+len(element)])+'.csv','w')
        table = response.xpath('/html/body/p/text()').get()
        table = [x.split('\t') for x in table.split('\n')]
        for i in range(len(table)):
            for j in range(len(table[i])):
                table[i][j]=table[i][j].replace("\"","")                
        df = pd.DataFrame(data=table[1:],columns=table[0])
        
        if element=="H":
            df.drop([df['term_k'].index[i] for i in df['term_k'].index if df['term_k'].values[i]!=''   ],axis=0,inplace=True) 
        
        df.to_csv(file)    
                        
        file.close()
