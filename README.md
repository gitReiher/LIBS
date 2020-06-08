# LIBS
LTE spectra simulator for LIBS spectroscopy

Code for webscrapping NIST's database for non-commercial uses on offline LTE spectra simulation

# Scraping routines

- levels routine
- lines routine

Both use a very straightforward scraping method, and rely on the scrapy library and also the periodictable library, for which I thank and give credit here. 

Scrapy: Kouzis-Loukas, D. (2016). Learning Scrapy. Packt Publishing Ltd.
Periodictable: Kienzle, P. A. 2017. “Periodictable V1.5.0.” doi:10.5281/zenodo.840347

One should install both libraries to use these codes. If one just wants to install scrapy, it will be necessary to deal with some exceptions envolving some elements in another way. There are also other free scraping libraries which could be used, like Selenium and Beautiful Soup

# LTE simulator

- LTE.py

Reads the offline stored data provided by the other routines and performs LTE calculations
