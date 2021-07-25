import requests
import re
import math

def get_html(city, keyword, page_ind=0):
    """return HTML file of the first web page based on the given City and Keyword"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    urls = {
        'Minsk': f'https://rabota.by/search/vacancy?area=1002&specialization=1&text={keyword.replace(" ", "+")}&only_with_salary=true&page={page_ind}&order_by=salary_asc',
        'Moscow': f'https://hh.ru/search/vacancy?area=1&specialization=1&text={keyword.replace(" ", "+")}&only_with_salary=true&page={page_ind}&order_by=salary_asc'
    }

    url = urls[city]
    html = requests.get(url, headers=headers)
    return html.text


def get_num_of_jobs(html):
    regex = r'header-1">(\d+).*?ваканс'
    pattern = re.compile(regex)
    num_of_jobs = int(pattern.search(html).group(1))
    return num_of_jobs


def get_num_of_pages(html):
    num_of_jobs = get_num_of_jobs(html)
    num_of_pages = math.ceil(num_of_jobs / 50) # website has 50 jobs per page;  math.cell rounds number up
    return num_of_pages
