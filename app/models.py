from app import db


class Student(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(120), index=True)
    room = db.Column(db.Integer)
    chat_id = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime)
    # problems = db.relationship('TestProblem', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.name} {self.surname} {self.chat_id}>'


class TestProblem(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, index=True)
    # student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student_id = db.Column(db.Integer)

    def __repr__(self):
        return f'Student_id: {self.student_id}, problem: {self.text}'


