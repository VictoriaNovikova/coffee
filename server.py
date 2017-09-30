from flask import Flask, abort, request
from html_source_page import html_page
app = Flask(__name__)



api_key='AIzaSyAsXD-BYYqu4ImlaIrfcSuzl-13rwyaiOA'
@app.route('/')
def index_page():
    return html_page

if __name__ == "__main__":
    app.run()