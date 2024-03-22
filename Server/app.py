from flask import Flask


app = Flask(__name__)

@app.route('/')

def hello():
    return 'Hello'

@app.route('/sample')
def helloSample():
    return 'Hello sample'



if __name__ == '__main__':
    app.run(debug =True)
