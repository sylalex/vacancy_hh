from builtins import tuple

import requests
import pprint
import json
import time
from flask import Flask, render_template, request
import sqlite3
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


def get_vac(search='ml', per_page=20):
    url = 'https://api.hh.ru/vacancies'
    # search = 'ml'
    # per_page = 20
    lst_vac_for_html = []
    lst = []
    # con = sqlite3.connect("hh.sqlite")
    # cursor = con.cursor()
    engine = create_engine('sqlite:///hh.sqlite')
    Base = declarative_base()

    class Vacancy(Base):
        __tablename__ = 'vacancy'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        city_id = Column(Integer, ForeignKey('city.id'))
        salary_from = Column(Integer)
        salary_to = Column(Integer)
        currency_id = Column(Integer, ForeignKey('currency.id'))

        def __init__(self, name, city_id, salary_from, salary_to, currency_id):
            self.name = name
            self.city_id = city_id
            self.salary_from = salary_from
            self.salary_to = salary_to
            self.currency_id = currency_id

    class City(Base):
        __tablename__ = 'city'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, name):
            self.name = name

    class Currency(Base):
        __tablename__ = 'currency'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, name):
            self.name = name

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

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
        # cursor.execute("insert or ignore into city (name) VALUES (?)", (list_vac[i]['area']['name'],))
        insert_com = City.__table__.insert().prefix_with('OR IGNORE').values(name=list_vac[i]['area']['name'])
        session.execute(insert_com)
        # session.add(City(list_vac[i]['area']['name']))

        # cursor.execute("select * from city where name=?", (list_vac[i]['area']['name'],))
        city_values = session.query(City.id).filter(City.name == list_vac[i]['area']['name']).first()
        # city_values = cursor.fetchone()
        # print(city_values)
        # cursor.execute("insert or ignore into currency (name) VALUES (?)", (list_vac[i]['salary']['currency'],))
        insert_com = Currency.__table__.insert().prefix_with('OR IGNORE').values(name=list_vac[i]['salary']['currency'])
        session.execute(insert_com)
        # session.add(Currency(list_vac[i]['salary']['currency']))

        # cursor.execute("select * from currency where name=?", (list_vac[i]['salary']['currency'],))
        currency_values = session.query(Currency.id).filter(Currency.name == list_vac[i]['salary']['currency']).first()
        # currency_values = cursor.fetchone()
        # print(currency_values)
        # cursor.execute("insert into vacancy (name, city_id, salary_from, salary_to, currency_id) VALUES (?,?,?,?,?)",
        #                (list_vac[i]['name'], city_values[0], list_vac[i]['salary']['from'],
        #                 list_vac[i]['salary']['to'], currency_values[0]))
        session.add(Vacancy(list_vac[i]['name'], city_values[0], list_vac[i]['salary']['from'],
                            list_vac[i]['salary']['to'], currency_values[0]))
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
    # cursor.execute("select * from vacancy")
    # print(cursor.fetchall())
    # con.commit()
    session.commit()
    for vac in session.query(Vacancy).all():
        city = session.query(City).filter(vac.city_id == City.id).first()
        print(f'{vac.name} ({city.name})')
    return lst_vac_for_html


@app.route('/')
def index():
    return render_template('index.html', name='ПАРСЕР HH')


@app.route('/services/', methods=['POST', 'GET'])
def services():
    if request.method == 'POST':
        lst = get_vac(request.form['search'], int(request.form['per_page']))
        return render_template('services.html', lst=lst, methods='POST')
    else:
        return render_template('services.html', methods='GET')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
