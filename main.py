from urllib.request import urlopen
from bs4 import BeautifulSoup
from re import compile
import pandas as pd


def read_html(url):
    response = urlopen(url)
    return response.read()


def find_links(html):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('ul', id='listTwo').find_all('a')
    for link in table:
        links.append(link.get('href'))
    return links


def read_page(html, url):
    prop = {}
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all('tr')

    # Nome
    print(trs[0])
    print('----------------------------------------------')
    prop['Nome'] = trs[0].find(
        'h1', class_='article-title').get_text(strip=True)
    # Categoria
    print(trs[1])
    print('----------------------------------------------')
    prop['Categoria'] = trs[1].find_next(
        'td').find_next('td').get_text(strip=True)
    # Codice alimento
    print(trs[2])
    print('----------------------------------------------')
    try:
        prop['CodiceAlimento'] = int(trs[2].find_next(
            'td').find_next('td').get_text(strip=True))
    except ValueError:
        prop['CodiceAlimento'] = trs[2].find_next(
            'td').find_next('td').get_text(strip=True)
    # ## Nome scientifico
    # print(trs[3])
    # print('----------------------------------------------')
    # prop['NomeScientifico'] = trs[3].find_next('td').find_next('td').get_text(strip=True)
    # ## Nome inglese
    # print(trs[4])
    # print('----------------------------------------------')
    # prop['NomeInglese'] = trs[4].find_next('td').find_next('td').get_text(strip=True)
    # Link
    prop['Link'] = url
    # Proprieta varie
    trs = soup.find_all('tr', class_=compile('corpo'))

    for tr in trs:
        print(tr)
        print('----------------------------------------------')
        if tr['class'][0] == 'corporicetta':
            continue
        titolo = tr.find_next('td').get_text(strip=True)
        valore = 0
        try:
            valore = float(tr.find_next('td').find_next('td').find_next(
                'td').get_text(strip=True).replace("<", ""))
        except ValueError:
            valore = tr.find_next('td').find_next('td').find_next(
                'td').get_text(strip=True).replace("<", "")
        prop[titolo] = valore

    return prop


def test_read_page(url):
    html = read_html(url)
    try:
        res.append(read_page(html, url))
    except Exception:
        print(f'{Exception} - Erorr on url -> {url}')
        breakpoint()
        pass


if __name__ == '__main__':
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    res = []
    html = read_html(
        "https://www.alimentinutrizione.it/tabelle-nutrizionali/ricerca-per-ordine-alfabetico")
    links = find_links(html)
    for link in links:
        url = f'https://www.alimentinutrizione.it{link}'
        print(url)
        html = read_html(url)
        try:
            res.append(read_page(html, url))
        except Exception:
            print(f'{Exception} - Erorr on url -> {url}')
            breakpoint()
            continue

    # url = 'https://www.alimentinutrizione.it/tabelle-nutrizionali/000872'
    # test_read_page(url)

    df = pd.DataFrame(res)
    df.fillna(0, inplace=True)
    df.to_excel('test.xlsx')
