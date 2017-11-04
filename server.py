from flask import Flask, abort, request, render_template, session, redirect, g, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required

from jinja2 import Template
import requests
from social_flask.routes import social_auth
from social_flask_sqlalchemy.models import init_social
from db import User, db_session, Cafe
import json
from fullfill_db import get_nearest_cafe, get_cafe_json

app = Flask(__name__)
app.config.from_object('config')
# app.config['SOCIAL_AUTH_USER_MODEL'] = 'db.User'
# app.register_blueprint(social_auth)

# init_social(app, session)

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "login"

CURRENT_USER = User()

@app.before_request
def global_user():    
    g.user = CURRENT_USER


@login_manager.user_loader
def load_user(userid):
    try:
        return User.query.get(userid)
    except:
        pass


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


@app.route('/')
def index_page():
    return render_template('index_page.html', user=g.user)


@app.route('/coffee/')
def cofee_info_page():
    return render_template('coffee_info_page.html', user=g.user)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('password')
    found_user = User.query.filter(User.email == email and User.password == pwd).first()
    if found_user:   
        login_user(found_user)
        g.user = found_user             
        return redirect('profile/{}'.format(found_user.id))
    else:
        return redirect('registration')


@app.route('/registrate', methods=['POST'])
def registrate():
    email = request.form.get('email')    
    password = request.form.get('password')    
    first_name = request.form.get('first_name')    
    last_name = request.form.get('last_name')    
    new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)    
    print(new_user)
    db_session.add(new_user)
    db_session.commit()    
    login_user(new_user)
    g.user = new_user
    print(g.user)
    return redirect('profile/{}'.format(g.user.id))


@app.route('/registration')
def registration_page():
    return render_template('registration.html', user=g.user)


@app.route('/logout')
def logout_page():
    print(g.user)
    logout_user()
    return 'Logged out'


@app.route('/profile/<int:user_id>')
@login_required
def profile_page(user_id):
    user = User.query.get(user_id)
    if user is None:
        print('User with id as {} not found'.format(user_id))
        return render_template('404.html', text="Это не тот пользователь, которого ты ищешь", img_link="http://cdn2.s.kolorado.ru/products/1/14/143/143736/101_1_14_design.png")
    return render_template('profile.html', user=user)


@app.route('/points/', methods=['GET'])
def get_cafes():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except:
        lat = 55.740750
        lng = 37.608874
    
    cafes = get_nearest_cafe(lat,lng)    
    return render_template('cafes.html', cafes=cafes)


@app.route('/points-result-json/', methods=['GET'])
def get_maps_json():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except:
        lat = 55.740750
        lng = 37.608874
    
    cafes = get_nearest_cafe(lat,lng)
    cafes_json = []
    for cafe in cafes:
        cafes_json.append((cafe.name, cafe.lat, cafe.lng))
    return jsonify(cafes=cafes_json)

@app.route('/cafes/<int:cafe_id>')
def cafe_info_page(cafe_id):    
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return render_template('404.html', text="", img_link="https://cdn.dribbble.com/users/469578/screenshots/2597126/404-drib23.gif")
    return render_template('cafe_info_page.html', cafe=cafe)


@app.errorhandler(404)
def not_found_page(e):
    return render_template('404.html', text="", img_link="https://cdn.dribbble.com/users/469578/screenshots/2597126/404-drib23.gif"), 404

if __name__ == "__main__":
    app.run()