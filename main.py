import json
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)

url_states_and_cities = "https://pt.wikipedia.org/wiki/Lista_de_estados_brasileiros_por_n%C3%BAmero_de_munic%C3%ADpios"
url_states = "http://www.servicos.blog.br/listas/lista-de-estados-brasileiros-com-siglas-e-capitais/"

# get sigle of states
driver.get(url=url_states)
table_states_by_sigle = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/table/tbody')

table_row_states_with_sigle: [] = list()

list_of_states_names: [] = list()

for row in range(1, 29):
    # refatorar
    table_row_states_with_sigle.append(table_states_by_sigle.find_element(By.CSS_SELECTOR, f'body > div.site > div.conteudo > table > tbody > tr:nth-child({row})'))

row = 1
for element in table_row_states_with_sigle:
    if row > 1:
        state: {} = {
            "estado": "",
            "sigla": ""
        }
        estado = element.find_element(By.CSS_SELECTOR,
                                               f'body > div.site > div.conteudo > table > tbody > tr:nth-child({row}) > td:nth-child(2)').text
        if estado == 'Ceara':
            state['estado'] = 'Ceará'
        else:
            state['estado'] = estado
        state['sigla'] = element.find_element(By.CSS_SELECTOR,
                                               f'body > div.site > div.conteudo > table > tbody > tr:nth-child({row}) > td:nth-child(1)').text
        list_of_states_names.append(state)
    row += 1

# list states and cities by wikipedia
driver.get(url=url_states_and_cities)
table_row_states_and_cities: [] = list()
table_of_states_and_cities = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]/tbody')

count: int = 0
for row in range(1, 27):
    #Bloco que pega o valor de cada estado na tabela
    save_td_data: {} = {
        "posicao": "",
        "estado": "",
        "sigla": "",
        "regiao": "",
        "municipios": [],
        "habitantes_por_estado": "",
        "habitantes_por_municipio": ""
    }
    total_cities = 0
    try:
        tr_table_states_and_cities = table_of_states_and_cities.find_element(By.XPATH,
                                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]')

        save_td_data["posicao"] = tr_table_states_and_cities.find_element(By.XPATH,
                                                                          f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[1]').text
        save_td_data["estado"] = tr_table_states_and_cities.find_element(By.XPATH,
                                                                         f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[2]').text
        for item in list_of_states_names:
            if save_td_data['estado'].__contains__(item['estado']):
                save_td_data['sigla'] = item['sigla']

        save_td_data["regiao"] = tr_table_states_and_cities.find_element(By.XPATH,
                                                                         f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[3]').text
        save_td_data["habitantes_por_estado"] = tr_table_states_and_cities.find_element(By.XPATH,
                                                                                        f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[5]').text
        save_td_data["habitantes_por_municipio"] = tr_table_states_and_cities.find_element(By.XPATH,
                                                                                           f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[6]').text

        total_cities = tr_table_states_and_cities.find_element(By.XPATH,
                                                               f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[4]').text

        tr_table_states_and_cities.find_element(By.XPATH,
                                                f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]/td[4]').click()
    except Exception as error:
        print(error)

    # Bloco para pegar as cidades que pertencem ao estado
    try:
        table_cities = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody')
        for row_table_cities in range(1, int(total_cities)):
            citie = {
                "name": "",
                "cod_ibge": ""
            }
            tr_table_cities = table_cities.find_element(By.XPATH,
                                                        f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities}]')

            citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                         f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities}]/td[2]').text
            citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities}]/td[3]').text

            save_td_data["municipios"].append(citie)
    except:
        pass
    try:
        for row_table_cities in range(1, int(total_cities)):
            citie = {
                "name": "",
                "cod_ibge": ""
            }
            table_cities = driver.find_element(By.XPATH,
                                               '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody')

            tr_table_cities = table_cities.find_element(By.XPATH,
                                                        f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities}]')

            if row_table_cities == 23:
                citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities}]/td[2]').text
                citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                                 f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities}]/td[4]').text
            else:
                citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities}]/td[2]').text
                citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities}]/td[3]').text

            save_td_data["municipios"].append(citie)
    except Exception as error:
        pass
    try:
        for row_table_cities in range(1, int(total_cities)):
            citie = {
                "name": "",
                "cod_ibge": ""
            }
            table_cities = driver.find_element(By.XPATH,
                                               '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[1]/tbody')

            tr_table_cities = table_cities.find_element(By.XPATH,
                                                        f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[{row_table_cities}]')

            citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                         f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[{row_table_cities}]/td[2]').text
            citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[{row_table_cities}]/td[3]').text

            save_td_data["municipios"].append(citie)
    except Exception as error:
        pass

    #Adciona dados em table_row_states_and_cities
    # table_row_states_and_cities.append(save_td_data)

    # Se for menor que 27 então prepara para voltar e pegar novos valores
    if count < 27:
        driver.back()
        driver.get(url=url_states_and_cities)

        # Ciando arquivos .json
        with open(f'states_files_json/cities_by{"".join(re.sub(r" ", "_", save_td_data["estado"].lower()))}.json', 'w', encoding="utf-8") as f:
            json.dump({"estado": save_td_data["estado"], "posição": save_td_data["posicao"],
                        "sigla": save_td_data["sigla"], "municipios": save_td_data['municipios']}, f, ensure_ascii=False, indent=4)

        table_of_states_and_cities = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]/tbody')

driver.close()

