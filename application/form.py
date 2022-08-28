from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField,DecimalField, FileField, PasswordField,IntegerField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError
from flask_login import current_user
from application.models import Users


class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip = IntegerField('Zip',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirmpassword = PasswordField('confirm password', validators=[
                                    DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken')


class UpdateUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip = IntegerField('Zip',validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    productname = StringField('Product Name', validators=[DataRequired()])
    productdiscription = TextAreaField(
        'Product Discription', validators=[DataRequired()])
    price = DecimalField('product price', validators=[DataRequired()])
    stock = IntegerField('product stock', validators=[DataRequired()])
    categorie = TextAreaField('categories')
    product_image = FileField('choose image', validators=[
                              FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class ProductUpdateForm(FlaskForm):
    productname = StringField('Product Name', validators=[DataRequired()])
    productdiscription = TextAreaField(
        'Product Discription', validators=[DataRequired()])
    price = DecimalField('product price', validators=[DataRequired()])
    stock = IntegerField('product stock', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class CheckOutForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip = IntegerField('Zip', validators=[DataRequired()])

    submit = SubmitField('Pay now')