from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/points/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        name = request.form['Name']
        data = findNameAndPoints(name)

        if data != None:
            return render_template('points.html', name=data[0], points=data[1])
        else:
            return "name not found"

    else:
        return redirect(url_for('home'))


def getData():
    sheet_url = "https://docs.google.com/spreadsheets/d/1t-W9RcsgEuTvNbwB9dRMfoMKjoN8kyJFJeLcHfiO8rs/edit#gid=0"
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    records = df.to_dict('records')

    ## The first one is the empty field, so we don't care about that
    del records[0]

    return records


def findNameAndPoints(name):
    records = getData()
    for r in records:
        if name == r['name']:
            return (name, int(r['sum points']))

    return None


if __name__ == '__main__':
    app.run()
