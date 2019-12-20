#!bin/env python3
import requests
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import os


def extract_data(repos, project):
    yesterday = date.today() - timedelta(days=1)
    yest_date = yesterday.strftime('%Y-%m-%d')
    response_commits = requests.get('https://api.github.com/repos/'+repos+'/'+project+'/commits?since='+yest_date+'', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
    return response_commits.json()

def count_commits(response_commits):
    number_commits = len(response_commits)
    commiters = []
    for i in range(0, number_commits):
        commiters.append(response_commits[0]["commit"]["author"])

    return ((number_commits, commiters))

def evaluate_commits(response_commits):
    details = count_commits(response_commits)
    yesterday = date.today() - timedelta(days=1)
    yest_date = yesterday.strftime('%Y-%m-%d')

    if details[0] < 2 :
        cwd = os.getcwd()
        fileLog = open(str(cwd)+"/log", "a")
        fileLog.write(""+yest_date+" their was "+ str(details[0])+" commits and authors are : \n")
        for commiter in range(0, details[0]):
            fileLog.write(str(details[1][commiter]))
        fileLog.close()

if __name__ == "__main__":

    data = extract_data('Facebook', 'react')
    evaluate_commits(data)
