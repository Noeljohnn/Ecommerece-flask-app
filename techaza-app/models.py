class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String[80], nullable=False, unique=True)
    password = db.Column(db.String[80], nullable=False)