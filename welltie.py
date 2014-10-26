from flask import *
from synth import generate_reflectivity, plot_logs, plot_spectrum
from StringIO import StringIO 

app = Flask(__name__)

def generate_image():
    t, RC_t = generate_reflectivity()

    buffer = StringIO()

    preview_kind = request.args['type'] 
    if preview_kind == 'reflectivity':
        plot_logs(buffer, 'png', t, RC_t, RC_t, start=1.4, end=2.5, title='Reflectivity') 
    elif preview_kind == 'spectrum':
        plot_spectrum( buffer, 'png', RC_t, title='Spectrum')
    else:
        raise Exception("Unknown preview type \"" + preview_kind + "\"") 

    return buffer.getvalue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    png_data = generate_image()
    response = make_response(png_data)
    response.headers['Content-Type'] ='image/png'
    return response
    

if __name__ == '__main__':
    app.run(debug=True)
