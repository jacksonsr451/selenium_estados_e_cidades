from time import sleep

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
    table_row_states_with_sigle.append(table_states_by_sigle.find_element(By.CSS_SELECTOR, f'body > div.site > div.conteudo > table > tbody > tr:nth-child({row})'))

row = 1
for element in table_row_states_with_sigle:
    state: {} = {
        "estado": "",
        "sigla": ""
    }
    if row > 1:
        state['estado'] = element.find_element(By.CSS_SELECTOR,
                                               f'body > div.site > div.conteudo > table > tbody > tr:nth-child({row}) > td:nth-child(2)').text
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
    print(row)
    count += 1
    tr_table_states_and_cities = table_of_states_and_cities.find_element(By.XPATH,
                                            f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[3]/tbody/tr[{row}]')
    save_td_data: {} = {
        "posicao": "",
        "estado": "",
        "sigla": "",
        "regiao": "",
        "municipios": [],
        "habitantes_por_estado": "",
        "habitantes_por_municipio": ""
    }
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

    citie = {
        "name": "",
        "cod_ibge": ""
    }

    try:
        table_cities = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody')
        for row_table_cities in range(int(total_cities)):
            if row_table_cities < 26:
                tr_table_cities = table_cities.find_element(By.XPATH,
                                                            f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities + 1}]')

                citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities + 1}]/td[2]').text
                citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                                 f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]/tbody/tr[{row_table_cities + 1}]/td[3]').text

            save_td_data["municipios"].append(citie)
    except:
        table_cities = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody')
        for row_table_cities in range(int(total_cities)):
            if row_table_cities < 26:
                tr_table_cities = table_cities.find_element(By.XPATH,
                                                            f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities + 1}]')

                citie['name'] = tr_table_cities.find_element(By.XPATH,
                                                             f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities + 1}]/td[2]').text
                citie['cod_ibge'] = tr_table_cities.find_element(By.XPATH,
                                                                 f'/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table/tbody/tr[{row_table_cities + 1}]/td[3]').text

            save_td_data["municipios"].append(citie)

    table_row_states_and_cities.append(save_td_data)

    if count <= 26:
        print(count)
        driver.back()
        driver.get(url=url_states_and_cities)
        sleep(2)
        table_of_states_and_cities = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]/tbody')
    else:
        print(count)
driver.close()

print(table_row_states_and_cities)


