from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, EditorData
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import bleach

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    data = EditorData.query.order_by(EditorData.id.desc()).first()
    print(data.name)

    flag =0
    if request.method == 'POST':
        new_data = EditorData(html=request.form.get('textpad'), name=request.form.get('name'), extension=request.form.get('ext') )
        duplicateName = EditorData.query.filter_by(name=new_data.name).first()
        if duplicateName is not None:
            flag=1
            return render_template('index.html',  title='Home', data=new_data, flag=flag)
        db.session.add(new_data)
        db.session.commit()
        return render_template('index.html',  title='Home', data=new_data, flag=flag)

   
    return render_template('index.html',  title='Home', data=data, flag=flag)



    
        
        

@app.route('/display')
@app.route('/myedits')
@login_required
def display():
    posts = EditorData.query.order_by(EditorData.id.desc()).all()

    

    return render_template('myedits.html', posts=posts)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)    
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/about")
@login_required
def about():
	
	return render_template('credits.html')
