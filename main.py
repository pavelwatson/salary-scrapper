import math

from main_functions import print_salaries_data


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




def main():
    city = 'Moscow'
    print_salaries_data(city, 'Express') # takes city and one keyword and then print all the data for this keyword 



    # compare_median_salaries(city,'.Net Core', 'Django', 'Express',
                            # 'Laravel', 'Ruby on Rails', 'Spring Boot',
                            # 'react', 'Symfony', 'Golang')
    # print('')
    # compare_average_salaries(city, '.Net Core', 'Django', 'Express',
    #                          'Laravel', 'Ruby on Rails', 'react',
    #                           'Symfony', 'Golang', 'Spring Boot')

if __name__ == '__main__':
    main()