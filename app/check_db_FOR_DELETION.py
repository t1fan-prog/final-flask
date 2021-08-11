from models import Student
from app import db

student = Student.query.all()
for s in student:
    print(s.name, s.chat_id)
# msg = f'Привет, {student.name}. Чем могу помочь?'
