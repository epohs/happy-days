from datetime import datetime
from app import login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash





@login.user_loader
def load_user(id):
  
  try:
    
    return User.query.get(int(id))
      
  except:
    
    db.create_all()
    
    return None



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    user_level = db.Column(db.Integer, index=False, unique=False, nullable=True, default=0)
    created_on = db.Column(db.DateTime(), index=False, unique=False, nullable=True,  default=datetime.now)
    last_login = db.Column(db.DateTime(), index=False, unique=False, nullable=True,  default=datetime.now)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
            )



class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Float)
    entry_type = db.Column(db.Integer, nullable=False, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('entry.id'), default=0)
    parent = db.relationship("Entry",
                        remote_side=[id],
                        primaryjoin=('entry.c.id==entry.c.parent_id'),
                        backref="children",
                        lazy="joined")
    created_on = db.Column(db.DateTime(), index=False, unique=False, nullable=True,  default=datetime.now)
    modified_on = db.Column(db.DateTime(), index=False, unique=False, nullable=True,  default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Entry {}>'.format(self.val)


