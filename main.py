import requests
from bs4 import BeautifulSoup as bs
import re
import ast

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_data():
    only_with_salary_url = 'https://rabota.by/search/vacancy?area=1002&&specialization=1&text=Python&only_with_salary=true'
    page = requests.get(only_with_salary_url, headers=headers)
    return page
