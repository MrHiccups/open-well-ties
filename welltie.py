from flask import Flask, render_template
from synth.synth import generate_reflectivity, plot_logs
from StringIO import StringIO 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    buffer = StringIO()
    t, RC_t = generate_reflectivity()
    start_z = 2300
    end_z = 2600

    start_t = 1.4
    end_t = 2.5
    plot_logs(buffer, 'png', t, RC_t, RC_t, start_t, end_t, title='synthetic')
    return buffer.getvalue()
    

if __name__ == '__main__':
    app.run(debug=True)
