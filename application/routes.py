
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
def get_website_data():
    if request.method == 'POST':
        return jsonify(ping_pi.get_website_data(request.get_json()))
    else:
        return 'Failed'

@app.route('/add-website', methods=['GET', 'POST'])
def add_website():
    if request.method == 'POST':
        return ping_pi.add_website(request.get_json())
    else:
        return 'Failed'

@app.route('/delete-website', methods=['GET', 'POST'])
def delete_website():
    if request.method == 'POST':
        return ping_pi.delete_website(request.get_json())
    else:
        return 'Failed'

@app.route('/edit-website', methods=['GET', 'POST'])
def edit_website():
    if request.method == 'POST':
        return ping_pi.edit_website(request.get_json())
    else:
        return 'Failed'

@app.route('/get-time-til-ping', methods=['GET', 'POST'])
def get_time_til_ping():
    if request.method == 'POST':
        return jsonify(ping_pi.get_time_til_next_ping(request.get_json()))
    else:
        return 'Failed'
