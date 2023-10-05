import requests
from bs4 import BeautifulSoup
from rich import print
import re
#RASPAÇÃO
def removeRetornaFloat(caractere):
    if ',' in caractere:
        caractere = caractere.replace(',', '.')
        caractere = "".join(filter(removeRetornaFloat, caractere))
        caractere = float(caractere)
    return caractere

# Perguntar Ação
def escolhaAcao():
    global sigla
    sigla = input('Digite o TICKET da ação que você quer analisar: ')
    sigla = sigla.upper()
    site = 'https://investidor10.com.br/acoes/' + sigla
    return site

site = escolhaAcao()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(site, headers=headers)
print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')

indicadores = []

indicadores_elementos = soup.find_all('div', class_='cell')
preço = soup.find('div', class_='_card cotacao')
preço = re.sub(r'[^0-9.,]', '',preço.text)
preço = removeRetornaFloat(preço)
print(f'R$ {preço}')
lista_valor = []
lista_nomes = []
for elemento in indicadores_elementos:
    valor = elemento.find('div', class_='value d-flex justify-content-between align-items-center')
    if valor:
        valor = re.sub(r'[^0-9.,]', '',valor.text)
        lista_valor.append(valor)
        

for elemento in indicadores_elementos:
    texto = elemento.find('span', class_='d-flex justify-content-between align-items-center')
    if texto:
        lista_nomes.append(texto.text)


dicionario = {}

for nome, valor in zip(lista_nomes,lista_valor):
    dicionario[nome] = valor

verde = 0
vermelho = 0
amarelo = 0

for nome, valor in dicionario.items():
        valor =removeRetornaFloat(valor)
        if nome == 'P/L ':
            if valor <= 10:
                print(f'{nome}: [green reverse]{valor}[/]')
                verde = verde + 1
            else:
                print(f'{nome}: [red reverse]{valor}[/]')
                vermelho = vermelho + 1 
        if nome == 'P/RECEITA (PSR) ':
            if valor <= 1:
                print(f'{nome}: [green reverse]{valor}[/]')
                verde = verde + 1
            else:
                print(f'{nome}: [red reverse]{valor}[/]')
                vermelho = vermelho + 1 
        if nome == 'P/VP ':
            if valor <= 1:
                print(f'{nome}: [green reverse]{valor}[/]')
                verde = verde + 1
            else:
                print(f'{nome}: [red reverse]{valor}[/]')
                vermelho = vermelho + 1 
        if nome == f'DIVIDEND YIELD - {sigla} ':
            if valor < 6:
                print(f'{nome}: [red reverse]{valor}%[/]')
                vermelho = vermelho + 1 
            elif valor > 6 and valor < 12:
                print(f'{nome}: [yellow reverse]{valor}%[/]')
                amarelo = amarelo + 1
            else:
                print(f'{nome}: [green reverse]{valor}%[/]')   
                verde = verde + 1 
        if nome == 'PAYOUT ':
            if valor > 50 and valor < 80:
                print(f'{nome}: [green reverse]{valor}%[/]')
                verde = verde + 1
            else:
                print(f'{nome}: [red reverse]{valor}%[/]')  
                vermelho = vermelho + 1 
        if nome == 'MARGEM LÍQUIDA ':
            if valor > 20:
                print(f'{nome}: [green reverse]{valor}%[/]')
                verde = verde + 1
            elif valor > 10 and valor < 19:
                print(f'{nome}: [yellow reverse]{valor}%[/]')
                amarelo = amarelo + 1
            else:
                print(f'{nome}: [red reverse]{valor}%[/]')
                vermelho = vermelho + 1 
        if nome == 'MARGEM BRUTA ':
            if valor > 20:
                print(f'{nome}: [green reverse]{valor}%[/]')
                verde = verde + 1
            elif valor > 10 and valor < 19:
                print(f'{nome}: [yellow reverse]{valor}%[/]')
                amarelo = amarelo + 1
            else:
                print(f'{nome}: [red reverse]{valor}%[/]')
                vermelho = vermelho + 1 
        if nome == 'VPA ':
            if valor > preço * 0.85 and valor < preço * 1.15:
                print(f'{nome}: [green reverse]{valor}[/]')
                verde = verde + 1
            elif valor > preço * 0.75 and valor < preço * 0.84 or  valor > preço * 1.16 and valor < preço * 1.25 :
                print(f'{nome}: [yellow reverse]{valor}[/]')
                amarelo = amarelo + 1
            else:
                print(f'{nome}: [red reverse]{valor}[/]')
                vermelho = vermelho + 1 
        if nome == 'ROE ':
                if valor > 15:
                    print(f'{nome}: [green reverse]{valor}%[/]')
                    verde = verde + 1
                elif valor >= 10:
                    print(f'{nome}: [yellow reverse]{valor}%[/]')
                    amarelo = amarelo + 1
                else:
                    print(f'{nome}: [red reverse]{valor}%[/]')  
                    vermelho = vermelho + 1   
print('[reverse] MEDIDOR [/]')
print('[green reverse] |[/]'* verde)
print('[yellow reverse] |[/]'* amarelo)
print('[red reverse] |[/]'* vermelho)