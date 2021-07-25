import ast # module for converting string to dictionary

def modify_data(data):
    listOfDicts_withData = make_list_of_dictionaries(data)
    modify_dictionaries(listOfDicts_withData)  # modifies all data IN PLACE, so refer to listOfDicts_withData
    convect_currency_to_usd(listOfDicts_withData)
    # sort_by_salary(listOfDicts_withData)
    return listOfDicts_withData


def make_list_of_dictionaries(data):
    modified_data = (string.replace('"compensation": ', '') + '}' for string in data)
    listOfDicts_withData = [ast.literal_eval(dict) for dict in modified_data] # converting string that looks like dictionary to an actual dictionary
    return listOfDicts_withData


def modify_dictionaries(listOfDicts_withData):
    for dict in listOfDicts_withData:
        if 'from' in dict and 'to' in dict:
            avg_salary = (dict['from'] + dict['to']) / 2
            dict['salary'] = int(avg_salary)
        elif 'from' in dict and 'to' not in dict:
            dict['salary'] = dict['from']
        elif 'to' in dict and 'from' not in dict:
            dict['salary'] = dict['to']

        dict.pop('to', None)
        dict.pop('from', None)


def convect_currency_to_usd(listOfDicts_withData):
    currencies = {
            'USD': 1,
            'BYR': 0.3948,
            'EUR': 1.2081,
            'RUR': 0.0135,
            'KZT': 0.0023325
        }
    for dict in listOfDicts_withData:
        currency = dict['currencyCode']
        dict['salary'] = int(dict['salary'] * currencies[currency])
        dict['currencyCode'] = 'USD'


def sort_by_salary(dict_salaries):
    return dict_salaries.sort(key=lambda dict: dict['salary'])


def calculate_average_salary(dict_salaries):
    salaries = 0
    for dict in dict_salaries:
        salaries += dict['salary']
    num_of_jobs = len(dict_salaries)
    return round(salaries / num_of_jobs)





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

