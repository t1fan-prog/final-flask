from app import db


class Student(db.Model):
    __tablename__ = 'Students'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(120), index=True)
    room = db.Column(db.Integer)
    chat_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f'<Student {self.name} {self.surname} {self.chat_id}>'
