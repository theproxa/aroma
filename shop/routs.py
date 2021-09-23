import os
from werkzeug.utils import secure_filename
from shop import app
from flask import render_template,request
from shop.models import Product,db
# from PIL import Image
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
        file_name = request.files.get('image')
        filename=secure_filename(file_name.filename)
        print (filename)
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        p= Product(title=f.get('title'),price=f.get('category'),category=f.get('category'),availibility=f.get('availibility'),description=f.get('description'),image=filename)
        db.session.add(p)
        db.session.commit()
    return render_template('add_product.html')