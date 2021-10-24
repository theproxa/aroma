from werkzeug.utils import secure_filename
from shop import app
from flask import render_template,request,redirect,url_for,flash
from shop.models import *
from PIL import Image
from flask_login import login_user, logout_user, current_user,login_required
from shop.forms import *


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html',products=products)

@app.route('/blog')
def blog ():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
    return render_template('blog.html',posts=posts)



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

@app.route('/post/<int:post_id>',methods=['GET','POST'])
def single_blog(post_id):  
    post = Post.query.get(post_id)
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    if request.method == 'POST':
        comment = Comment(name=request.form.get('name'), subject=request.form.get('subject'),email=request.form.get('email'),massege=request.form.get('massage'),post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('comment added', 'succes')
        return redirect(url_for('single_blog',post_id=post.id))
    return render_template('single_blog.html', post=post ,comments = comments )



@app.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():  
    form = PostForm()
    if form.validate_on_submit(): 
        image = request.files.get('image')
        if image:
            file_name = image.filename
            image = Image.open(image)
            image.save('shop/static/img/blog/'+file_name)
            post = Post(title=form.title.data,author=current_user,image=file_name,content=form.content.data)
            db.session.add(post)
            db.session.commit()      
            flash('пост был создан','succes')
            return redirect(url_for('blog'))
    return render_template('new_post.html', form=form)
        

@app.route('/products/<int:product_id>/buy',methods=['GET','POST'])
def buy(product_id):
    if request.method == "POST":
        f= request.form
        b= Buy(name=f.get('name'),email=f.get('email'),adres=f.get('adres'),product_id=product_id)
        db.session.add(b)
        db.session.commit()
    return render_template('buy.html')

@app.route('/buys',methods=['GET','POST'])
def buys():
    buys = Buy.query.all()
    return render_template('buys.html',buys=buys)

@app.route('/buyDELETE<int:buy_id>',methods=['GET','POST'])
def delete_buy(buy_id):
    s = buy_id
    b = Buy.query.filter_by(id=s).first()
    db.session.delete(b)
    db.session.commit()
    return redirect(url_for('buys'))
