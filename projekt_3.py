import requests
from bs4 import BeautifulSoup
from openpyxl.workbook import Workbook
import sys

"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Karel Minarčík

email: k.minarcik@seznam.cz

discord: Karel Minarčík | karlos9957

"""
def kraj_number(url_address):
    """ Ziska cislo kraje, ktere se nachazi za 'kraj=' v url adrese.

    Args:
        url_address (_str_): url adresa okrsku

    Returns:
        str : vraci cislo kraje
    """
    number = url_address[-16:-14]
    if "=" in number:
        number = number.replace("=", "")
        return number
    else:
        return number
        

def scrap_the_web(url, file_name):
    """_summary_

    Args:
        url (string): url adresa okrsku
        file_name (string): nazev souboru, do ktereho se maji vysledna data ulozit(bez pripony)
    """
    
    response = requests.get(url)
    web_html = response.text

    soup = BeautifulSoup(web_html, "html.parser")
    
    print(f"Downloading data from inserted URL address:{url}")

    # Getting codes and name of municipality
    kod_kraje = url[-4:]
    kod_obce_html = soup.find_all(name="td", class_="cislo")
    nazev_obce_html = soup.find_all(name="td", class_= "overflow_name") 
    data_list = []

    for kod_obce, nazev_obce in zip(kod_obce_html, nazev_obce_html):
        # gain code of the particular municipality
        kod_obce = kod_obce.getText()
        nazev_obce = nazev_obce.getText()
        
        url_obec = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj_number(url)}&xobec={kod_obce}&xvyber={kod_kraje}"
        response_obec = requests.get(url_obec)
        obec_html = response_obec.text
        obec_soup = BeautifulSoup(obec_html, "html.parser")
        
        # Data with election numbers - overall
        volici_v_seznamu = obec_soup.select_one("td:nth-child(4)").text
        vydane_obalky = obec_soup.select_one("td:nth-child(5)").text
        platne_hlasy = obec_soup.select_one("td:nth-child(8)").text
        
        # Data wit parties numbers
        pocty_ze_dvou_tabulek = []
        strany_ze_dvou_tabulek = []
        hlasovani_page = obec_soup.find(id="inner")
        tablulky_strana = hlasovani_page.find_all(name="div", class_="t2_470")
        
        for tabulka in tablulky_strana:
            # Names of political parties
            strany_html = tabulka.find_all(name="td", class_="overflow_name")
            strany = [strana.text.strip() for strana in strany_html]
            strany_ze_dvou_tabulek.extend(strany)
            
            # Data from first table
            pocet_html_1 = tabulka.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
            if pocet_html_1:  # Check if the list is not empty
                pocty1 = [pocet.text.strip() for pocet in pocet_html_1]
                
            # Data from second table
            pocet_html_2 = tabulka.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
            if pocet_html_2:  # Check if the list is not empty
                pocty2 = [pocet.text.strip() for pocet in pocet_html_2]
                
        # Data from both tables
        pocty_ze_dvou_tabulek = pocty1+pocty2
        
        # Get all data to the one list
        data = [kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy]
        data.extend(pocty_ze_dvou_tabulek)
        
        # Create a list which will contain all data lists 
        data_list.append(data)
        
        
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Define the header
    header = ["Kód", "Obec", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    header.extend(strany_ze_dvou_tabulek)

    # Write the header row to the worksheet
    ws.append(header)

    # Write the data to the worksheet
    for row in data_list:
        ws.append(row)

    # Save the workbook
    excel_file_path = f"{file_name}.csv"
    wb.save(excel_file_path)

    print(f"Data has been written to {excel_file_path}")
    print("The program is terminated")


def main():
    if len(sys.argv) != 3:
        print("Pouziti: python projekt_3.py <url> <nazev_souboru>")
        sys.exit(1)

    url = sys.argv[1]
    file_name = sys.argv[2]

    scrap_the_web(url, file_name)

if __name__ == '__main__':
    main()






