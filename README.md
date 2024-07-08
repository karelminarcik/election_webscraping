# Engeto_pa-3-projekt
Treti projekt na Python akademii od Engeta

## 1. Popis projektu
Tento projekt slouzi k extrahovani vysledku voleb v roce 2017.
Odkaz k prohlednuti najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## 2. Instalace knihoven
Knihovny, ktere jsou pouzity v kodu jsou ulozene v souboru `requirements.txt`. Pro instalaci doporucuji pouzit nove virtualni prostredi a s nainstalovanym managerem spustit nasledovne:
- `pip --version`                      # overim verzi manageru
- `pip install -r requirements.txt`    # nainstalujeme knihovny

## 3. Spusteni projektu
Spusteni souboru `project_3.py` v ramci prikazoveho radku pozaduje dva povinne argumenty.
`python projekt_3.py <odkaz-uzemniho-celku>  <vysledny-soubor>`
Nasledne se Vam stahnou vysledky jako soubor s priponou .csv

## 4. Ukazka projektu 
Vysledky hlasovani pro okres Olomouc:
1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102`
jelikoz je ampersand reservovany znak
![ampersand image](/img/ampersand.png)
musime url upravit : `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ"&"xkraj=12"&"xnumnuts=7102`
2. agrument: `volby_olomouc`

### Spusteni programu: 
`python projekt_3.py https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ"&"xkraj=12"&"xnumnuts=7102 volby_olomouc`

### Prubeh stahovani:
```python
Downloading data from inserted URL address:https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102      
Data has been written to output.csv
The program is terminated
```

### Castecny vystup:
```python
['500623', 'Bílá Lhota', '931', '568', '565', '31', '0', '0', '42', '0', '20', '73', '4', '6', '6', '0', '5', '53', '2', '12', '164', '0', '0', '62', '0', '0', '3', '1', '81', '0']
['552062', 'Bílsko', '172', '119', '119', '8', '0', '1', '11', '0', '7', '3', '1', '1', '0', '1', '0', '12', '0', '1', '27', '0', '0', '25', '0', '0', '1', '0', '20', '0']
['500801', 'Blatec', '497', '320', '319', '21', '0', '0', '28', '0', '19', '26', '7', '1', '3', '0', '0', '25', '0', '7', '110', '0', '1', '26', '0', '1', '0', '0', '43', '1']
```

