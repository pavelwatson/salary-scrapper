import json
import requests

def get_json(keyword, page_ind=0):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    u_id = 1   # MOSCOW
    # u_id = 113   # SANKT-PETERSBURG 
    # u_id = 1002  # MINSK
    # u_id = 115   # KIEV
    only_with_salary = 'true'
    url = f'https://api.hh.ru/vacancies?&text={keyword}&area={u_id}&only_with_salary={only_with_salary}&page={page_ind}&specialization=1'

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data


def test():
    json_data = get_json('Python')
    print(json_data['found'])


if __name__ == '__main__':
    test()
