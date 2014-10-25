from flask import Flask, render_template
from evans_workflow import flow
from StringIO import StringIO 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    buffer = StringIO()
    flow.plot('evans_workflow/L-30.las',buffer)
    return buffer.getvalue()
    

if __name__ == '__main__':
    app.run(debug=True)
