from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html', title = 'Home')





@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name, title='hi')


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)