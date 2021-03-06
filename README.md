# LTE spectra simulator for LIBS spectroscopy

Produced by Rafael de Queiroz Garcia

**About**

Code for webscrapping NIST's current database for non-commercial offline uses, more specifically using the scraped data to build LTE spectra, widely used in LIBS spectroscopy analysis. The simulated values all reproduce what is simulated at the already well-stablished NIST's LIBS Database [1]. NIST does not have any responsibility over the use of the codes within this project or the copies that they produce, which were solely developed by the author of this project. Furthermore, the author does not have any asssociation with NIST.

It is noteworthy that having all the Atomic Spectra Database [1] information available offline allows one to also explore it for a lot of other uses, not only for building LTE Spectra. Gathering also information from other databases allows further or complementary applications in spectroscopy simulations, and in the future the author may expand the scraping routines to embrace other databases. Although these scraping routines do not have a huge complexity, it may save some time for the ones who never worked with scraping.

# Scraping routines

- Eenergy_levels.py routine
- Emission_lines.py routine

Both use a very straightforward scraping method, and rely on the scrapy library [2] and also the periodictable library [3]. One should install both libraries to use these codes. If one just wants to install scrapy, it will be necessary to deal with some exceptions envolving some elements in another way. There are also other free scraping libraries which could be used, like Selenium and Beautiful Soup.

# LTE simulator

- LTE.py

Reads the offline stored data provided by the other routines and performs LTE calculations. The calculations show agreement with other sources at all tested cases. For now, all the spectrum plots were made with the plotly library [4] and were also made in a very simple way. So, maybe the code will be updated to improve the data representation in the future. It may also be improved for increasing performance with elements with a great amount of emission lines.

Every feedback would be great to increase my programming skills. I hope you find good use of this code.

**References**

[1] - Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team (2019). NIST Atomic Spectra Database (version 5.7.1), [Online]. Available: https://physics.nist.gov/asd [Mon Jun 08 2020]. National Institute of Standards and Technology, Gaithersburg, MD. DOI: https://doi.org/10.18434/T4W30F

[2] - Scrapy. Available at: https://scrapy.org/ 

[3] - Kienzle, P. A. 2017. “Periodictable V1.5.0.” doi:10.5281/zenodo.840347

[4] -  Plotly Technologies Inc. Title: Collaborative data science Publisher: Plotly Technologies Inc. Place of publication: Montréal, QC Date of publication: 2015 URL: https://plot.ly
