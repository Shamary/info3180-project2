"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_m
from flask import render_template, request, redirect, url_for, jsonify, Response, flash,session
from bs4 import BeautifulSoup
from flask_login import login_user, logout_user, current_user, login_required
import requests
import urlparse
import smtplib
import random

from image_getter import *
from forms import *
from models import User,Wish


###
# Routing for your application.
###

#@app.route('/')
#def index():
    #"""Render website's home page."""
    #return app.send_static_file('index.html')
 
 
######    
#HTML Routes
######

#user=""

@app.route('/')
def home():
    """Render website's home page."""
    if (current_user.is_authenticated):
        page = 'secure_page'
    else:
        return render_template('home.html')
    return redirect(url_for(page))


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')



@app.route('/addItem',methods=['POST','GET'])
def add_item():
    return render_template('add_item.html')



@app.route('/register')
def register():
    form=RegisterForm()
    return render_template("register.html",form=form);



@app.route('/login', methods=["GET"])
def loginUI():
    #form = LoginForm()
    return render_template("login.html")


@app.route('/secure-page')
@login_required
def secure_page():
    return render_template("secure-page.html")

######   
#API Routes
######
@app.route('/api/users/register', methods=["POST"])
def signup():
    # form = RegisterForm()
    
    # fname = form.fname.data
    # lname = form.lname.data
    # gender = form.gender.data
    # age = form.age.data
    # uname = form.username.data
    # pwd = form.password.data
    # ispwd = form.ispassword.data
    
    uid = random.randint(1000,1999)
    #write to db
    fname=request.form['fname']
    lname=request.form['lname']
    gender=request.form['gender']
    age=request.form['age'];
    uname=request.form['uname']
    pwd=request.form['password']
    
    # if pwd == ispwd:
        
    user=User(userid=uid,fname=fname,lname=lname,age=age,sex=gender,uname=uname,password=pwd)
    db.session.add(user)
    db.session.commit()
    flash('User Profile Added','success')
    return url_for('loginUI')
        
    # else:
    #     flash('Incorrect password entered')
    #     return redirect(url_for('register'))
    
    #pass

    #return response
    #res={"error":None,"status":"OK","message":"Success"}
    
    


@app.route('/api/users/login',methods=["POST"])
def login():
    #form = LoginForm()
    
    uname = request.form['uname']
    password = request.form['password']
    
    user = User.query.filter_by(uname=uname, password=password).first()
    
    if (user):
    
        login_user(user)
        flash('Login Successful','success')
        
        uid=User.query.filter_by(uname=uname).with_enities(User.userid)
        session['username']=uname
        session['uid']=uid
        
        
        return url_for('secure_page')#returns the url to angular
        #return jsonify({"Success":"True"})
    else:
        flash('Username or Password is incorrect','danger')
        return url_for('loginUI')
        #return jsonify({"Success":"False"})
            
    
    
    
@app.route('/api/users/logout')#,methods=["POST"])
@login_required
def logout():
    logout_user()
    flash('User '+session['username']+' Logged out ','success')
    session.clear()
    return redirect(url_for('home'))

  
    
@app.route('/api/users/<userid>/wishlist',methods=["GET","POST"])
def wishes(userid):
    
    if(request.method=="POST"):
        iname=request.form['iname']
        url=request.form['url']
        
        wish=Wish(userid=userid,item_name=iname,item_url=url)
        
        db.session.add(wish)
        db.session.commit()
    else:
        wish=Wish.query.filter_by(userid=userid)
        
        return wish
    
    
    
@app.route('/api/thumbnails',methods=["GET"])
def get_images():
    if(request.method=="GET"):
        url=request.args.get('url')
        #url="https://www.tripadvisor.com/Hotel_Review-s1-g147312-d503026-Reviews-Rooms_Ocho_Rios-Ocho_Rios_Saint_Ann_Parish_Jamaica.html"#default
        #url=request.form['url']
        soup=work_on(url)
        lst=getLst(soup)
        
        msg={"error":None,"message":"Success","thumbnails":lst}
        
        return jsonify(msg)
    #pass



@app.route('/api/users/{userid}/wishlist/{itemid}', methods=["DELETE"])
def delete_wish():
    pass



@app.route('/thumbnails/view')
def tview():
    return render_template("thumb.html")
    


@login_m.user_loader
def load_user(id):
    return User.query.get(int(id))
    


def share_wishlist():
    
    from_addr = request.form['']
    to_addr = ''
    to_name=''
    subject=''
    message_to_send = message.format(from_name, from_addr, to_name,to_addr,subject, msg)
    # Credentials (if needed)
    username = ''
    password = ''
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_addr, message_to_send)
    server.quit()
    


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
