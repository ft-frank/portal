from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html', title = 'Home')

@app.route('/invoices')
def invoices():
    return render_template('invoices.html', title = 'Invoices')

@app.route('/homework')
def homework():
    return render_template('homework.html', title='Homework')

@app.route('/questions')
def questions():
    return render_template('questions.html', title='Questions')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Settings')

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)