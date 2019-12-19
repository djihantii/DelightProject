from flask import Flask, render_template, request, json, url_for
import requests
import json
from flask_accept import accept
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime
import time
import os
import io
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import DateField

app = Flask(__name__)

class Formatted_data:
    contributors = []
    total_commits = []
    weeks = []
    details_participation = []
    total_weeks = 0

app.config['SECRET_KEY'] = 'SHH'


class DateForm(FlaskForm):
    dt = DateField('Pick a Date', format="%Y-%m-%d")

def build_graph(x_coordinates_interval , y_coordinates , indiceName):
    fig = plt.figure()
    x = pd.date_range(x_coordinates_interval[0] , x_coordinates_interval[1] , freq='W-SUN')
    print("longueur date = "+str(len(x)))
    print("longueur y = "+str(len(y_coordinates)))
    plt.plot(x, y_coordinates)
    plt.xticks(rotation=45)
    ax=plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    name = "myFig"+indiceName+""
    plt.savefig("static/"+name , format='png')
    return name

def index_from_array(motif , array):
    for i in range(0, len(array)):
        if array[i]==motif:
            return i
    return -1;

def date_from_timestamp(date):
    readable = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    return readable

# def draw_plots(numberGraphs, contributors_table, ):


def contributions_in_period(start_week, end_week, contributors):
    result_contributors = []
    sum = 0
    index_start = index_from_array(start_week, contributors.weeks)
    index_end = index_from_array(end_week, contributors.weeks)

    for i in range(0, len(contributors.contributors)):
        for j in range (index_start, index_end):
            sum = sum + contributors.details_participation[i][j][2]
        result_contributors.append((contributors.contributors[i] , sum))
        sum = 0
    return result_contributors



def sort_table_contributors_descending(contributors_table):
    result = sorted(contributors_table , key=lambda x : x[1] , reverse = True)
    return result


def format_File(fileTitle):
    file = open(fileTitle , "r")
    data = json.load(file)

    data_to_class = Formatted_data()
    print("taille data = "+str(len(data[0]["weeks"])))
    weeks_list = []
    contributors = []
    week_details = []
    contributor_details = []
    data_to_class.total_weeks = len(data[0]["weeks"])
    for i in range(0, len(data)):
        data_to_class.contributors.append((data[i]["author"]["login"] ,data[i]["author"]["id"] ))
        # contributor_details.append(data[i]["author"]["login"])
        # contributor_details.append(data[i]["author"]["id"])
        data_to_class.total_commits.append(data[i]["total"])
        # weeks_list.append(data[i]["total"])
        for j in range(0, len(data[i]["weeks"])):

            week_details.append(data[i]["weeks"][j]["a"])
            week_details.append(data[i]["weeks"][j]["d"])
            week_details.append(data[i]["weeks"][j]["c"])

            weeks_list.append(week_details)
            week_details=[]
            # print("then "+str(len(week_details)))

        data_to_class.details_participation.append(weeks_list)
        # contributors.append((weeks_list , contributor_details))
        weeks_list=[]
        # contributor_details=[]
    for i in range(0, data_to_class.total_weeks):
        data_to_class.weeks.append(data[0]["weeks"][i]["w"])
    file.close()

    return data_to_class

def get_total_Commits(contributors):
    commits_per_week=[]
    sum = 0

    for i in range(0, contributors.total_weeks):
        for j in  range(0, len(contributors.contributors)):
            sum = sum + contributors.details_participation[j][i][2]
        commits_per_week.append(sum)
        sum = 0
    return commits_per_week

@app.route("/" , methods=['post' , 'get'])
def temperature():
    nameFile = "contributors_list.json"
    file = open(nameFile, "w")

    # zipcode = request.form['zip']
    # r = requests.get('https://samples.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid='+api_key+'')
    # response_all_commits = requests.get('https://api.github.com/repos/Facebook/react/commits?since=2019-12-12T00:00:00Z', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    # response_commit_per_hour = requests.get('https://api.github.com/repos/Facebook/react/stats/punch_card?since=2019-12-08', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    # response_commit_per_week = requests.get('https://api.github.com/repos/Facebook/react/stats/participation', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})

    response_contributors = requests.get('https://api.github.com/repos/Facebook/react/stats/contributors', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    # response_repository = requests.get('https://api.github.com/repos/Facebook/react', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    # response_commits_year_activity = requests.get('https://api.github.com/repos/Facebook/react/stats/commit_activity', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    # response_project_contributors = requests.get('https://api.github.com/repos/Facebook/react/contributors', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})



    file.write(response_contributors.text)
    file.close()
    data_to_class = format_File(nameFile)
    date = ['2013-05-26', '2019-12-19']
    total_commits = get_total_Commits(data_to_class)
    image = build_graph(date,total_commits , "Total" )

    form1 = DateForm()
    form2 = DateForm()
    if form1.validate_on_submit():
        return form1.dt.data.strftime('%x')
    if form2.validate_on_submit():
        return form2.dt.data.strftime('%x')
    return render_template("indexDelight.html" , image = image , form1=form1 , form2=form2)

if __name__ == '__main__':


    app.run(debug=True)
