from flask import Flask,url_for,render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = "盧宗基"
    age = 25
    return render_template('index.html',name=name,age=age)
