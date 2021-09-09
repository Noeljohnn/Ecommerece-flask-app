from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'a081f5372e9ce5b9cc58972f7b835614'

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String[100], nullable=False)
    price = db.Column(db.Integer[100], nullable=False)
    image_file = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'Store {self.name}'

class SingleProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.String[100], nullable=False)
    product_name = db.Column(db.String[100], nullable=False)
    product_price = db.Column(db.Integer[100], nullable=False)
    product_details = db.Column(db.String[1000], nullable=False)
    product_description_title = db.Column(db.String[1000], nullable=False)
    product_descriptin_easysetup = db.Column(db.String[1000], nullable=False)
    product_descriptin_features = db.Column(db.String[1000], nullable=False)
    product_descriptin_adjustable = db.Column(db.String[1000], nullable=False)
    image_file = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'Store {self.product_name}'
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String[80], nullable=False, unique=True)
    password = db.Column(db.String[80], nullable=False)

    def __repr__(self):
        return f'User {self.email}'

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

# flask form signup
class Signup(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})

    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})

    submit = SubmitField("Signup")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()

        if existing_user_email:
            raise ValidationError("The user already exists")

# flask form login
class Login(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Email"})

    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

# Home page route
@app.route("/")
def index():
    return render_template('index.html')

# store
@app.route("/store")
def store():
    items = Store.query.all()
    return render_template('store.html', items=items)

# pro page
@app.route("/pro_page")
def pro_page():
    return render_template('pro_page.html')

@app.route("/single_product")
def single_product():
    products = SingleProduct.query.all()
    return render_template('single_product.html', products=products)    

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('user_info'))
    return render_template('login.html', form=form)

# user route
@app.route("/user_info", methods=['GET', 'POST'])
@login_required
def user_info():
    return render_template('user_info.html')

# Signup route
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = Signup()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

if __name__=='__main__':
    app.run(debug=True)