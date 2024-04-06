from .app import db
from .app import jwt


class User(db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    username = db.Column(db.String(64), nullable = False, unique=True)
    email = db.Column(db.String(254), nullable = False, unique=True)
    password = db.Column(db.String(254), nullable = False)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create User")
        return self

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()

class Friendship(db.Model):
    friendship_id = db.Column(db.Integer, primary_key = True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    user2_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id

    def to_dict(self):
        return {
            "friendship_id": self.friendship_id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id
        }

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create Friendship")
        return self


class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    name = db.Column(db.String(64), nullable = False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.subcategory_id", onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    location = db.Column(db.String(254), nullable = False)
    details = db.Column(db.String(254), nullable = False)

    def __init__(self, user_id, name, subcategory_id, date, start_time, end_time, location, details):
        self.user_id = user_id
        self.name = name
        self.subcategory_id = subcategory_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.details = details

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "user_id": self.user_id,
            "subcategory_id": self.subcategory_id,
            "date": str(self.date),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "location": self.location,
            "details": self.details
        }
    
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            print("event created")
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create Event")
        return self

class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    name = db.Column(db.String(64), nullable = False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.subcategory_id", onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
    date = db.Column(db.Date, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    details = db.Column(db.String(254), nullable = False)

    def __init__(self, user_id, name, subcategory_id, date, duration, start_time, details):
        self.user_id = user_id
        self.name = name
        self.subcategory_id = subcategory_id
        self.date = date
        self.duration = duration
        self.start_time = start_time
        self.details = details

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "name": self.name,
            "subcategory_id": self.subcategory_id,
            "date": str(self.date),
            "duration": self.duration,
            "start_time": str(self.start_time),
            "details": self.details
        }

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create Task")
        return self

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    name = db.Column(db.String(64), nullable = False)

    def __init__(self, user_id, name):
        self.name = name
        self.user_id = user_id

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "user_id": self.user_id,
            "name": self.name
        }
    
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create Category")
        return self


class Subcategory(db.Model):
    __tablename__ = 'subcategory'

    subcategory_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    cateogry_id = db.Column(db.Integer, db.ForeignKey("category.category_id", onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
    color = db.Column(db.String(64))

    def __init__(self, name, category_id, color):
        self.name = name
        self.cateogry_id = category_id
        self.color = color

    def to_dict(self):
        return {
            "subcategory_id": self.subcategory_id,
            "name": self.name,
            "category_id": self.cateogry_id,
            "color": self.color
        }

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create Subcategory")
        return self

