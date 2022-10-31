from django.shortcuts import render, redirect

# Librerias Scraping
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests as r
import os

def inicio(request):
    return render(request, 'inicio.html')

def anime(request):
    if request.method == 'POST':
        anime = request.POST['nombreAnime']

        url = f'https://www3.animeflv.net/browse?q={anime}'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        paginaPrincipal = 'https://www3.animeflv.net'
        busqueda = r.get(url, headers=headers)

        print(busqueda.status_code)

        soup = bs(busqueda.text, 'html.parser')
        titulos = soup.find_all('article', class_='Anime')
        listaDic = []

        for titulo in titulos:
            a = titulo.find('a').get('href')
            img = titulo.find('img').get('src')
            b = titulo.find('h3', class_='Title')
            diccionario = dict(titulo=b.text.strip(),link=f'{paginaPrincipal}{a}',portada=img)
            listaDic.append(diccionario)
        context = {
            'datos':listaDic
        }

        return render(request, 'busqueda.html', context)
    elif request.method == 'GET':
        return render(request, 'busqueda.html')

def verAnime(request):
    paginaPrincipal = 'https://www3.animeflv.net'
    if request.method == 'POST':
        linkPagina = request.POST['linkPagina']
        imgAnime = request.POST['imagenAnime']
        tituloAnime = request.POST['tituloAnime']
        # chromeOp = Options()
        # chromeOp.headless=True
        # chromeOp.add_argument('--disable-gpu')
        # chromeOp.add_argument('--no-sandbox')
        # chromeOp.add_argument('user-agent=fake-useragent')
        # navegador = wd.Chrome(service=Service(r'C:\Users\Kevin Martínez\AppData\Local\chromedriver\chromedriver.exe'), options=chromeOp)

        chromeOp = Options()
        chromeOp.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chromeOp.headless=True
        chromeOp.add_argument('--disable-gpu')
        chromeOp.add_argument('--no-sandbox')
        chromeOp.add_argument('user-agent=fake-useragent')
        navegador = wd.Chrome(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chromeOp)


        navegador.get(linkPagina)
        paginaJs = navegador.page_source
        navegador.quit()

        soup2 = bs(paginaJs, 'html.parser')
        descripcion = soup2.find('div', class_='Description')
        descAnime = descripcion.find('p').text
        episodios = soup2.find_all('li', class_='fa-play-circle')

        enlace = []
        caps = []
        todosEp = []

        for episodio in episodios:
            cap = episodio.find('a').get('href')
            if cap != '#':
                numEp = float(cap.rsplit('-', 1)[1])
                urlEp = cap.rsplit('-', 1)[0]
                enlace.append(urlEp)
                caps.append(numEp)
        urlBase = enlace[0]
        ultimoCap = max(caps)
        for i in range(1,int(ultimoCap) + 1):
            epAnime = dict(numeroCap=i,enlaceCap=f'{paginaPrincipal}{urlBase}-{i}')
            todosEp.append(epAnime)
        todosEp2 = reversed(todosEp)
        context = {
            'capitulos':todosEp2,
            'imagen':imgAnime,
            'descripcion':descAnime,
            'titulo':tituloAnime,
        }
        return render(request,'episodios.html', context)
    else:
        return redirect('inicio')

def verCapitulo(request):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    if request.method == 'POST':
        capituloAnime = request.POST['episodioAnime']
        busqueda = r.get(capituloAnime, headers=headers)
        print(busqueda.status_code)

        soup3 = bs(busqueda.text, 'html.parser')

        # linksAnime = soup3.find_all('a', class_='fa-download')
        linksAnime = soup3.find('a', class_='fa-download')
        link = linksAnime.get('href')
        parte1 = link.rsplit('/', 1)[0]
        parte2 = link.rsplit('/', 1)[1]
        print(link)
        print(f'{parte1}/embed{parte2}')
        linkFinal = f'{parte1}/embed{parte2}'
        context = {
            'url':linkFinal
        }
        return render(request, 'visualizacion.html', context)
        # for l in linksAnime:
        #     print(l.get('href'))
