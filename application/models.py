from application import db,login_manager
from flask_login import UserMixin




@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


class Users(db.Model,UserMixin):
    id = id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String(60),nullable = False)
    address = db.Column(db.String,nullable=False)
    city = db.Column(db.String,nullable=False)
    state = db.Column(db.String,nullable=False)
    zip = db.Column(db.Integer,nullable=False)
    
    order = db.relationship('Order',backref='cartorder',lazy=True)
    cart = db.relationship('Cart', backref='cartuser', lazy=True)
    roles = db.relationship('Role', secondary='user_roles',backref=db.backref('user', lazy='dynamic'))

    def has_role(self, role): 
        query = Role.query.filter_by(name = role).first()
        if query:
            if query in self.roles:
                return True
        return False

    def __repr__(self):
        return '<Users %r %r >' % (self.name, self.email)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String, nullable=False)
    productdiscription = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.String(20), nullable=False)
    product_stock = db.Column(db.Integer(),nullable=False)
    item = db.relationship('Cart', backref='itemcart', lazy=True)
    categories = db.relationship('Categorie', secondary='product_categories',backref=db.backref('product', lazy='dynamic'))

    def __repr__(self):
        return '<Products %r %r >' % (self.productname, self.productdiscription)


class ProductCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id', ondelete='CASCADE'))

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Cart(db.Model):
    
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False,primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False,primary_key=True)
    quantity = db.Column(db.Integer,default=1,nullable=False)

    def __repr__(self):
        return '<Cart %r %r >' % (self.user_id, self.product_id)


class Order(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
    quantity = db.Column(db.Integer,default=1,nullable=False)
    order_number = db.Column(db.Integer,nullable = False)




