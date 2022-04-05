from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    phone_number = db.Column(db.String(80), unique=False, nullable=False)
    cloudinary_url=db.Column(db.String(120), unique=False, nullable=True)

class TravelerUser(Base):
    name = db.Column(db.String(120), unique=False, nullable=True)
    lastname = db.Column(db.String(80), unique=False, nullable=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
   
    @classmethod
    def create(cls, **data):
        #crear instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print('FALLA EL CONSTRUCTOR')
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD: ',error.args)
            db.session.rollback()
            return None
            raise Exception(error.args, 500)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "lastname": self.lastname,
            "nickname": self.nickname
            # do not serialize the password, its a security breach
        }

    def __init__(self,**kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class CompanyUser(Base):
    company_name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=True)
    instagram_url = db.Column(db.String(80), unique=False, nullable=True)


    @classmethod
    def create(cls, **data):
        #crear instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print('FALLA EL CONSTRUCTOR')
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD: ',error.args)
            db.session.rollback()
            return None
            raise Exception(error.args, 500)
    def serialize(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "instagram_url": self.instagram_url
            # do not serialize the password, its a security breach
        }

    def __init__(self,**kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class CompanyPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cloudinary_url = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(120), unique=False, nullable=False)
    state = db.Column(db.String(120), unique=False, nullable=False)
    country = db.Column(db.String(120), unique=False, nullable=False)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username
    
