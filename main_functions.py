from request_functions import get_html, get_num_of_pages
from scrap_functions import scrap_data
from data_modifying_functions import modify_data

# def print_salaries(city, keyword):
#     dict_salaries, num_of_jobs = prepair(keyword, city)
#     print(f'{num_of_jobs} vacancies «{keyword.title()}» in {city.title()}:', end='')
#     for ind, dict in enumerate(dict_salaries):
#         if (ind % 5) == 0:
#             print('') # print new row
#         print('\tSalary:', end='')
#         print(f'{dict["salary"]}'.rjust(5), end='')
#         print(f'{dict["currencyCode"]}'.rjust(4).ljust(16), end='')

#     average = calculate_average_salary(dict_salaries)
#     print(f'\n\nAverage Salary is: {average} USD')
#     median = calculate_median_salary(dict_salaries)
#     print(f'Median Salary is: {median} USD')


# def compare_median_salaries(city, *keywords):
#     info = []
#     for keyword in keywords:
#         dict_salaries, num_of_jobs = prepair(keyword, city)
#         median = calculate_median_salary(dict_salaries)
#         dict = {'median': median,
#                 'string': f'\t{keyword.upper()}, median salary: {median} USD per {num_of_jobs} vacancies'}
#         info.append(dict)
#     print(info)
#     sorted_info = sorted(info, key=lambda dict:  dict['median'], reverse=True)

#     print('Median Salaries:')
#     for dict in sorted_info:
#         print(dict['string'])

def print_salaries_data(city, keyword):
    html = get_html(city, keyword)

    print_singlepage_data(html)

    num_of_pages = get_num_of_pages(html)
    if num_of_pages > 1:
        print_multiplepage_data(city, keyword, num_of_pages)


def print_singlepage_data(html):
    data = scrap_data(html)
    data = modify_data(data)
    print_salaries_in_rows(data)


def print_multiplepage_data(city, keyword, num_of_pages):
    for page_ind in range(1, num_of_pages):
        html = get_html(city, keyword, page_ind)
        print_singlepage_data(html)


def print_salaries_in_rows(data):
    for ind, dict in enumerate(data):
        if (ind % 5) == 0:
            print('') # print new row
        print('\tSalary:', end='')
        print(f'{dict["salary"]}'.rjust(5), end='')
        print(f'{dict["currencyCode"]}'.rjust(4).ljust(16), end='')
    


# print_salaries_data('Moscow', 'Express.js')
print_salaries_data('Moscow', 'Python')

# print_multiplepage_data(2)