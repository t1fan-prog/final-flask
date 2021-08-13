from datetime import datetime, timedelta

from models import Student, TestProblem
from app import db
from sqlalchemy import func

# test = Student.query.filter(Student.date == datetime.now().date()).all()
# print(test)
# print(datetime.now().date(), type(datetime.now().date()))
#
#
# student = Student.query.all()
# for s in student:
#     print(s.name, s.chat_id, s.date, type(s.date))
#     print(s.date.date() < datetime.now().date() + timedelta(days=1))


oldest_date = Student.query.order_by(Student.date.desc()).all()
for i in oldest_date:
    print(i.name, i.chat_id)

a = Student.query.order_by(Student.date.desc()).first()
print(a)

# for p in problem:
#     print(p.id, p.name, p.date)
# max_date = db.session.query(func.max(Student.date)).scalar()
# user = db.session.query(Student).filter(Student.date == max_date).all()
# print(user.date)
# Удаление из базы

# student = Student.query.delete()
# db.session.commit()