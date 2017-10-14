from flask import Flask, abort, request, render_template
from jinja2 import Template
import requests

app = Flask(__name__)

api_key='AIzaSyAsXD-BYYqu4ImlaIrfcSuzl-13rwyaiOA'

def get_cafe_json():
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&location={lat},{lng}&radius=500&type=cafe".format(api_key=api_key, lat=55.740750, lng=37.608874)
    
    print(url)
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        print("Something went wrong...")


@app.route('/')
def index_page():
    return render_template('index_page.html')

@app.route('/coffee/')
def cofee_info_page():
    return render_template('coffee_info_page.html')

@app.route('/login/', methods=['POST'])
def login_page():
    return render_template('login.html', email=request.form.get('email'), password=request.form.get('password'))

if __name__ == "__main__":
    app.run()