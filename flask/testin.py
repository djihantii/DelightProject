from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/testin.html', methods = ['POST', 'GET'])
def testin():
    starts = request.form["vizualisation_start"]
    ends = request.form["vizualisation_end"]
    return render_template('testin.html' , starts = starts, ends = ends)


@app.route('/')
def indexTestin():
   return render_template('indexTestin.html')


if __name__ == '__main__':
   app.run(debug = True)
