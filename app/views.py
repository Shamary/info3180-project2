"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_m
from flask import render_template, request, redirect, url_for, jsonify, Response, flash, session
from bs4 import BeautifulSoup
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import urlparse
import smtplib
import random

from image_getter import *
#from forms import *
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
@login_required
def wishlist():
    return render_template('wishlist.html')



@app.route('/addItem',methods=['POST','GET'])
def add_item():
    return render_template('add_item.html')



@app.route('/register')
def register():
    return render_template("register.html");



@app.route('/login', methods=["GET"])
def loginUI():
    return render_template("login.html")



@app.route('/secure-page')
@login_required
def secure_page():
    return render_template("secure-page.html")



@app.route('/share')
@login_required
def share_wishlist():
    if (request.method == 'POST'):
        to_name=request.form['name']
        to_addr=request.form['to_addr']
        share(to_name, to_addr)
        flash('Message Sent Successfully','success')
        return url_for('home')
    else:
        
        flash('Message Not Sent','danger')
        return url_for('share_wishlist')
        
    return render_template("share.html")


######   
#API Routes
######
@app.route('/api/users/register', methods=["POST"])
def signup():
    
    uid = random.randint(1000,1999)
    #write to db
    fname=request.form['fname']
    lname=request.form['lname']
    gender=request.form['gender']
    age=request.form['age'];
    uname=request.form['uname']
    pwd=request.form['password']
    ispwd=request.form['ispassword']
    
    if (pwd == ispwd):
        hash_pwd = generate_password_hash(pwd,method='pbkdf2:sha1',salt_length=8)
        
        user=User(userid=uid,fname=fname,lname=lname,age=age,sex=gender,uname=uname,password=hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash('User Profile Added','success')
        return url_for('loginUI')
        
    else:
        print('failure')
        flash('Incorrect password entered','danger')
        return url_for('register')
    
    


@app.route('/api/users/login',methods=["POST"])
def login():
    
    uname = request.form['uname']
    password = request.form['password']
    
    user = User.query.filter_by(uname=uname).first()
    temp = user.password
    
    if (user and check_password_hash(temp, password)):
    
        login_user(user)
        flash('Login Successful','success')
        
        session['username']=uname
        session['uname']=user.fname+" "+user.lname
        session['uid']=user.userid
        
        #token=generate_token()
        
        return url_for('secure_page',userid=current_user.get_id())#returns the url to angular
        #return jsonify({"Success":"True"})
    else:
        flash('Username or Password is incorrect','danger')
        return url_for('loginUI')
        #return jsonify({"Success":"False"})
            
    

@app.route('/gsession')
def gsession():
    return str(session['uid'])
    
    
    
@app.route('/api/users/logout')#,methods=["POST"])
@login_required
def logout():
    logout_user()
    flash('User '+session['username']+' Logged out ','success')
    
    #####cleanup session
    session.pop('username',None)
    session.pop('uid',None)
    session.pop('uname',None)
    
    return redirect(url_for('home'))

  
    
@app.route('/api/users/<userid>/wishlist',methods=["GET","POST"])
def wishes(userid):
    
    iid=random.randint(1000,9999)
    if(request.method=="POST"):
        
        iname=request.form['iname']
        url=request.form['url']
        
        userid=session['uid'];
        
        wish=Wish(itemid=iid,userid=userid,item_name=iname,item_url=url)
        
        db.session.add(wish)
        db.session.commit()
        
        flash("Item added");
        
        return "OK"
        
    else:
        wish=Wish.query.filter_by(userid=userid)
        
        url=[]
        names=[]
        img_ids=[]
        
        for u in wish:
            url+=[u.item_url]
            names+=[u.item_name]
            img_ids+=[u.itemid]
            
        return jsonify({"status":"OK","error":None,"names":names,"ids":img_ids,"urls":url})
    
    
    
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



@app.route('/api/users/<userid>/wishlist/<itemid>', methods=["DELETE"])
def delete_wish(userid,itemid):
    Wish.query.filter_by(itemid=itemid,userid=userid).delete();
    db.session.commit()
    
    return "OK"
    #pass



@app.route('/thumbnails/view')
def tview():
    return render_template("thumb.html")
    


######
#Functions
######

@login_m.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    
def share(to_name, to_addr):
    
    from_name = session['uname']
    from_addr = session['username']
    subject='My Wishlist'
    #msg = 
    messsage = """From: {} <{}>\nTo: {} <{}>\nSubject: {}\n{}"""
    message_to_send = message.format(from_name, from_addr, to_name,to_addr,subject, msg)
    # Credentials (if needed)
    username = ''
    password = ''
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message_to_send)
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
