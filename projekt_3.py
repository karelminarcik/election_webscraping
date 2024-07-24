import requests
import sys
import csv
from bs4 import BeautifulSoup


"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Karel Minarčík

email: k.minarcik@seznam.cz

discord: Karel Minarčík | karlos9957

"""

def kraj_number(url_address):
    """ 
    Extracts the region number from the provided URL address.

    Args:
        url_address (str): The URL address containing the region number.

    Returns:
        str: The region number extracted from the URL address.
    """
    number = url_address[-16:-14]
    if "=" in number:
        number = number.replace("=", "")
    return number


def send_request_get(url):
    """
    Sends a GET request to the provided URL and returns the response text and URL.

    Args:
        url (str): The URL to which the GET request is sent.

    Returns:
        tuple: A tuple containing the response text and the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, url
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        sys.exit(1)


def parse_response(response, url):
    """
    Parses the HTML response using BeautifulSoup.

    Args:
        response (str): The HTML response to be parsed.
        url (str): The URL of the response.

    Returns:
        tuple: A tuple containing the BeautifulSoup object and the URL.
    """
    soup = BeautifulSoup(response, "html.parser")
    return soup, url


def get_cityname_and_citycode(kod_obce_html, nazev_obce_html):
    """
    Extracts lists of municipality codes and names from the provided HTML elements.

    Args:
        kod_obce_html (ResultSet): A BeautifulSoup ResultSet containing HTML elements with municipality codes.
        nazev_obce_html (ResultSet): A BeautifulSoup ResultSet containing HTML elements with municipality names.

    Returns:
        tuple: A tuple containing two lists - one with municipality codes and another with municipality names.
    """
    kod_obce_list = [kod_obce.getText() for kod_obce in kod_obce_html]
    nazev_obce_list = [nazev_obce.getText() for nazev_obce in nazev_obce_html]
    return kod_obce_list, nazev_obce_list


def get_overall_election_numbers(obec_soup):
    """
    Extracts overall election numbers from the municipality soup object.

    Args:
        obec_soup (BeautifulSoup): The BeautifulSoup object of the municipality page.

    Returns:
        tuple: A tuple containing the number of voters, issued envelopes, and valid votes.
    """
    volici_v_seznamu = obec_soup.select_one("td:nth-child(4)").text.replace('\xa0', '')
    vydane_obalky = obec_soup.select_one("td:nth-child(5)").text.replace('\xa0', '')
    platne_hlasy = obec_soup.select_one("td:nth-child(8)").text.replace('\xa0', '')
    return volici_v_seznamu, vydane_obalky, platne_hlasy


def get_party_numbers(obec_soup):
    """
    Extracts the vote counts for political parties from the municipality soup object.

    Args:
        obec_soup (BeautifulSoup): The BeautifulSoup object of the municipality page.

    Returns:
        tuple: A tuple containing a list of vote counts for political parties and a list of political party names.
    """
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
        pocty1 = [pocet.text.strip().replace('\xa0', '') for pocet in pocet_html_1] if pocet_html_1 else []

        # Data from second table
        pocet_html_2 = tabulka.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
        pocty2 = [pocet.text.strip().replace('\xa0', '') for pocet in pocet_html_2] if pocet_html_2 else []

        pocty_ze_dvou_tabulek.extend(pocty1)
        pocty_ze_dvou_tabulek.extend(pocty2)

    return pocty_ze_dvou_tabulek, strany_ze_dvou_tabulek


def scrap_data(soup, url):
    """
    Scrapes election data from the provided soup object and URL.

    This function extracts municipality codes and names, election statistics,
    and political party vote counts from the HTML soup object representing a 
    webpage with election data. It constructs a list of data records and a list 
    of political party names.

    Args:
        soup (BeautifulSoup): Parsed HTML soup object containing the main page with municipality data.
        url (str): The URL of the main page being scraped.

    Returns:
        tuple: A tuple containing two elements:
            - data_list (list of lists): A list where each element is a list of data points 
              for a specific municipality, including its code, name, voter statistics, and 
              vote counts for political parties.
            - strany_ze_dvou_tabulek (list): A list of political party names encountered 
              during the scraping process.
    """
    print(f"Downloading data from inserted URL address: {url}")
    
    kod_kraje = url[-4:]
    kod_obce_html = soup.find_all(name="td", class_="cislo")
    nazev_obce_html = soup.find_all(name="td", class_= "overflow_name") 
    data_list = []

    kod_obce_list, nazev_obce_list = get_cityname_and_citycode(kod_obce_html, nazev_obce_html)

    for kod_obce, nazev_obce in zip(kod_obce_list, nazev_obce_list):
        url_obec = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj_number(url)}&xobec={kod_obce}&xvyber={kod_kraje}"
        
        response_obec, _ = send_request_get(url_obec)
        obec_soup, _ = parse_response(response_obec, url_obec)

        # Data with election numbers - overall
        volici_v_seznamu, vydane_obalky, platne_hlasy = get_overall_election_numbers(obec_soup)

        # Data with parties numbers
        pocty_ze_dvou_tabulek, strany_ze_dvou_tabulek = get_party_numbers(obec_soup)

        # Get all data to one list
        data = [kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy]
        data.extend(pocty_ze_dvou_tabulek)
        data = [str(value) for value in data]

        data_list.append(data)

    print("Data was downloaded properly.")
    return data_list, strany_ze_dvou_tabulek


def write_data_into_file(strany, data_list, file_name):
    """
    Writes the scraped data into a CSV file.

    Args:
        strany (list): A list of political party names.
        data_list (list of lists): A list where each element is a list of data points 
                                   for a specific municipality.
        file_name (str): The name of the file (without extension) to save the data.

    Returns:
        None
    """
    csv_file_path = f"{file_name}.csv"
    # Define the header
    header = ["Kód", "Obec", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    header.extend(strany)

    # Write data to the csv file
    with open(csv_file_path, mode="w", newline='', encoding='utf-8') as new_csv:
        writer = csv.writer(new_csv)
        writer.writerow(header)
        writer.writerows(data_list)

    

    print(f"Data has been written to {csv_file_path}")  


def scrap_the_web(url):
    """
    Scrapes the web for election data from the provided URL.

    Args:
        url (str): The URL of the main page to be scraped.

    Returns:
        tuple: A tuple containing two elements:
            - strany (list): A list of political party names encountered during the scraping process.
            - data_list (list of lists): A list where each element is a list of data points 
                                         for a specific municipality.
    """
    response, url = send_request_get(url)
    soup, url = parse_response(response, url)
    data_list, strany = scrap_data(soup, url)
    return strany, data_list


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python projekt_3.py <URL> <output_file_name>")
        sys.exit(1)

    url = sys.argv[1]
    file_name = sys.argv[2]

    strany, data_list = scrap_the_web(url)
    write_data_into_file(strany, data_list, file_name)
