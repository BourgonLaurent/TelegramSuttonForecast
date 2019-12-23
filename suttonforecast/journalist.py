# Journalist bot
## Gets the information
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import os.path

class Journalist:
    def __init__(self):
        self.createDictionnaries()
        condition_de_ski_soup = self.getPageSoup(r"https://montsutton.com/la-montagne/conditions-de-ski/")
        statut_soup = self.getPageSoup(r"https://montsutton.com/la-montagne/conditions-de-ski/domaine-skiable-ouvert/")
        self.processConditionsDeSki(condition_de_ski_soup)
        self.processStatut(statut_soup)
    
    def createDictionnaries(self):
        self.data = dict()
        self.data["info_time"] = str()

        self.data["conditions"] = dict()
        self.data["conditions"]["surface"] = str()
        self.data["conditions"]["base"] = str()
        self.data["conditions"]["couverture"] = str()
        self.data["conditions"]["message"] = str()

        self.data["pistes"] = dict()
        self.data["remontees"] = dict()
        self.data["chalets"] = dict()

        for d in (self.data["pistes"], self.data["remontees"], self.data["chalets"]):
            d["ouvert"] = int()
            d["index"] = int()
            d["statut"] = dict()
            d["statut"]["ouvert"] = list()
            d["statut"]["ferme"] = list()

    def getPageSoup(self, url):
        page = uReq(url)
        soup = BeautifulSoup(page, "html.parser")
        return soup
    
    def processConditionsDeSki(self, soup):
        self.data["info_time"] = soup.find("section", attrs={"class":"icon_section bg-grey-light"}).h5.text.strip()
        
        self.data["pistes"]["ouvert"], self.data["pistes"]["index"] = soup.find_all("div", attrs={"class":"first_icon_block"})[0].h3.text.strip().split("/")
        self.data["remontees"]["ouvert"], self.data["remontees"]["index"] = soup.find_all("div", attrs={"class":"icon_block"})[0].h3.text.strip().split("/")
        self.data["chalets"]["ouvert"], self.data["chalets"]["index"] = soup.find_all("div", attrs={"class":"icon_block"})[1].h3.text.strip().split("/")
        
        self.data["conditions"]["surface"], self.data["conditions"]["base"], self.data["conditions"]["couverture"] = [info.text.strip() for info in soup.find("div", attrs={"class":"surface"}).findAll("p")]
        self.data["conditions"]["message"] = soup.find("div", attrs={"class":"_1aa6"}).find("div", attrs={"class":""}).text.strip().replace(u"\xa0","").replace("\n","")

    def processStatut(self, soup):
        for i, table in enumerate(soup.find_all("table")):
            if i == 0:
                dictionnary = self.data["pistes"]
            elif i == 1:
                dictionnary = self.data["remontees"]
            else:
                dictionnary = self.data["chalets"]

            trows = table.find_all("tr")
            trows.pop(0)  # Remove header

            for table_row in trows:
                if i == 0:
                    if "ouvert" in table_row.find_all("td")[4].text.lower():
                        dictionnary["statut"]["ouvert"].append(table_row.find_all("td")[0].text.strip() + ". " + table_row.find_all("td")[1].text.strip())
                    else:
                        dictionnary["statut"]["ferme"].append(table_row.find_all("td")[0].text.strip() + ". " + table_row.find_all("td")[1].text.strip())
                else:
                    if "ouvert" in table_row.find_all("td")[2].text.lower():
                        dictionnary["statut"]["ouvert"].append(table_row.find_all("td")[0].text.strip())
                    else:
                        dictionnary["statut"]["ferme"].append(table_row.find_all("td")[0].text.strip())