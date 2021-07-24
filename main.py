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

page = get_data()
jobs = find_salaries(page)
print(len(jobs))