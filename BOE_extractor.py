import requests, csv
from bs4 import BeautifulSoup

ano_inicial = 1966
i = 1
dif_i = 1
dif = 1000

def saveincsv(url, titulo, textos, ano):

    filename = "indultos-" + str(ano) + ".csv"
    dataset = open(filename, "a+")
    data = url + "|" + titulo + "|" + textos + "|" +  str(ano) + "\n"
    dataset.write(data)
    dataset.close()

def get_xml(url):

    #url = 'https://www.boe.es/diario_boe/xml.php?id=BOE-A-2021-10344'
    headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
    response = requests.get(url, headers=headers)
    return response.text

def get_titulo(XML):

    soup = BeautifulSoup(XML, "xml")
    titulo = soup.find("titulo")
    return titulo.get_text()

def get_texto(XML):
    
    textos = ""
    soup = BeautifulSoup(XML, "xml") 
    text = soup.find_all("texto")
 
    for t in text:
        textos = textos + " | " + str(t.get_text().replace("\n", ""))

    return textos

def main():
    global ano_inicial, i, dif, dif_i

    while (ano_inicial < 2021) and (i < 320001):

        url = f"https://www.boe.es/diario_boe/xml.php?id=BOE-A-{ano_inicial}-{i}"

        try:

            print(f"[>][URL] {url}")

            XML = get_xml(url)
            titulo = get_titulo(XML)
            textos = get_texto(XML)
            if textos == "":
                textos = "None"
            print(titulo)
            print(textos)
            print()

            saveincsv(url, titulo, textos, ano_inicial)
            i += 1
            

        except Exception as e:

            print (f"[>][ERROR EN LA PETICIÓN] {e}")

            dif_i += 1

            if dif_i == dif:
                ano_inicial +=1

            else:
                i += 1

main()
