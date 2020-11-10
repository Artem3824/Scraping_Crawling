import csv
import datetime
import requests
import json
from pprint import pprint

TOKEN = 'yourToken'
headers = {'freelancer-oauth-v1': TOKEN, 'content-type': 'application/json'}

URL = "https://www.freelancer.com/api/projects/0.1/projects/active/"

QUERIES = ['Research', 'Web search', 'Business Analysis', 'Data Processing', 'Data Collection', 'Market Research',
           'Data Scraping', 'Web Scraping', 'Data Mining', 'Scrapy', 'Internet Research']

# Function for making a dictionary of 'params'
def search_by_query(query):
    from_time_projects = datetime.datetime.now() - datetime.timedelta(hours=8)
    time_in_unix = int(datetime.datetime.timestamp(from_time_projects))
    params = {'query': query,
              'job_details': True,  # True - for more information about necessary skills
              'project_types[]': 'fixed', # fixed or hourly
              'sort_field': 'time_updated', # sorting field by (time_updated/bid_count/bid_enddate/bid_avg_usd)
              'reverse_sort': True, # sorting field by 'sort_field'
              'compact': True,  # If set, strip all null and empty values from response
              'from_time': time_in_unix,  # Returns projects last updated after this time
              }
    return params


def make_response(params):
    response = requests.get(URL, headers=headers, params=params)
    if response.ok:
        data = json.loads(response.text)
        return data


def list_of_search(data):
    list_of_search_results = data['result']['projects']
    return list_of_search_results


def get_amount_of_jobs(data):
    list_of_search_results = data['result']
    return list_of_search_results['total_count']


def get_info(list_of_results):
    '''Open file for further searching duplicates'''
    count_new_projects = 0
    with open('freelance_jobs.csv', 'r', newline='', encoding='utf8') as result_csv:
        csv_data = csv.reader(result_csv)
        list_ids = []
        for row in csv_data:
            if row:
                list_ids.append(row[0])
        '''Get information about each project'''
        for i in list_of_results:
            project_id = str(i['id'])
            seo_url = 'https://www.freelancer.com/projects/' + i['seo_url']
            description = i['preview_description'].strip().split('\n')
            join_description = ' '.join(description)
            try:
                budget_max = int(i['budget']['maximum'])
            except KeyError:
                budget_max = 'Unknown'
            budget_min = int(i['budget']['minimum'])
            currency = i['currency']['name']
            budget_projects = f'{budget_min} - {(budget_max)} {currency}'
            time_submitted = datetime.datetime.fromtimestamp(i['time_submitted'])
            difference_time = int((datetime.datetime.now() - time_submitted).seconds / 60)
            if difference_time < 60:
                difference_time = f'{difference_time} min ago'
            else:
                hours = difference_time // 60
                minutes = difference_time % 60
                difference_time = f'{hours}h:{minutes} min ago'
            results = (project_id, seo_url, join_description, difference_time, budget_projects)

            '''After gathering the information about the project, 
            check if this project has already been added to the file and write it to the file'''
            if results[0] not in list_ids:
                with open('freelance_jobs.csv', 'a', newline='', encoding='utf8') as new_result_csv:
                    writer = csv.writer(new_result_csv)
                    writer.writerow(results)
                    count_new_projects += 1

    print(f'Total jobs: {len(list_of_results)}')
    print(f'New projects: {count_new_projects}\n')


def main_search_by_query():
    for i in QUERIES:
        print(f'Search by {i}')
        searching = search_by_query(i)
        response_id = make_response(searching)
        search_list = list_of_search(response_id)
        get_info(search_list)


main_search_by_query()


'''Count the most popular jobs by queries
1) Open file with saved queries
2) Searching projects by amount
3) Write the result into a new file
'''
# with open('queries.csv', 'r', newline='') as csv_file:
#     csv_data = csv.reader(csv_file)
#     for row in csv_data:
#         searching_params = search_by_query(row)
#         response_by_query = make_response(searching_params)
#         amount_by_query = get_len_of_jobs(response_by_query)
#         with open('popularity_by_query.csv', 'a', newline='') as out_file:
#             writer = csv.writer(out_file)
#             new_results = [row[0], amount_by_query]
#             writer.writerow(new_results)
