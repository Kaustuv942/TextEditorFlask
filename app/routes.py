from flask import render_template, flash, redirect, url_for, request, Response
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, EditorData, CodeData
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from io import BytesIO

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    data = EditorData.query.order_by(EditorData.id.desc()).filter_by(author=current_user).first()
    flag=-1
    if data is not None:
        flag=0
        
    if request.method == 'POST':
        if flag ==0:
            z=request.form.get('name')
            if data.name == z:
                print('data saved under previous name')
                
                data.html = request.form.get('textpad')
                db.session.commit()
                new_data=EditorData.query.order_by(EditorData.id.desc()).filter_by(author=current_user).first()
                return render_template('index.html',  title='Home', data=new_data, flag=flag)
            else:
                print('Data saved under new name')
                new_data = EditorData(html=request.form.get('textpad'), name=request.form.get('name'), author=current_user )
                db.session.add(new_data)
                db.session.commit()                
                return render_template('index.html',  title='Home', data=new_data, flag=flag)

        else:
            print('Data saved as new file')
            new_data = EditorData(html=request.form.get('textpad'), name=request.form.get('name'), author=current_user )
            db.session.add(new_data)
            db.session.commit()         
            flag=0       
            return render_template('index.html',  title='Home', data=new_data, flag=flag)

    if data is None:
        flag=-1
        return render_template('index.html', title='Text Editor', flag=flag)
    
    
    return render_template('index.html', title='Text Editor', data=data, flag=flag)


@app.route('/codingtab', methods=['GET','POST'])
@login_required
def codeit():
    
    code = CodeData.query.order_by(CodeData.id.desc()).filter_by(author=current_user).first()
    flag=-1
    if code is not None:
        flag=0
        
    if request.method == 'POST':
        if flag ==0:
            z=request.form.get('name')
            if code.name == z:
                print('code saved under previous name')
                
                code.code = request.form.get('textpad')
                db.session.commit()
                new_data=CodeData.query.order_by(CodeData.id.desc()).filter_by(author=current_user).first()
                return render_template('codingtab.html',  title='Home', code=new_data, flag=flag)
            else:
                print('code saved under new name')
                new_data = CodeData(code=request.form.get('textpad'), name=request.form.get('name'), author=current_user )
                db.session.add(new_data)
                db.session.commit()                
                return render_template('codingtab.html',  title='Home', code=new_data, flag=flag)

        else:
            print('code saved as new file')
            new_data = CodeData(code=request.form.get('textpad'), name=request.form.get('name'), author=current_user )
            db.session.add(new_data)
            db.session.commit()         
            flag=0       
            return render_template('codingtab.html',  title='Home', code=new_data, flag=flag)

    if code is None:
        flag=-1
        return render_template('codingtab.html', title='Type a Code', flag=flag)
    
    
    return render_template('codingtab.html', title='Type a Code', code=code, flag=flag)


@app.route('/uploads', methods=['GET','POST'])
@login_required
def uploads():

    return render_template('uploads.html', title='Upload a file')

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['inputFile']
    
    newfile = EditorData(name=file.filename, html=file.read(), extension="", author=current_user )
    db.session.add(newfile)
    db.session.commit()

    return 'Saved '+ file.filename +' to the database'




@app.route('/download/<int:id>')
def download(id):
    post = EditorData.query.filter_by(id=id).first()
    generator = post.html
   
    return Response(generator,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;"}) 


@app.route('/downloadcode/<int:id>')

def downloadcode(id):
    code = CodeData.query.filter_by(id=id).first()   
    generator = code.code

    return Response(generator,mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;"})  



@app.route('/display')
@app.route('/myedits')
@login_required
def display():
    posts = EditorData.query.order_by(EditorData.id.desc()).filter_by(author=current_user).all()

    
        

    return render_template('myedits.html', posts=posts, title='My Edits')


@app.route('/mycodes')
@login_required
def displaycodes():
    codes = CodeData.query.order_by(CodeData.id.desc()).filter_by(author=current_user).all()


    return render_template('mycodes.html', codes=codes, title='My Codes')

@app.route('/edit/<int:id>', methods=['GET', 'POST'] )
@login_required
def edit(id):
    post = EditorData.query.filter_by(id=id).first()

    if request.method == 'POST':
        posts = EditorData.query.order_by(EditorData.id.desc()).filter_by(author=current_user).all()
        post.name = request.form.get('name')
        post.extension = request.form.get('ext')
        post.html = request.form.get('textpad')
        db.session.commit()

        print('data saved')


        return render_template('myedits.html', posts=posts)

    return render_template('edit.html', data=post, title='Edit My Posts')

@app.route('/editcodes/<int:id>', methods=['GET', 'POST'])
@login_required
def editcode(id):
    code = CodeData.query.filter_by(id=id).first()
    if request.method == 'POST':
        codes = CodeData.query.order_by(CodeData.id.desc()).filter_by(author=current_user).all()
        code.name = request.form.get('name')
        code.code = request.form.get('textpad')
        db.session.commit()

        print('code saved')


        return render_template('mycodes.html', codes=codes,title='My Codes')
    return render_template('editcodes.html', code=code, title='Edit My Code')



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = EditorData.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()


    
    posts = EditorData.query.order_by(EditorData.id.desc()).filter_by(author=current_user).all()

    return render_template('myedits.html', posts=posts)

@app.route('/deletecodes/<int:id>', methods=['GET','POST'])
@login_required
def deletecode(id):

    code= CodeData.query.filter_by(id=id).first()

    db.session.delete(code)
    db.session.commit()
    
    codes = CodeData.query.order_by(CodeData.id.desc()).filter_by(author=current_user).all()

    return render_template('mycodes.html', codes=codes, title='My Codes')


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
