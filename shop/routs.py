from werkzeug.utils import secure_filename
from shop import app
from flask import render_template,request,redirect,url_for,flash
from shop.models import Product,db,User
from PIL import Image
from flask_login import login_user, logout_user, current_user
from shop.forms import RegistretionForm


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html',products=products)

@app.route('/blog')
def blog ():
    return render_template('blog.html')

@app.route('/add product' ,methods=['GET','POST'])
def add_product ():
    if request.method == "POST":
        f= request.form
        image = request.files.get('image')
        file_name=image.filename
        image = Image.open(image)
        image.save('shop/static/img/product/' + file_name)
        p= Product(title=f.get('title'),price=f.get('price'),category=f.get('category'),availibility=f.get('availibility'),description=f.get('description'),image=file_name)
        db.session.add(p)
        db.session.commit()
    return render_template('add_product.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first() 
        if user and user.password == request.form.get('password'):
            login_user( user ) 
        return redirect(url_for('index'))      
    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():  
    logout_user()
    return redirect(url_for('index'))


@app.route('/products/<int:product_id>')
def product_deteil(product_id):  
    product =Product.query.get(product_id)
    return render_template('product_deteil.html', product=product)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistretionForm()
    if form.validate_on_submit():
        
        user = User(email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registration successful', 'succes')
        login_user( user )
        return redirect(url_for('index'))   
    return render_template('register.html' , form=form)



@app.route('/errorRegister')
def errorRegister():  
    return render_template('errorRegister.html')


