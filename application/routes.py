
from application import app
from application import ping_pi
from flask import render_template, request, jsonify

@app.route('/')
def index():
    data = {
        'sites' : ping_pi.get_all_websites()
    }
    return render_template('index.html', data=data)


#---------- AJAX ---------

@app.route('/get-website-data', methods=['GET', 'POST'])
def get_website():
    if request.method == 'POST':
        return jsonify(ping_pi.get_website_data(request.get_json()))
    else:
        return 'Failed'
