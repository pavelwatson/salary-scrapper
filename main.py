from request_functions import get_json


def print_sorted_median_salaries(keywords):
    summary = []
    for keyword in keywords:
        vacancies_list = get_keyword_vacancies(keyword) # list of dictionaries, where each dictionary represents a vacancy
        if (vacancies_list):
            salaries = get_salaries(vacancies_list)
            median = calculate_median_salary(salaries)
            keyword_data = {'keyword': keyword, 'median salary': median, 'number of jobs': len(vacancies_list)}
            summary.append(keyword_data)
    pppprint(summary)


def get_salaries(vacancies_list):
    salaries = [vacancy['salary'] for vacancy in vacancies_list]
    salaries = modify_salaries(salaries)
    return salaries


def pppprint(summary_list):
    summary_list.sort(key=lambda dict: dict['median salary'], reverse=True)
    print('Search Keyword' + " "*15 + 'Median Salary:' + " "*15 + "Number of Jobs:")
    for dict in summary_list:
        print(f'{dict["keyword"]}' + f'{dict["median salary"]}$'.rjust(32-len(dict["keyword"])) + f'{dict["number of jobs"]}'.rjust(32-len(str(dict["median salary"])))) 

    
def get_keyword_vacancies(keyword):
    json_data = get_json(keyword)
    if json_data['found'] < 45:
        return print(f'Not enough data for {keyword}')
    singlepage = get_singepage_data(json_data)
    num_of_pages = json_data['pages']
    if num_of_pages > 1:
        multiplepage = get_multiplepage_data(keyword, num_of_pages)
        return singlepage + multiplepage
    return singlepage


def get_singepage_data(json_data):
    page_vacancies = json_data['items']
    return page_vacancies


def get_multiplepage_data(keyword, num_of_pages):
    multiplepage_data = []
    for page_ind in range(1, num_of_pages):
        json_data = get_json(keyword, page_ind=page_ind)
        page_ind_data = get_singepage_data(json_data)
        multiplepage_data += page_ind_data
    return multiplepage_data


def calculate_median_salary(salaries):
    if len(salaries) % 2 == 1:
        middle = int(len(salaries)/2)
        return salaries[middle]
    elif len(salaries) % 2 == 0:
        middle1 = int(len(salaries)/2)
        middle2 = int(len(salaries)/2) - 1
        median = (salaries[middle1] + salaries[middle2]) / 2
        return round(median)


def modify_salaries(salaries):
    modify_salary_dictionaries(salaries)
    convect_currency_to_usd(salaries)
    salaries.sort(key=lambda dict: dict['salary'])
    salaries_list = [dict['salary'] for dict in salaries]
    return salaries_list


def modify_salary_dictionaries(listOfDicts_withData):
    for dict in listOfDicts_withData:
        if dict['from'] and dict['to']:
            avg_salary = (dict['from'] + dict['to']) / 2
            dict['salary'] = int(avg_salary)
        elif dict['from']and not dict['to']:
            dict['salary'] = dict['from']
        elif dict['to'] and not dict['from']:
            dict['salary'] = dict['to']

        dict.pop('to', None)
        dict.pop('from', None)


def convect_currency_to_usd(listOfDicts_withData):
    currencies = {
            'USD': 1,
            'BYR': 0.3948,
            'EUR': 1.2081,
            'RUR': 0.0135,
            'KZT': 0.0023325,
            'UAH': 0.03647
        }
    for dict in listOfDicts_withData:
        currency = dict['currency']
        dict['salary'] = int(dict['salary'] * currencies[currency])
        dict['currency'] = 'USD'


print_sorted_median_salaries(['Embedded', 'perl', 'Scala', 'Ruby on Rails', 'Golang', 'Django', 'React',
                        '.Net Core', 'Express.js', 'Node', 'Express',
                        'Symfony', 'Laravel', 'Spring',
                        'DevOps', 'System Administrator', 'Security engineer',
                        'Data engineer', 'data analyst', 'Robotics', 'Microcontrollers', 'Android', 'kotlin',
                        'Unity', "Unreal Engine", "Machine Learning", "Data science", 'Artificial intelligence',
                         'Встроенное по', 'Network engineer', 'swift'])

# print_sorted_median_salaries(['Frontend', 'Backend', 'Web development', 
#                                      'Data Science', 'Data Engineering', 'Mobile Development',
#                                      'Android', 'IOS', 'User Experience', 'Virtual Reality',
#                                      'Games Development', 'Machine Learning', 'IOT', 'Internet of Things',
#                                      'Physical Computing', 'R&D'])
