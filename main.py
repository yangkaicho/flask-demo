
from flask import Flask, render_template, request
from datetime import date
from flask import Flask, render_template
from pm25 import get_pm25, get_six_pm25, get_countys, get_county_pm25
import json


app = Flask(__name__)

# 首頁

stocks = [
    {'分類': '日經指數', '指數': '22,920.30'},
    {'分類': '韓國綜合', '指數': '2,304.59'},
    {'分類': '香港恆生', '指數': '25,083.71'},
    {'分類': '上海綜合', '指數': '3,380.68'}
]


@app.route('/index/')
@app.route('/index/<name>')
def index(name='GUEST'):

    date = get_date()
    return render_template('./index.html', user_name=name, date=date)


@app.route('/date')
def get_date():
    from datetime import datetime
    date = datetime.now()
    print(date)
    return date.strftime('%Y-%m-%d %H:%M:%S')

# <type:id>


@app.route('/book/<int:id>')
def get_book(id):
    try:

        books = {1: 'Python', 2: 'HTML', 3: 'CSS'}
        return books[id]
    except Exception as e:
        print(e)
        return '書籍編號錯誤!'


@app.route('/sum/x=<a>&y=<b>')
def get_sum(a, b):
    total = eval(a)+eval(b)
    return f'{a}+{b}={total}'


@app.route('/bmi/name=<name>&height=<a>&weight=<b>')
def get_bmi(name, a, b):
    try:

        bmi = eval(b)/((eval(a)/100)**2)
        return f'姓名:{name} 身高:{b} 體重:{a} BMI為:{round(bmi,2)}'
    except Exception as e:
        print(e)
        return '參數輸入錯誤!'


@app.route('/stock')
def get_stock():
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]
    date = get_date()

    return render_template('./stock.html', date=date, stocks=stocks)


@app.route('/pm25', methods=['GET', 'POST'])
def pm25():
    sort = False

    if request.method == 'POST':
        sort = True

    date = get_date()
    columns, values = get_pm25(sort)

    return render_template('./pm25.html', **locals())

@app.route('/')
@app.route('/pm25-charts')
def pm25_charts():

    return render_template('./pm25-charts-bulma.html', countys=get_countys())


@app.route('/pm25-json', methods=['POST'])
def pm25_josn():
    columns, values = get_pm25()

    site = [value[1]for value in values]
    pm25 = [value[2]for value in values]
    date = values[0][-1]

    return json.dumps({'date': date, 'site': site, 'pm25': pm25}, ensure_ascii=False)


@app.route('/pm25-six-json', methods=['POST'])
def pm25_six_json():
    values = get_six_pm25()
    site = [value[0]for value in values]
    pm25 = [value[1]for value in values]
    return json.dumps({'site': site, 'pm25': pm25}, ensure_ascii=False)


@app.route('/pm25-county/<county>', methods=['POST'])
def pm25_county_json(county):

    values = get_county_pm25(county)
    site = [value[0]for value in values]
    pm25 = [value[1]for value in values]

    return json.dumps({'site': site, 'pm25': pm25}, ensure_ascii=False)


if __name__ == '__main__':

    app.run(debug=True)
