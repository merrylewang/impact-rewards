from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

TOTAL_POINTS_SHEET = "https://docs.google.com/spreadsheets/d/1t-W9RcsgEuTvNbwB9dRMfoMKjoN8kyJFJeLcHfiO8rs/edit#gid=0"
RECENT_POINTS_SHEET = "https://docs.google.com/spreadsheets/d/1t-W9RcsgEuTvNbwB9dRMfoMKjoN8kyJFJeLcHfiO8rs/edit#gid=1159651787"

@app.route('/')
def home():
    return render_template('home.html')

# going REST api approach to give data to John's react app
@app.route('/api/<name>', methods=['GET'])
def api(name):
    data = findNameAndPoints(name)

    if data != None:
        retData = dict()
        retData['name'] = data[0]
        retData['totalPoints'] = data[1]
        retData['mostRecentlyAddedPoints'] = data[2]
        return jsonify(retData)
    else:
        return jsonify({'name':'None','points': 'None', 'mostRecentlyAddedPoints': 'None'})

def getTotalPoints(name):
    # second sheet on the google sheet
    sheet_url = TOTAL_POINTS_SHEET
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    records = df.to_dict('records')

    ## The first one is the empty field, so we don't care about that
    del records[0]

    for r in records:
        if name == r['name']:
            return int(r['sum points'])

    return None

def getMostRecentAddedPoints(name):
    ## third sheet on the google sheet
    sheet_url = RECENT_POINTS_SHEET
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    records = df.to_dict('records')

    for r in records:
        if name == r['name']:
            return int(r['points'])

    return None

def findNameAndPoints(name):
    total = getTotalPoints(name)
    recentAdd = getMostRecentAddedPoints(name)

    if total != None and recentAdd != None:
        return (name, total, recentAdd)

    return None

if __name__ == '__main__':
    app.run()
