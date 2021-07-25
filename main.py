import requests
from bs4 import BeautifulSoup as bs
import re
import ast
import math

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_html(keyword, city, pages):
    urls = []
    for ind in range(pages):
        if city == 'Minsk':
            only_with_salary_url = f'https://rabota.by/search/vacancy?area=1002&&specialization=1&text={keyword.replace(" ", "+")}&only_with_salary=true&page={ind}'
            urls.append(only_with_salary_url)
        elif city == 'Moscow':
            only_with_salary_url = f'https://hh.ru/search/vacancy?area=1&specialization=1&text={keyword.replace(" ", "+")}&only_with_salary=true&page={ind}'
            urls.append(only_with_salary_url)
    pages = [requests.get(url, headers=headers) for url in urls]
    return pages


def find_salaries(pages):
    salaries = []
    for page in pages:
        regex = r'"compensation": {"from".+?"currencyCode": "..."|"compensation": {"to".+?"currencyCode": "..."'
        pattern = re.compile(regex)
        salaries.append(pattern.findall(page.text))
    return [salary for sublist in salaries for salary in sublist]


def make_list_of_dictionaries(salaries):
    modified_salaries = (salary.replace('"compensation": ', '') + '}' for salary in salaries)
    dict_salaries = [ast.literal_eval(salary) for salary in modified_salaries]
    return dict_salaries


def modify_dictionary(dict_salaries):
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


def print_salaries(city, keyword):
    dict_salaries, num_of_jobs = prepair(keyword, city)
    print(f'{num_of_jobs} vacancies «{keyword.title()}» in {city.title()}:', end='')
    for ind, dict in enumerate(dict_salaries):
        if (ind % 5) == 0:
            print('') # print new row
        print('\tSalary:', end='')
        print(f'{dict["salary"]}'.rjust(5), end='')
        print(f'{dict["currencyCode"]}'.rjust(4).ljust(16), end='')

    average = calculate_average_salary(dict_salaries)
    print(f'\n\nAverage Salary is: {average} USD')
    median = calculate_median_salary(dict_salaries)
    print(f'Median Salary is: {median} USD')


def calculate_average_salary(dict_salaries):
    salaries = 0
    for dict in dict_salaries:
        salaries += dict['salary']
    num_of_jobs = len(dict_salaries)
    return round(salaries / num_of_jobs)


def sort_salaries(dict_salaries):
    return dict_salaries.sort(key=lambda dict: dict['salary'])

def calculate_median_salary(dict_salaries):
    salaries = []
    for dict in dict_salaries:
        salaries.append(dict['salary'])
    if len(salaries) % 2 == 1:
        middle = int(len(salaries)/2)
        return salaries[middle]
    elif len(salaries) % 2 == 0:
        middle1 = int(len(salaries)/2)
        middle2 = int(len(salaries)/2) - 1
        median = (salaries[middle1] + salaries[middle2]) / 2
        return round(median)


def compare_median_salaries(city, *keywords):
    info = []
    for keyword in keywords:
        dict_salaries, num_of_jobs = prepair(keyword, city)
        median = calculate_median_salary(dict_salaries)
        dict = {'median': median,
                'string': f'\t{keyword.upper()}, median salary: {median} USD per {num_of_jobs} vacancies'}
        info.append(dict)
    print(info)
    sorted_info = sorted(info, key=lambda dict:  dict['median'], reverse=True)

    print('Median Salaries:')
    for dict in sorted_info:
        print(dict['string'])


def prepair(keyword, city):
    initial_html = get_html(keyword, city, 1)  # needed for extracting number of pages
    print(keyword+' ', end='')
    num_of_jobs = get_num_of_jobs(initial_html[0])
    number_of_pages = math.ceil(num_of_jobs / 50)

    htmls = get_html(keyword, city, number_of_pages)  # return list of requests with HTML files
    salaries_info = find_salaries(htmls)  # scrap HTML files for salary information
    dict_salaries = make_list_of_dictionaries(salaries_info)  # put all salary information in dictionaries(JS objects)
    modify_dictionary(dict_salaries)  # format dictionaries in a nice way 
    convect_currency_to_usd(dict_salaries)  # change all currency to Dollars
    sort_salaries(dict_salaries)  # sort dictionaries by salaries

    return dict_salaries, num_of_jobs  # return data for printing


def get_num_of_jobs(html):
    regex = r'(Найдено\s\d+?\sвакансий|Найдена\s\d+?\sвакансия|Найдено\s\d+?\sвакансии)'
    pattern = re.compile(regex)
    num_of_jobs_str = pattern.search(html.text).group(0)
    print(num_of_jobs_str +'\t\t', end='')
    num_of_jobs = int(re.search('\d+', num_of_jobs_str).group(0))
    return num_of_jobs
        



def main():
    city = 'Moscow'
    # print_salaries('Express', city)
    compare_median_salaries(city,'.Net Core', 'Django', 'Express',
                            'Laravel', 'Ruby on Rails', 'Spring Boot',
                            'react', 'Symfony', 'Golang')
    print('')
    # compare_average_salaries(city, '.Net Core', 'Django', 'Express',
    #                          'Laravel', 'Ruby on Rails', 'react',
    #                           'Symfony', 'Golang', 'Spring Boot')

if __name__ == '__main__':
    # main()
    city = 'Moscow'
    keyword = 'Python'
    dict_salaries, num_of_jobs = prepair(keyword, city)
    print(num_of_jobs)