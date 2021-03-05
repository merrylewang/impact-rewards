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
@app.route('/api/<email>', methods=['GET'])
def api(email):
    data = findNameAndPoints(email)

    if data != None:
        retData = dict()
        retData['name'] = data[0]
        retData['email'] = data[1]
        retData['totalPoints'] = data[2]
        retData['mostRecentlyAddedPoints'] = data[3]
        return jsonify(retData)
    else:
        return jsonify({'name':'None','email':'None', 'points': 'None', 'mostRecentlyAddedPoints': 'None'})

def getTotalPointsAndName(email):
    # second sheet on the google sheet
    sheet_url = TOTAL_POINTS_SHEET
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    records = df.to_dict('records')
    print(records)
    ## The first one is the empty field, so we don't care about that
    del records[0]

    def clean_records(records):
        """Helper function to clean the keys"""
        return [{k.strip(): v for (k, v) in record.items()} for record in records]
    records = clean_records(records)

    for r in records:
        if email == r['email']:
            return (r['name'], int(r['sum points']))

    return (None, None)

def getMostRecentAddedPoints(email):
    ## third sheet on the google sheet
    sheet_url = RECENT_POINTS_SHEET
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    records = df.to_dict('records')

    for r in records:
        if email == r['email']:
            return int(r['points'])

    return None


def findNameAndPoints(email):
    name, total = getTotalPointsAndName(email)
    recentAdd = getMostRecentAddedPoints(email)

    if total != None and recentAdd != None:
        return (name, email, total, recentAdd)

    return None

if __name__ == '__main__':
    app.run()
