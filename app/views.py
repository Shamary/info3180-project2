"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app,db,login_m
from flask import render_template, request, redirect, url_for, jsonify, Response, flash
from bs4 import BeautifulSoup
from flask_login import login_user, logout_user, current_user, login_required
import requests
import urlparse


from image_getter import *
from forms import *
from models import User


###
# Routing for your application.
###

#@app.route('/')
#def index():
    #"""Render website's home page."""
    #return app.send_static_file('index.html')
    

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/register')
def register():
    form=RegisterForm()
    return render_template("register.html",form=form);

@app.route('/api/users/register', methods=['POST'])
def signup():
        #write to db
        fname=request.form['fname']
        lname=request.form['lname']
        gender=request.form['gender']
        age=request.form['age'];
        uname=request.form['uname']
        pwd=request.form['password']
        
        user=User(fname=fname,lname=lname,age=age,gender=gender,uname=uname,password=pwd)
        
        db.session.add(user)
        db.session.commit()
        #pass
        
        #return response
        #res={"error":None,"status":"OK","message":"Success"}
        
        #return res;



@app.route('/api/users/login',methods=["POST"])
def login():
    pass

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.uname.data
        password = form.password.data
        
        user = User.query.filter_by(username=username, password=password).first()
        
        if user is not None:
        
            login_user(user)
            flash('Login Successful','success')
            return redirect(url_for(''))
    
    return render_template("login.html",form=form)
    
    
@login_m.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    
    
@app.route('/api/users/logout',methods=["POST"])
def logout():
    logout_user()
    flash('User Logged out','success')
    return render_template("home.html")

    
@app.route('/api/users/<userid>/wishlist',methods=["GET","POST"])
def wishes(userid):
    pass
    
@app.route('/api/thumbnails',methods=["GET"])
def get_images():
    if(request.method=="GET"):
        url="https://www.walmart.com/ip/54649026"#default
        soup=work_on(url)
        lst=getLst(soup)
        
        msg={"error":None,"message":"Success","thumbnails":lst}
        
        return jsonify(msg)
    #pass



@app.route('/thumbnails/view')
def tview():
    return render_template("thumb.html")

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
