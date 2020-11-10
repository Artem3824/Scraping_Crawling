import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re


def salary(text):
    pattern = re.compile('(\d+. ?\d+)')
    compensation = re.findall(pattern, text)
    compensation = [int(i.replace('\xa0', '')) for i in compensation]
    salary_dict = {}
    if compensation:
        new_text = text.split(' ')
        currency = new_text[-1]
        if len(compensation) == 1 and new_text[0] == 'от':
            min_salary = compensation[0]
            max_salary = 0
        elif len(compensation) == 1 and new_text[0] == 'до':
            min_salary = 0
            max_salary = compensation[0]
        else:
            min_salary = compensation[0]
            max_salary = compensation[1]

    salary_dict['min'] = min_salary
    salary_dict['max'] = max_salary
    salary_dict['cur'] = currency
    return salary_dict


vacancy = input('Введите профессию: ')
main_link = 'https://www.superjob.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

response = requests.get(f'{main_link}/vacancy/search/?keywords={vacancy}')
superjob_vacancies = []

while True:
    soup = BeautifulSoup(response.text, 'lxml')
    vacancies_block = soup.find_all('div', {'class': '_3zucV undefined _3SGgo'})[1]
    vacancy_list = vacancies_block.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    for vac in vacancy_list:
        vacancy_data = {}
        main_data = vac.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'})
        vac_name = main_data.getText()
        vac_url = main_link + main_data.find('a')['href']
        employer_data = vac.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'})
        employer_name = employer_data.getText() if employer_data else None
        employer_url = main_link + employer_data.find('a')['href'] if employer_data else None
        vac_salary = vac.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText().strip()
        # if vac_salary != 'По договорённости':
        #     salary_data = salary(vac_salary)
        #     min_salary = salary_data['min']
        #     max_salary = salary_data['max']
        #     currency = salary_data['cur']
        # else:
        #     min_salary = 0
        #     max_salary = 0
        #     currency = 0


        vacancy_data['name'] = vac_name
        vacancy_data['url'] = vac_url
        vacancy_data['employer'] = employer_name
        vacancy_data['employer_url'] = employer_url
        # vacancy_data['min_salary'] = min_salary
        # vacancy_data['max_salary'] = max_salary
        # vacancy_data['currency'] = currency
        vacancy_data['source'] = main_link
        superjob_vacancies.append(vacancy_data)

    '''Pagination'''
    navigation = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
    if navigation:
        next_page = main_link + navigation['href']
    else:
        break
    response = requests.get(f'{next_page}', headers=headers)

pprint(superjob_vacancies)
print(len(superjob_vacancies))

