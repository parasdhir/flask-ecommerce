from application import app,db,bcrpyt
from flask import render_template, url_for, redirect, flash,request,abort
from application.form import ProductForm, RegistrationForm, LoginForm,CheckOutForm,ProductUpdateForm,UpdateUserForm
from application.models import Products,Users,Cart,Order,UserRoles,Role,Categorie,ProductCategories
from application.utils import save_picture,currencyconvert
from flask_login import login_user,logout_user,current_user,login_required


# main page

@app.route('/')
@app.route('/index')
def index():
    page_number = request.args.get('page_number',1,type=int)
    product = Products.query.order_by(Products.id.desc()).paginate(page=page_number,per_page = 6)
    all_categories = Categorie.query.all()
    return render_template('index.html',all_categories=all_categories ,products=product,currencyconvert=currencyconvert)

#registration page

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    all_categories = Categorie.query.all()
    if form.validate_on_submit():
        hashed_password = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name= form.name.data,email=form.email.data,address=form.address.data,city=form.city.data,state=form.state.data,zip=form.zip.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful")
        return redirect(url_for('login'))

    return render_template('RegistrationForm.html',all_categories=all_categories,form=form,page='register')

#login page

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    all_categories = Categorie.query.all()
    if form.validate_on_submit():
        user = Users.query.filter_by(email =form.email.data).first()
        if user and bcrpyt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid Id or Password")

    return render_template('login.html',all_categories=all_categories,form=form,page='login')

#logout user

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# account update page


@app.route('/updateprofile',methods=['GET', 'POST'])
def updateprofile():
    if not current_user.is_authenticated:
        flash('Login to update')
        return redirect(url_for('index'))

    all_categories = Categorie.query.all()
    form = UpdateUserForm()
    if form.validate_on_submit():
        
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip =form.zip.data

        db.session.commit()
        flash('Update sucessful')
    elif request.method =='GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip.data = current_user.zip
    return render_template('updateaccount.html',page='update profile',all_categories=all_categories,form = form)







#product page for uploading products only for admin user

@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    #admin login
    if not current_user.has_role('Admin'):
        return abort(401)
    
    form = ProductForm()
    if form.validate_on_submit():
    
        image = save_picture(form.product_image.data)
        product = Products(productname=form.productname.data,productdiscription=form.productdiscription.data, price=form.price.data,product_stock=form.stock.data, product_image=image)
        db.session.add(product)
        if form.categorie.data:
            formcategorie = form.categorie.data.split(',')
            for categ in formcategorie:
                categorie_exist = Categorie.query.filter_by(name=categ).first()
                if categorie_exist:
                    productcategorie = ProductCategories(Product_id=product.id,categorie_id=categorie_exist.id)
                    db.session.add(productcategorie)
                else:
                    product.categories.append(Categorie(name=categ))
            
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('productform.html',form=form,page='product')

# all the product list and link to update the products

@app.route('/product/list', methods=['GET', 'POST'])
@login_required
def product_list():
    #admin login
    if not current_user.has_role('Admin'):
        return abort(401)
    products = Products.query.all()
    return render_template('productlist.html',products=products,page='productlist')

@app.route('/product/list/<int:productid>', methods=['GET', 'POST'])
@login_required
def product_update(productid):
    #admin login
    if not current_user.has_role('Admin'):
        return abort(401)

    product = Products.query.filter_by(id=productid).first()
    form = ProductUpdateForm()
    if form.validate_on_submit():
        product.productname = form.productname.data
        product.productdiscription = form.productdiscription.data
        product.price = form.price.data
        product.product_stock = form.stock.data
        db.session.commit()
        flash('Updated')
    else:
        form.productname.data = product.productname
        form.productdiscription.data = product.productdiscription
        form.price.data = product.price
        form.stock.data = product.product_stock

    return render_template('productupdate.html',page=product.productname,form=form)

    

#add product to cart link

@app.route('/addtocart')
def addtocart():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        product_Id = int(request.args.get('product_id'))
        productexist = current_user.cart
        for product in productexist:
            if product_Id == product.product_id:
                flash("Product already in cart")
                return redirect(url_for('index'))

        cart = Cart(user_id = current_user.id,product_id=product_Id)
        db.session.add(cart)
        db.session.commit()

        return redirect(url_for('index'))


# cart page

@app.route('/cart')

def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    all_categories = Categorie.query.all()
    
    # get product photo, product name  and product quantity 
    carts = Cart.query.filter_by(user_id = current_user.id).join(Products,Cart.product_id== Products.id).add_columns(Products.product_image,Products.productname,Cart.quantity,Cart.product_id,Products.price).all()
    # calculate the total order
    total = 0
    for item in carts:
        total+= (item.quantity * item.price)
   
    return render_template("cart.html",all_categories=all_categories,page='cart',carts = carts,currencyconvert=currencyconvert,total = total)

# delete product link

