import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import pandas as pd
from pymongo import MongoClient

'''Convert salary range to max, min'''
def salary(text):
    pattern = re.compile('(\d+. ?\d+)')
    compensation = re.findall(pattern, text)
    compensation = [int(i.replace('\xa0', '')) for i in compensation]
    salary_dict = {}
    min_salary = 0
    max_salary = 0
    currency = 0
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


main_link = 'https://hh.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

vacancy_input = input('Enter job title: ')
response = requests.get(f'{main_link}/search/vacancy?clusters=true&area=1&search_field=name&enable_snippets=true&salary=&st=searchVacancy&text={vacancy_input}',
                        headers=headers)
jobs = []
while True:
    soup = BeautifulSoup(response.text, 'lxml')
    block_of_jobs = soup.find('div', {'class': 'vacancy-serp'})
    job_block = block_of_jobs.find_all('div', {'class': 'vacancy-serp-item'})
    for job in job_block:
        job_dict = {}
        job_title = job.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText().strip()
        job_url = job.find('a', {'class': 'bloko-link HH-LinkModifier'}).get('href').split('?')[0]
        job_id = job_url.split('/')[-1]
        job_employer_info = job.find('div', {'class': 'vacancy-serp-item__meta-info'})
        job_employer_name = job_employer_info.getText().strip()
        job_employer_url = main_link + job_employer_info.find('a').get('href')
        job_salary = job.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText().strip()
        if job_salary:
            salary_data = salary(job_salary)
            min_salary = salary_data['min']
            max_salary = salary_data['max']
            currency = salary_data['cur']
            job_salary = job_salary.replace('\xa0', ' ')
        else:
            job_salary = 'По договоренности'
            min_salary = 0
            max_salary = 0
            currency = 0
        job_dict['id'] = job_id
        job_dict['url'] = job_url
        job_dict['title'] = job_title
        job_dict['employer'] = job_employer_name
        job_dict['employer_url'] = job_employer_url
        job_dict['salary'] = job_salary
        job_dict['min_salary'] = min_salary
        job_dict['max_salary'] = max_salary
        job_dict['currency'] = currency
        job_dict['source'] = main_link
        jobs.append(job_dict)

    '''Pagination'''
    next_page_url = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
    if next_page_url:
        next_page = main_link + next_page_url.get('href')
    else:
        break
    response = requests.get(next_page, headers=headers)

pprint(jobs)
pprint(len(jobs))

