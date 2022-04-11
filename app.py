import codecs
from itertools import count
import json
from os import abort
from random import randint
from flask import Flask, redirect , render_template,request,jsonify,flash, session, url_for,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import BigInteger, true, table,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import requests
from urllib3 import Retry

app = Flask(__name__)
app.secret_key='asdaqwqd23423r' 
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///users.db"
app.config['SQLALCHEMY_BINDS']={'notesdb': 'sqlite:///notes.db','usersdb':'sqlite:///users.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class usersdb(db.Model):
    __bind_key__='usersdb'
    user_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    role_id=db.Column(db.Integer(),nullable=False)
    email=db.Column(db.String(30))
    password=db.Column(db.String(100),nullable=False)
    country=db.Column(db.String(10),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    mobno=db.Column(db.BigInteger(),nullable=False)
    notes=db.relationship("notesdb",backref="notes")


    def __repr__(self) -> str:
        return f"{self.email}- {self.user_id} - {self.date_created}"

class notesdb(db.Model):
    __bind_key__='notesdb'
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    note_id=db.Column(db.BigInteger(),db.ForeignKey('usersdb.user_id'))
    notestext=db.Column(db.String(100),nullable=False)
    notesname=db.Column(db.String(10),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
     


    def __repr__(self) -> str:
        return f"{self.notes_id}- {self.notesname} - {self.notestext}"



@app.before_request
def before_requests():
    g.user=None
    if 'user_id' in session:
        print(session['user_id'])
        g.user=session['user_id']

@app.route("/")
def hello_worlds():
    #admin_data=usersdb(user_id=usersdb().user_id,role_id=1,email='admin@gmail.com',password='QWDE@32E!!',mobno=9999999990,country='India')
    #db.session.add(admin_data)
    #db.session.commit()
    #print('data added')
    return render_template('index.html')

@app.route("/login" , methods=['GET'])
def logins():
    if request.method=='GET':
        return render_template('login.html') 

@app.route("/signup" , methods=['GET'])
def signupAccount():
    if request.method=='GET':
        return render_template('signup.html')


@app.route("/mynotes",methods=['GET'])
def mynotes():
    if request.method=='GET' and g.user !=None:
        user_id=g.user
        notes=notesdb.query.filter_by(note_id=user_id)
        return render_template('mynotes.html',notes=notes)
    else:
        return redirect(url_for('logins'))

@app.route("/api/createUsers",methods=['POST','GET'])
def create_Account():
    if request.method=='POST':
        datas=request.get_json(force=True)
        db_datas=usersdb.query.all()            
        email,mob,password,country=datas['email'].strip(),datas['mobile'].strip(),datas['password'].strip(),datas['country'].strip()
        print(mob)
        print(type(mob))
        for data in db_datas:
            if data.email==email:
                flag=0
            else:
                flag=1

        if flag==1 and email != '' and password != '' and mob != '' and country != '':
            print(mob)
            db_data=usersdb(user_id=usersdb().user_id,email=email,mobno=mob,password=password,country=country,role_id=2)
            db.session.add(db_data)
            db.session.commit()
            datas={'email':email,'mobile':mob,'country':country,'role_id':2,'success':True}
            return jsonify(datas)
        else:
            error={'error':True}
            return jsonify(error)
            #return redirect(url_for('signupAccount')) 
    else:   
        return redirect(url_for('signupAccount'))


@app.route("/api/reset-password",methods=['POST'])
def resetpasswordwithtoken():
 if request.method=='POST':
    datas=request.get_json(force=True)
    pwd=datas['password']
    token=datas['token']
    email=codecs.decode(token,'rot-13')
    users=usersdb.query.filter_by(email=email).first()
    users.password=pwd
    db.session.commit()
    return jsonify({'email':email})
 else:
     return jsonify({'error':'Some Error Occured'})   


@app.route("/forgotpassword/<token>")
def resetpassword(token):
    token=token
    email=codecs.decode(token,'rot-13')
    flag=usersdb.query.filter_by(email=email).first()
    if flag !=None:
       return render_template('resetpassword.html',token=token)
    else:
        return redirect('forgotpassword')


@app.route("/forgotpassword")
def forgotpasswordpage():
    return render_template('forgotpassword.html')

@app.route("/api/forgot-password",methods=['POST'])
def forgotpassword():
    if request.method=='POST':
        datas=request.get_json(force=True)
        email=datas['email']
        users_data=usersdb.query.filter_by(email=email).first()
        if users_data !=None:
            #print(users_data)
            #passwd=users_data.password
            token=codecs.encode(email,"rot-13")
            url="http://127.0.0.1:5000/forgotpassword/"+token
            data_json={'email':email,'token':token,'reset-url':url}
            return jsonify(data_json)
        else:
            return jsonify({'error':'User Not Found'})
@app.route("/api/loginUsers",methods=['POST'])
def loginusers():
    session.pop('user_id',None)
    if request.method=='POST':
        datas=request.get_json(force=True)
        email,password=datas['email'].strip(),datas['password'].strip()
        existing_user = usersdb.query.filter_by(email=email).first()
        if existing_user== None or password != existing_user.password:
            #flash('No User Found with This Email')
            #print('No user found')
            return {'error':True}
        else: 
            #session['user_id']='asda21e12e21e'
            session['user_id']=existing_user.user_id
            #print(session['user_id'])
            #print("g user is value: ",g.user)
            #return redirect(url_for('dashboard'),code=302)
            #return(render_template('dashboard.html',code=302))
            data_json=jsonify({'user_id':existing_user.user_id,'password':existing_user.password})
            return data_json

    else:
        return {'error':True}

@app.route('/api/users/<user_id>/notes',methods=['GET','PUT'])
def readnotes(user_id):
    if request.method=='GET':
       users=notesdb.query.filter_by(note_id=user_id)
       data_json=[{'notesname':user.notesname,'notestext':user.notestext} for user in users]
       return jsonify(data_json)

    else:
        datas=request.get_json(force=True)
        name,text=datas['notesname'],datas['notestext']
        data=notesdb(id=notesdb().id,notestext=text,notesname=name,note_id=user_id)
        #db.session.add(data)
        data.notestext=text
        data.notesname=name
        db.session.commit()
        return jsonify({'notesname':name,'notestext':text})


@app.route('/api/createnotes',methods=['POST'])
def create_notes():
   if request.method=='POST' and g.user!=None:
       data=request.get_json(force=True)
       text,name=request.json['notes_text'],request.json['notes_name']
       if text != '' and name !='': 
           notes_db=notesdb( id=notesdb().id,note_id=g.user,notesname=name,notestext=text)
           db.session.add(notes_db)
           db.session.commit()
           data_json=jsonify({'notestext':text,'notesname':name})
           return data_json
       else:
           return {'error':True}



@app.route('/dashboard')
def dashboard():
        if not g.user:
            return redirect('login')
        else:
            return render_template('dashboard.html')

@app.route('/createnotes')
def makenotes():
    if not g.user:
        return redirect('logins')
    else:
         return render_template('createnotes.html')


@app.route('/signout')
def signout():
    if not g.user:
        return redirect('logins')
    else:
        session.pop('user_id',None)
        return render_template('login.html')

@app.route('/api/roles',methods=['GET','PUT'])
def users():
  if request.method=='GET':
    users=usersdb.query.all()
    data_json=[{'email':user.email,'role_id':user.role_id} for user in users]
    return jsonify(data_json)
  else:
      if request.method=='PUT':
         datas=request.get_json(force=True)
         email,role_id=datas['email'],datas['role_id']
         users=usersdb.query.filter_by(email=email).first()
         if users!=None and (role_id!='' or role_id!=None):
             users.role_id=role_id
             db.session.commit()
             return {'Success':True}
         else:
             return {'error':True}
      else:
             return {'error':True}


if __name__ == "__main__":
    app.run(debug=True)
