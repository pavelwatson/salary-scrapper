import requests
import re
import ast

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_data():
    keyword = 'embedded'
    only_with_salary_url = f'https://rabota.by/search/vacancy?area=1002&&specialization=1&text={keyword}&only_with_salary=true'
    page = requests.get(only_with_salary_url, headers=headers)
    return page


def find_salaries(page):
    regex = r'"compensation": {"from".+?"currencyCode": "..."|"compensation": {"to".+?"currencyCode": "..."'
    pattern = re.compile(regex)
    salaries = pattern.findall(page.text)
    return salaries

def make_list_of_dictionaries(salaries):
    modified_salaries = (salary.replace('"compensation": ', '') + '}' for salary in salaries)
    dict_salaries = [ast.literal_eval(salary) for salary in modified_salaries]
    return dict_salaries

def modify_dictionaries(dict_salaries):
    for dict in dict_salaries:
        if 'from' in dict and 'to' in dict:
            avg_salary = (dict['from'] + dict['to']) / 2
            dict['salary'] = int(avg_salary)
        elif 'from' in dict and 'to' not in dict:
            dict['salary'] = dict['from']
        elif 'to' in dict and 'from' not in dict:
            dict['salary'] = dict['to']

        dict.pop('to', None)
        dict.pop('from', None)

def convect_currency_to_usd(dict_salaries):
    for dict in dict_salaries:
        if dict['currencyCode'] == 'BYR':
            dict['salary'] = int(dict['salary'] * 0.3948)  # convert BYN to USD
        elif dict['currencyCode'] == 'EUR':
            dict['salary'] = int(dict['salary'] * 1.2081) # convert EUR to USD
        elif dict['currencyCode'] == 'RUR':
            dict['salary'] = int(dict['salary'] * 0.0135)  # convert RUB to USD
        elif dict['currencyCode'] == 'KZT':
            dict['salary'] = int(dict['salary'] * 0.0023325)  # convert KZT to USD
        dict['currencyCode'] = 'USD'

page = get_data()
jobs = find_salaries(page)
print(len(jobs))