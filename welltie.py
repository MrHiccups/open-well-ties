from flask import Flask, render_template, make_response
from synth.synth import generate_reflectivity, plot_logs
from StringIO import StringIO 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    t, RC_t = generate_reflectivity()
    start_z = 2300
    end_z = 2600

    start_t = 1.4
    end_t = 2.5

    buffer = StringIO()
    plot_logs(buffer, 'png', t, RC_t, RC_t, start_t, end_t, title='reflectiviy') 
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] ='image/png'
    return response
    

if __name__ == '__main__':
    app.run(debug=True)
