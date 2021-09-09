@app.route("/")
def index():
    return render_template('index.html')

# store
@app.route("/store")
def store():
    items = User.query.all()
    return render_template('store.html', items=items)

# pro page
@app.route("/pro_page")
def pro_page():
    return render_template('pro_page.html')

@app.route("/single_product")
def single_product():
    return render_template('single_product.html')    

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
