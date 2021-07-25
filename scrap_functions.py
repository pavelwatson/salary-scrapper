import re
def scrap_data(html):
    regex = r'"compensation": {"from".+?"currencyCode": "..."|"compensation": {"to".+?"currencyCode": "..."'
    pattern = re.compile(regex)
    data = pattern.findall(html)
    return data