import requests, csv
from bs4 import BeautifulSoup
from pymongo import MongoClient

ano_inicial = 2008 #2807
i = 1
dif_i = 1
dif = 1000

#Conexión con la base de datos
con = MongoClient()
db = con.DG

def insert_mongo(url, titulo, textos, ano):

	boe = db.DG_BORME.find_one({"url":url})
 
	if boe == None:
 
		db.DG_BORME.update({'url':url},{"nombre":titulo,"text":textos, "ano":ano}, True)
   
	else:
 
		print (f"[>][MONGODB] Ya está guardado previamente en mongoDB {url}")

def saveincsv(url, titulo, textos, ano):

    filename = "BORME-C-" + str(ano) + ".csv"
    dataset = open(filename, "a+")
    data = url + "|" + titulo + "|" + textos + "|" +  str(ano) + "\n"
    dataset.write(data)
    dataset.close()

def get_xml(url):

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

    while (ano_inicial < 2022) and (i < 320001):

        url = f"https://www.boe.es/diario_borme/xml.php?id=BORME-C-{ano_inicial}-{i}"

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
            insert_mongo(url, titulo, textos, ano_inicial)
            i += 1
            print(dif_i)

        except Exception as e:

            print (f"[>][ERROR EN LA PETICIÓN] {e}")

            dif_i += 1
            print (f"Nº de errores: {dif_i}")

            if dif_i >= dif:

                ano_inicial +=1
                dif_i = 0
                i = 1

            else:
                i += 1

main()
