from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    phone_number = db.Column(db.String(80), unique=False, nullable=False)
    cloudinary_url=db.Column(db.String(120), unique=True, nullable=True)

class TravelerUser(Base):
    name = db.Column(db.String(120), unique=False, nullable=True)
    lastname = db.Column(db.String(80), unique=False, nullable=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)

class CompanyUser(Base):
    company_name = db.Column(db.String(120), unique=False, nullable=False)
    adress = db.Column(db.String(80), unique=False, nullable=True)
    Instagram_url = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }