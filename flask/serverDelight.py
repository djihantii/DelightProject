from flask import Flask, render_template, request, json, url_for
import requests
import json
from flask_accept import accept
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import os
import io
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import DateField
import calendar

app = Flask(__name__)

class Formatted_data:
    contributors = []
    total_commits = []
    weeks = []
    details_participation = []
    total_weeks = 0

app.config['SECRET_KEY'] = 'SHH'


def build_graph(x_coordinates_interval , y_coordinates , indiceName , title):

    fig = plt.figure()
    x = pd.date_range(x_coordinates_interval[0] , x_coordinates_interval[1] , freq='W-SUN')
    print("longueur date = "+str(len(x)))
    print("longueur y = "+str(len(y_coordinates)))
    plt.plot(x, y_coordinates)
    plt.xticks(rotation=45)
    ax=plt.gca()
    ax.set_title(title)
    #We count the difference between start date and end date
    temp_start = date.fromisoformat(x_coordinates_interval[0])
    temp_end = date.fromisoformat(x_coordinates_interval[1])

    delta = (temp_end - temp_start).days
    if delta < 70:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=SU))
    elif (delta < 365 and delta >69):
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    else:
        ax.xaxis.set_major_locator(mdates.YearLocator())

    name = "myFig"+indiceName+""
    plt.savefig("static/"+name , format='png')
    return name

def build_list_graphs(contribution_class, list_contributors , start_date, end_date):
    graphs = []
    max_graphs = 9
    for i in range(0, max_graphs):
        index = list_contributors[i][0]
        details_per_contributor = detail_contribution_in_period(index, start_date, end_date, contribution_class)
        graphs.append(build_graph([start_date, end_date], details_per_contributor, str(i), contribution_class.contributors[index][0]) )

    return graphs



def index_from_array(motif , array):
    for i in range(0, len(array)):
        if array[i]==motif:
            return i
    return -1;

def date_from_timestamp(date):
    readable = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    return readable

def timestamp_from_date(date_timestamp):
    temp = datetime.strptime(date_timestamp , "%Y-%m-%d %H:%M:%S")
    timeStamp = calendar.timegm(temp.utctimetuple())
    return timeStamp

def sort_table_contributors_descending(contributors_table):
    result = sorted(contributors_table , key=lambda x : x[1] , reverse = True)
    return result

def total_contributions_in_period(start_week, end_week, contributors):
    #Counts the sum of commits of each contributor in a given period
    #Sort the list of contributors depending on their sum of commits
    #So we can start inserting by contributors with higher commits
    #Each element of the table contains a tuple (index_of_contributor, Sum)
    logCon = open("logcontr" , "w")
    sentence = "start date ==> "+start_week+"  and en ==> "+end_week+""
    logCon.write(sentence)

    result_contributors = []
    sum = 0
    timestamp_start = timestamp_from_date(""+start_week+" 00:00:00")
    timestamp_end = timestamp_from_date(""+end_week+" 00:00:00")
    index_start = index_from_array(timestamp_start , contributors.weeks)
    index_end = index_from_array(timestamp_end , contributors.weeks)

    for i in range(0, len(contributors.contributors)):
        for j in range (index_start, index_end):
            sum = sum + contributors.details_participation[i][j][2]
        result_contributors.append((contributors.contributors[i][2] , sum))
        sum = 0

    logCon.write(str(sort_table_contributors_descending(result_contributors)))
    logCon.close()
    return sort_table_contributors_descending(result_contributors)

def detail_contribution_in_period(contributor_index, start_date , end_date , contributors):
    #For a given contributor in a precised period we give the list of his commits
    # Used to draw graphs
    details = []
    timestamp_start = timestamp_from_date(""+start_date+" 00:00:00")
    timestamp_end = timestamp_from_date(""+end_date+" 00:00:00")
    index_start = index_from_array(timestamp_start, contributors.weeks)
    index_end = index_from_array(timestamp_end , contributors.weeks)

    for i in range(index_start,index_end+1 ):
        details.append(contributors.details_participation[contributor_index][i][2])

    return details


def data_for_graphs(data_list_contributors , quantity):
    commits = []
    contributors = []
    for i in range(0, quantity):
        contributors.append(data_list_contributors[0][i])
        commits.append(data_list_contributors[1][i])

    return((contributors , commits))

def first_sunday_from_day(dateWeek):
    d = date.fromisoformat(dateWeek)

    while d.weekday() != 6:
        d -=timedelta(days=1)

    return d


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
        data_to_class.contributors.append((data[i]["author"]["login"] ,data[i]["author"]["id"] , i))
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
def index():
    nameFile = "contributors_list.json"
    file = open(nameFile, "w")

    response_contributors = requests.get('https://api.github.com/repos/Facebook/react/stats/contributors', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})

    file.write(response_contributors.text)
    file.close()

    data_to_class = format_File(nameFile)
    start_date = date_from_timestamp(data_to_class.weeks[0])
    end_date = date_from_timestamp(data_to_class.weeks[-1])


    date = [start_date, end_date]
    total_commits = get_total_Commits(data_to_class)
    image = build_graph(date,total_commits , "Total", "Total_activity" )

    list_contributors = total_contributions_in_period(start_date, end_date, data_to_class)
    graphs = build_list_graphs(data_to_class, list_contributors, start_date, end_date)


    return render_template("index.html" , image = image , image1 = graphs[0], image2 = graphs[1], image3 = graphs[2], image4 = graphs[3], image5 = graphs[4], image6 = graphs[5], image7 = graphs[6], image8 = graphs[7], image9 = graphs[8])


@app.route("/indexDelight.html" , methods=['post', 'get'])
def contributions():

    logFile = open("log", "w")
    nameFile = "contributors_list.json"
    data_to_class = format_File(nameFile)

    starts = request.form["vizualisation_start"]
    ends = request.form["vizualisation_end"]
    start_date = first_sunday_from_day(starts).strftime("%Y-%m-%d")
    end_date = first_sunday_from_day(ends).strftime("%Y-%m-%d")
    sentence = "start date ==> "+start_date+"  and en ==> "+end_date+""
    logFile.write(sentence)

    list_contributors = total_contributions_in_period(start_date, end_date, data_to_class)
    logFile.write(str(list_contributors))
    logFile.close()
    graphs = build_list_graphs(data_to_class, list_contributors, start_date, end_date)

    total_commits = get_total_Commits(data_to_class)

    repo_creation = date_from_timestamp(data_to_class.weeks[0])
    repo_now = date_from_timestamp(data_to_class.weeks[-1])

    image = build_graph([repo_creation, repo_now],total_commits , "Total", "Total_activity" )

    return render_template('indexDelight.html' , image=image , image1 = graphs[0], image2 = graphs[1], image3 = graphs[2], image4 = graphs[3], image5 = graphs[4], image6 = graphs[5], image7 = graphs[6], image8 = graphs[7], image9 = graphs[8])
if __name__ == '__main__':


    # nameFile = "contributors_list.json"
    # data_to_class = format_File(nameFile)
    # start_date = first_sunday_from_day('2019-10-29').strftime("%Y-%m-%d")
    # end_date = first_sunday_from_day('2019-12-20').strftime("%Y-%m-%d")
    # sentence = "start date ==> "+start_date+"  and en ==> "+end_date+""
    #
    # list_contributors = total_contributions_in_period(start_date, end_date, data_to_class)
    #
    # graphs = build_list_graphs(data_to_class, list_contributors, start_date, end_date)
    #
    # total_commits = get_total_Commits(data_to_class)
    #
    # repo_creation = date_from_timestamp(data_to_class.weeks[0])
    # repo_now = date_from_timestamp(data_to_class.weeks[-1])
    #
    # image = build_graph([repo_creation, repo_now],total_commits , "Total", "Total_activity" )

    app.run(debug=True)
