from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
  Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  Name = db.Column(db.Text, nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def remove(self):
    db.session.delete(self)
    db.session.commit()

class BaseModel2:
  Id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def remove(self):
    db.session.delete(self)
    db.session.commit()