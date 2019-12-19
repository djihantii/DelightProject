# from flask import Flask, render_template, request, json
# import requests
# from flask_accept import accept
# api_key = "b3d347b0f52ffcb1c34c9a6f1f60c03a"
# # Create the application instance
# app = Flask(__name__)
# def build_graphs(x_coordinate, y_coordinate, indiceName):
#
#
#
# @app.route("/home" , methods=['POST' , 'GET'])
#
# def temperature():
#     file = open("contributors_list", "w")
#
#     # zipcode = request.form['zip']
#     # r = requests.get('https://samples.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid='+api_key+'')
#     response_all_commits = requests.get('https://api.github.com/repos/Facebook/react/commits?since=2019-12-12T00:00:00Z', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_commit_per_hour = requests.get('https://api.github.com/repos/Facebook/react/stats/punch_card?since=2019-12-08', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_commit_per_week = requests.get('https://api.github.com/repos/Facebook/react/stats/participation', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_contributors = requests.get('https://api.github.com/repos/Facebook/react/stats/contributors', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_repository = requests.get('https://api.github.com/repos/Facebook/react', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_commits_year_activity = requests.get('https://api.github.com/repos/Facebook/react/stats/commit_activity', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#     response_project_contributors = requests.get('https://api.github.com/repos/Facebook/react/contributors', params={'q': 'requests+language:python'},headers={'Accept': "application/vnd.github.cloak-preview" , 'Accept' : 'application/vnd.github.v3+json'})
#
#     json_object = json.dumps(response_all_commits.text)
#     data = response_all_commits.json()
#
#     json_object2 = json.dumps(response_commit_per_week.text)
#     data2 = response_commit_per_week.json()
#
#     #list des contributions + detail contributeur
#     json_contributors = json.dumps(response_contributors.text)
#     data_contributors = response_contributors.json()
#
#     json_year_activity = json.dumps(response_commits_year_activity.text)
#     data_year_activity = response_commits_year_activity.json()
#
#
#     #Liste des contributeurs avec total contributions sans details
#     data_list_contributors = response_project_contributors.json()
#     data_repository = response_repository.json()
#     # test = data[0]["sha"]
#     # my_dict = json.loads(json_object)
#     leng = len(data)
#     # keys = my_dict.keys()
#
#     data_per_hour = response_commit_per_hour.json()
#
#     data_all_commits = response_all_commits.json()
#     test = response_all_commits.text
#     file.write(response_contributors.text)
#     file.close()
#     return data_list_contributors
#
# @app.route("/")
# def index():
#     return render_template("index.html")
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms.fields import DateField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
Bootstrap(app)

class MyForm(Form):
    date = DateField(id='datepick')

@app.route('/')
def index():
    form = MyForm()
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
