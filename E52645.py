import requests
from bs4 import BeautifulSoup
import urllib3
import re  # Para usar expressões regulares na limpeza do texto

# Desabilitar o aviso de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de impressoras e setores
impressoras = {
    "ALMOXARIFADO": "https://10.11.120.45/",
    "CENTRO CIRURGICO - POSTO": "https://10.11.121.70/",
    "CTI": "https://10.11.121.55/",
    "HEMODINAMICA RECEPÇÃO": "https://10.11.121.64/",
    "LABORATORIO - RECEPÇÃO": "https://10.11.132.7/",
    "MANUTENCAO COORDENAÇÃO": "https://10.11.120.44/",
    "NEO/PED - POSTO": "https://10.11.122.68/",
    "SAD - POSTO": "https://10.11.121.58/",
    "POSTO - 2 ANDAR": "https://10.11.122.70/",
    "POSTO - 3 ANDAR": "https://10.11.123.50/",
    "POSTO - 4 ANDAR": "https://10.11.123.160/",
    "P.A POSTO DE ENFERMAGEM": "https://10.11.120.35/",
    "P.A SALA DE MEDICAÇÃO": "https://10.11.120.55/",
    "P.A RECEPÇÃO": "https://10.11.120.66/"
}

# Lista para armazenar impressoras com nível de toner baixo
alertas_toner_baixo = []

# Função para obter o nível de toner de uma impressora
def obter_nivel_toner(setor, url):
    try:
        # Adicionando timeout de 5 segundos
        response = requests.get(url, verify=False, timeout=5)
        # Verificando se o acesso foi bem-sucedido
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Encontrar o elemento específico do nível de toner
            toner_level_text = soup.find('span', id='SupplyPLR0').text
            # Removendo caracteres não numéricos usando regex
            toner_level_clean = re.sub(r'[^0-9]', '', toner_level_text)
            
            # Convertendo para inteiro
            if toner_level_clean:
                toner_level = int(toner_level_clean)
                print(f"Setor: {setor}, Nível do toner: {toner_level}%")

                # Verificando se o toner está abaixo de 12%
                if toner_level < 21:
                    alertas_toner_baixo.append(f"ALERTA: O nível de toner da impressora no setor {setor} está abaixo de 12%!")
            else:
                print(f"Setor: {setor}, Não foi possível determinar o nível de toner. Texto obtido: {toner_level_text}")
        else:
            print(f"Setor: {setor}, Falha ao acessar o site. Status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Setor: {setor}, Timeout ao tentar acessar o site.")
    except Exception as e:
        print(f"Setor: {setor}, Ocorreu um erro: {e}")

# Iterar sobre cada impressora e obter o nível de toner
for setor, url in impressoras.items():
    obter_nivel_toner(setor, url)

# Imprimir alertas de toner baixo no final
if alertas_toner_baixo:
    print("\n=== ALERTAS DE TONER BAIXO ===")
    for alerta in alertas_toner_baixo:
        print(alerta)
else:
    print("\nTodas as impressoras têm toner acima de 12%.")
