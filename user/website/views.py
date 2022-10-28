from operator import truediv
from . import db,mail
from .models import bookingdb
from .models import User
from .models import galleryImageUpload
from flask import Blueprint, render_template, request,redirect, flash,url_for
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user,login_required, logout_user, current_user
import base64
from flask_mail import Mail,Message
from sre_constants import SUCCESS


views = Blueprint('views', __name__)
 
#login


class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Register")

    def validate_username(self, username):
        existing_user_username=User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists.please choose different one.")

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Login")

@views.route("/")
def index():
    return render_template("home.html",user=current_user)


@views.route("/home")
def home():
    return render_template("home.html",user=current_user)

@views.route("/services")
def services():
    return render_template("services.html",user=current_user)



@views.route("/gallery")
def gallery():
    all_data=galleryImageUpload.query.all()
    return render_template("gallery.html",user=current_user,data=all_data)


@views.route("/login",methods=['get','post'])
def login():
    form= LoginForm()
    return render_template("login.html",form=form,user=current_user)

@views.route("/register",methods=['get','post'])
def register():
    form=RegisterForm()
    return render_template("register.html",form=form,user=current_user)

@views.route("/registerForm",methods=['get','post'])
def registerForm():
    if request.method=='POST':
        form=RegisterForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            print(user)
            if user:
                flash("Username alreay exists!! Try another name")
                return redirect(url_for('views.register',user=current_user))
            else:
                new_user=User(username=form.username.data, password=form.password.data, usertype="user")
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(username=form.username.data).first()
                login_user(user,remember=True)
                return redirect(url_for('views.home',user=current_user))
        return render_template("register.html",form=form,user=current_user)


@views.route("/loginForm",methods=['get','post'])
def loginForm():
    if request.method=='POST':
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if(user.password == form.password.data):
                    login_user(user,remember=True)
                    if(user.usertype == "user"):
                        return redirect(url_for('views.home',user=current_user))
                    else:
                        return redirect(url_for('views.galleryAdmin',user=current_user))
                else:
                    flash("invalid password")
                    return redirect(url_for('views.login',user=current_user))
            else:
                flash("username not found!!")
                return redirect(url_for('views.login',user=current_user))
        return render_template("register.html",form=form,user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login',user=current_user))

@views.route("/package")
def package():
    return render_template("package.html",user=current_user)

@views.route("/booking")
def booking():
    if current_user.is_authenticated:
        all_data=bookingdb.query.filter_by(username=current_user.username)
        print(current_user.username)
        return render_template("booking.html",user=current_user,data=all_data)
    else:
        return render_template("booking.html",user=current_user)


    

@views.route("/bookingForm",methods=['GET','POST'])
def bookingForm():
    if request.method == 'POST':
        if current_user.is_authenticated:
            name=request.form['name']
            email=request.form['email']
            address=request.form['address']
            package=request.form['package']
            date=request.form['date']
            phne=request.form['phne']
            username=current_user.username
            status="Pending"
            from datetime import datetime
            import datetime
            Db_date=bookingdb.query.filter_by(date=date,status="Accepted").first()
            t_date= datetime.date.today()
            cur=datetime.datetime.strptime(date,'%Y-%m-%d')
            c_date=cur.date()
            print(c_date)
            if(Db_date):
                flash("Date is already booked!!")
            elif(c_date<t_date):
                flash("Enter correct date")
            else:
                if(len(phne)!=10):
                    flash("Enter 10 digit of phone number!")
                    return redirect(url_for('views.booking',user=current_user))
                else:
                    if(phne.isdigit()==False):
                        flash("Only numbers are allowed!")
                        return redirect(url_for('views.booking',user=current_user))

                my_data=bookingdb(name,email,address,phne,package,date,username,status)
                db.session.add(my_data)
                db.session.commit()
                flash("Data send to admin...Wait for your response")
                email="keerthij.20cse@kongu.edu"
                subject="order received"
                msg="Hurray! , "+ my_data.name +" has order for date:"+my_data.date+" please respond to the customer!"
                message=Message(subject,sender="harinisham.20cse@kongu.edu",recipients=[email])
                message.body=msg
                mail.send(message)
                success ="message send"
                return redirect(url_for('views.booking',user=current_user,success=success))
        else:
            flash("please login to continuee.....!")
            return redirect(url_for('views.booking',user=current_user))

    return redirect(url_for('views.booking',user=current_user))


# admin

@views.route("/bookingAdmin")
def bookingAdmin():
    all_data=bookingdb.query.all()
    return render_template("bookingAdmin.html",data=all_data,user=current_user)


@views.route("/packageAdmin")
def packageAdmin():
    return render_template("packageAdmin.html",user=current_user)


@views.route("/galleryAdmin")
def galleryAdmin():
    all_data=galleryImageUpload.query.all()
    return render_template("galleryAdmin.html",data=all_data,user=current_user)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg' ,'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/galleryImage",methods=['post'])
@login_required
def galleryImage():
    if request.method == 'POST':
        file = request.files['inputFile']

        if file.filename == '':
            flash("no image is selected")
            return redirect(url_for('views.galleryAdmin',user=current_user))
        
        if file and allowed_file(file.filename):
            name = file.filename
            data = file.read()
            final_pic=base64.b64encode(data).decode('ascii')
            upload = galleryImageUpload(name , final_pic)
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('views.galleryAdmin',user=current_user))
        else:
            flash("Only images are allowed")
            return redirect(url_for('views.galleryAdmin',user=current_user))
 
#accepting and rejecting orders

@views.route("/acceptConcept/<id>")
def acceptConcept(id):
    my_data=bookingdb.query.get(id)
    my_data.status="Accepted"
    db.session.commit()
    flash("Order has been accepted successfully!!")
    email=my_data.email
    subject="confiramtion mail"
    msg= my_data.name +" , Your booking for MakeupArt is confirmed :)"
    message=Message(subject,sender="harinisham.20cse@kongu.edu",recipients=[email])
    message.body=msg
    mail.send(message)
    success ="message send"
    return redirect(url_for('views.bookingAdmin',user=current_user,success=success))

@views.route("/rejectConcept/<id>")
def rejectConcept(id):
    my_data=bookingdb.query.get(id)
    my_data.status="Rejected"
    db.session.commit()
    flash("Order has been rejected successfully!!")
    email=my_data.email
    subject="Rejection mail"
    msg="Sorry, "+ my_data.name +"Your booking for MakeupArt is rejected :("
    message=Message(subject,sender="harinisham.20cse@kongu.edu",recipients=[email])
    message.body=msg
    mail.send(message)
    success ="message send"
    return redirect(url_for('views.bookingAdmin',user=current_user,success=success))

@views.route("/cancelConcept/<id>")
def cancelConcept(id):
    my_data=bookingdb.query.get(id)
    my_data.status="Canceled"
    db.session.commit()
    flash("Your order has been cancelled!!")
    email="keerthij.20cse@kongu.edu"
    subject="cancellation mail"
    msg="Sorry, "+ my_data.name +" has cancelled the booking for MakeupArt :("
    message=Message(subject,sender="harinisham.20cse@kongu.edu",recipients=[email])
    message.body=msg
    mail.send(message)
    success ="message send"
    return redirect(url_for('views.booking',user=current_user,success=success))