@app.route('/deletefromcart')
def deletefromcart():
    itemtodelete = request.args.get('product_id')
    cart = Cart.query.filter_by(user_id = current_user.id,product_id=itemtodelete).first()
    if not cart:
        flash("Something went wrong")
        return redirect(url_for('cart'))
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/incrementquantity')
def incrementquantity():
    quantityhandler = request.args.get('product_id')
    cart = Cart.query.filter_by(user_id = current_user.id,product_id=quantityhandler).first()
    
    if not cart:
        flash("Something went wrong")
        return redirect(url_for('cart'))

    # add product upto maximum stock limit
    product = Products.query.filter_by(id=quantityhandler).first()
    if product.product_stock == cart.quantity:
        flash("Cannot add more than " + str(cart.quantity) + ' in cart')
        return redirect(url_for('cart'))

    cart.quantity = cart.quantity + 1
    db.session.commit()
    
    return redirect(url_for('cart'))

@app.route('/decrementquantity')
def decrementquantity():
    quantityhandler = request.args.get('product_id')
    cart = Cart.query.filter_by(user_id = current_user.id,product_id=quantityhandler).first()

    if not cart:
        flash("Something went wrong")
        return redirect(url_for('cart'))
    # cannot decrement less than 1 for product    
    if cart.quantity == 1:
        flash("Cannot decrement to 0 ")
        return redirect(url_for('cart'))
    cart.quantity = cart.quantity - 1
    db.session.commit()
    
    return redirect(url_for('cart'))

# checkout page

@app.route('/checkout',methods=['GET', 'POST'])
@login_required
def checkout():
    if not current_user.is_authenticated:
        flash('Login to checkout')
        return redirect(url_for('index'))

    cart = Cart.query.filter_by(user_id = current_user.id).all()
    if not cart:
        flash('no item in the cart')
        return redirect(url_for('cart'))
    all_categories = Categorie.query.all()
    form = CheckOutForm()
    if form.validate_on_submit():
        
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip =form.zip.data

        db.session.commit()
        flash('Checkout sucessful')
        return redirect(url_for('successful'))
    elif request.method =='GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip.data = current_user.zip
    return render_template('checkout.html',page='checkout',all_categories=all_categories,form = form)

# order placed successful page

@app.route('/successful')
@login_required
def successful():
    cart = Cart.query.filter_by(user_id = current_user.id).all()
    if not cart:
        flash('no item in the cart')
        return redirect(url_for('cart'))

    lastvalue = Order.query.order_by(Order.order_number.desc()).first()
    if not lastvalue:
        lastvalue = 1
    else:
        lastvalue = lastvalue.order_number + 1
    for item in cart:
        order = Order(user_id=item.user_id,product_id=item.product_id,quantity=item.quantity,order_number=lastvalue)
        product = Products.query.filter_by(id=item.product_id).first()
        product.product_stock = product.product_stock - item.quantity
        db.session.add(order)
        db.session.delete(item)
    

    db.session.commit()
    

    return render_template('successful.html')

# orders page

@app.route('/orders')
def orders():

    if not current_user.is_authenticated:
        flash('Login First')
        return redirect(url_for('login'))

    all_categories = Categorie.query.all()
    orders = Order.query.filter_by(user_id = current_user.id).group_by(Order.order_number).all()


    return render_template('order.html',all_categories=all_categories,page='orders',orders=orders)

# each order detail page

@app.route('/orders/<int:order_number>')
@login_required
def order_details(order_number):

    if not current_user.is_authenticated:
        flash('Login first')
        return redirect(url_for('index'))
    all_categories = Categorie.query.all()
    orders = Order.query.filter_by(user_id = current_user.id,order_number=order_number).join(Products,Order.product_id== Products.id).add_columns(Products.productname,Order.quantity,Products.price).all()
    if not orders:
        flash('no order of this number available')
        return redirect(url_for('orders'))

    total = 0
    for item in orders:
        total+= (item.quantity * item.price)

    return render_template('orderdetail.html',all_categories = all_categories,page='orderdetails',orders = orders,total=total,ordernumber=order_number,currencyconvert=currencyconvert)

# categorie page
@app.route('/Categories')
def allcategories():
    page_number = request.args.get('page_number',1,type=int)
    all_categories = Categorie.query.all()
    product = Products.query.order_by(Products.id.desc()).paginate(page=page_number,per_page = 9)
    return render_template('categories.html',all_categories =all_categories,products=product,currencyconvert=currencyconvert)

# categorie filter by name

@app.route('/Categories/<string:name>')
def categories(name):
    page_number = request.args.get('page_number',1,type=int)
    all_categories = Categorie.query.all()
    categ = Categorie.query.filter_by(name = name).first()
    product = categ.product.order_by(Products.id.desc()).paginate(page=page_number,per_page = 9)
    return render_template('categories.html',all_categories = all_categories,products=product,currencyconvert=currencyconvert)
