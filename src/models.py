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
    company_name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=True)
    instagram_url = db.Column(db.String(80), unique=True, nullable=False)

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
            raise Exception(error.args)

    def __repr__(self):
        return '<User %r>' % self.username
    
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