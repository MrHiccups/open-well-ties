from flask import *
from synth import generate_reflectivity, plot_logs, plot_spectrum
from StringIO import StringIO 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    t, RC_t = generate_reflectivity()

    buffer = StringIO()

    preview_kind = request.args['type'] 
    if preview_kind == 'reflectivity':
        plot_logs(buffer, 'png', t, RC_t, RC_t, start=1.4, end=2.5, title='reflectiviy') 
    elif preview_kind == 'spectrum':
        plot_spectrum( buffer, 'png', RC_t)
    else:
        raise Exception("Unknown preview type \"" + preview_kind + "\"") 

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] ='image/png'
    return response
    

if __name__ == '__main__':
    app.run(debug=True)
