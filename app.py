from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bandit@localhost/kick'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class feedback(db.Model):
    __tableName__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='I guess you missed a field')

        if db.session.query(feedback).filter(feedback.customer == customer).count() == 0:
            data = feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')

        else:
            return render_template('index.html', message="You've submitted feedback already!")


if __name__ == '__main__':
    app.run()
