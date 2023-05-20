import requests
import pprint
import json
import time
from flask import Flask, render_template, request

app = Flask(__name__)


def get_vac(search='ml', per_page=20):
    url = 'https://api.hh.ru/vacancies'
    # search = 'ml'
    # per_page = 20
    lst_vac_for_html = []
    lst = []

    params = {'page': 1,
              'per_page': per_page,
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
    key_skills = []
    salary = 0
    for i in range(len(list_vac)):
        dct = {'name': list_vac[i]['name'], 'city': list_vac[i]['area']['name'], 'salary': list_vac[i]['salary']}
        lst_vac_for_html.append(dct)
        # print(list_vac[i]['url'])
        # vacancy_url = list_vac[i]['url']
        # if list_vac[i]['salary']['from'] is None:
        #     sal = list_vac[i]['salary']['to']
        # else:
        #     sal = list_vac[i]['salary']['from']
        # if list_vac[i]['salary']['currency'] == 'USD':
        #     salary += sal * 80
        # elif list_vac[i]['salary']['currency'] == 'EUR':
        #     salary += sal * 90
        # else:
        #     salary += sal
        # time.sleep(1)
        # response = requests.get(vacancy_url)
        # print(f'Статус {i + 1}: {response.status_code}')
        # result = response.json()
        # # print(result)
        # desc = result['description']
        # key_sc = result['key_skills']
        # for key in skills.keys():
        #     if key.lower() in desc.lower():
        #         skills[key] += 1
        # if key_sc is not None:
        #     for key in key_sc:
        #         if key['name'] not in key_skills:
        #             key_skills.append(key['name'])

    # pprint.pprint(skills)
    # lst_2 = []
    # for key, value in skills.items():
    #     lst_2.append({'name': key, 'count': value, 'persent': round(value / len(list_vac) * 100, 1)})
    # lst.append({'keywords': search, 'salary_mean': round(salary / len(list_vac)), 'count': len(list_vac),
    #             'requirements': lst_2})
    #
    # pprint.pprint(lst)
    # pprint.pprint(key_skills)
    # with open(f"{search}.json", "w") as f:
    #     json.dump(lst, f)
    return lst_vac_for_html


@app.route('/')
def index():
    return render_template('index.html', name='ПАРСЕР HH')


@app.route('/services/', methods=['POST', 'GET'])
def services():
    if request.method == 'POST':
        lst = get_vac(request.form['search'], int(request.form['per_page']))
        return render_template('services.html', lst=lst)
    else:
        return render_template('services.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
