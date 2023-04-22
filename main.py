import requests
import pprint
import json


url = 'https://api.hh.ru/vacancies'
search_vac = ['ml', 'python']
lst = []
for search in search_vac:
    params = {'page': 1,
              'per_page': 20,
              'text': search,
              'area': 113,
              'only_with_salary': True}
    response = requests.get(url, params=params)
    print(f'Статус ({search}): {response.status_code}')
    result = response.json()
    list_vac = result['items']
    # pprint.pprint(response.json())

    # print(result['items'][0]['url'])
    skills = {'Python': 0, 'Spark': 0, 'Hadoop': 0, 'Docker': 0, 'Linux': 0, 'Git': 0, 'SQL': 0, 'PyTorch': 0,
              'Keras': 0,
              'Sklearn': 0, 'Pandas': 0, 'Scipy': 0, 'Numpy': 0, 'XGBoost': 0, 'CatBoost': 0, 'LightGBM': 0,
              'Matplotlib': 0, 'REST': 0, 'FastApi': 0, 'JSON': 0, 'Django': 0, 'Flask': 0, 'Redis': 0, 'Cassandra': 0,
              'ClickHouse': 0}
    salary = 0
    for i in range(len(list_vac)):
        # print(list_vac[i]['url'])
        vacancy_url = list_vac[i]['url']
        if list_vac[i]['salary']['from'] is None:
            sal = list_vac[i]['salary']['to']
        else:
            sal = list_vac[i]['salary']['from']
        if list_vac[i]['salary']['currency'] == 'USD':
            salary += sal * 80
        elif list_vac[i]['salary']['currency'] == 'EUR':
            salary += sal * 90
        else:
            salary += sal

        response = requests.get(vacancy_url)
        print(f'Статус {i + 1}: {response.status_code}')
        result = response.json()
        # print(result)
        desc = result['description']
        for key in skills.keys():
            if key.lower() in desc.lower():
                skills[key] += 1
    pprint.pprint(skills)
    lst_2 = []
    for key, value in skills.items():
        lst_2.append({'name': key, 'count': value, 'persent': round(value / len(list_vac) * 100, 1)})
    lst.append({'keywords': search, 'salary_mean': round(salary / len(list_vac)), 'count': len(list_vac),
                'requirements': lst_2})

pprint.pprint(lst)
with open("data_vac.json", "w") as f:
    json.dump(lst, f)
