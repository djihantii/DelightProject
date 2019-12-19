from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import DateField
from datetime import date

app = Flask(__name__)
app.secret_key = 'SHH!'


class DateForm(FlaskForm):
    dt = DateField('Pick a Date', format="%m/%d/%Y")


@app.route('/', methods=['post','get'])
def home():
    form = DateForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%x')
    return render_template('vort.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
