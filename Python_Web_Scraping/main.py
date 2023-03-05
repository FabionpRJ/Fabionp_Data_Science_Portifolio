from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By


#PASSO 0: Montando o Setup
options= webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
navegador = webdriver.Chrome(options=options)
lista_whiskys = []
count = 0
num_whisky = 0
#PASSO 1: Entrar no navegador
navegador.get('https://www.amazon.com.br/')


#Passo 2: Pesquisar uma lista de whiskys 
elem = navegador.find_element('xpath','//*[@id="twotabsearchtextbox"]')
elem.click()
elem.send_keys('Whisky')
elem.submit()

while count < 4:
    sleep(2)

    #Passo 3: Transformar a página web em BeautifulSoup
    web_page = BeautifulSoup(navegador.page_source, 'html.parser')

    #Passo 4: Encontrar o HTML comum à todos os whiskys
    Whiskys = web_page.findAll('div',attrs={'class':'a-section a-spacing-base'})
   

    for whisky in Whiskys:
        num_whisky +=1
        #Encontrando o título
        titulo = whisky.find('h2',attrs={'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})
        print(f'Titulo: {titulo.text}')

        #Encontrando a Avaliação
        avaliacao = whisky.find('span', attrs={'class':'a-size-base'})
        print(f'Avaliacao: {avaliacao.text}')
        #Encontrando o Preço
        #Encontrando o Preço
        valor_inteiro = whisky.find('span', attrs={'class':'a-price-whole'})
        valor_fracao = whisky.find('span', attrs={'class':'a-price-fraction'})

        



        if valor_inteiro is not None:
            valor_inteiro = valor_inteiro.text
        else:
            valor_inteiro = '0'

        if valor_fracao is not None:
            valor_fracao = valor_fracao.text
        else:
            valor_fracao = '00'

        valor_total = valor_inteiro + valor_fracao




        print(f'Valor: {valor_total}')


        #Encontrando o Link
        link = whisky.find('a',attrs={'class':'a-link-normal s-no-outline'})

        
        print(f'NumWhisky: ',num_whisky)
        print('\n\n')
        

        lista_whiskys.append([titulo.text, avaliacao.text, valor_total, link['href']])



    sleep(2)

    proxima_pagina = ', página '+ str(count+2)
    elem = navegador.find_element(By.CSS_SELECTOR, '[aria-label = "Ir para a próxima página' + proxima_pagina + '"]')
    elem.click()
    count +=1


tabela = pd.DataFrame(lista_whiskys, columns=['Titulo','Avaliação','Valor','link'])
tabela.to_excel('whiskys.xlsx', index=False)
