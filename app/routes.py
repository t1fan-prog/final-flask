from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.models import Student


@app.route('/')
def schedule():
    try:
        students = Student.query.all()
    except Exception as e:
        print(f'Произошла ошибка при работе с базой: {e}')
        return 500
    return render_template('schedule.html', title='Рассписание', students=students)


@app.route('/api/student', methods=['GET'])
def get_student():
    """Получение списка всех студентов. Если же есть параметр ?chat-id={id} - возвращает сущность Student с конкретным chat-id"""
    chat_id = request.args.get('chat-id', '')
    if chat_id:
        chat_id = int(chat_id)
        chat_ids = [i[0] for i in Student.query.with_entities(Student.chat_id).all()]
        if chat_id in chat_ids:
            student = Student.query.filter_by(chat_id=chat_id).first()
            return jsonify({'http_code': 250, 'result': 'OK', 'name': student.name, 'surname': student.surname, 'room': student.room, 'chat_id': student.chat_id})
        else:
            return jsonify({'http_code': 250, 'result': 'no such user'})
    else:
        try:
            students_list = [{'name': student.name, 'surname': student.surname, 'room': student.room, 'chat_id': student.chat_id} for student in Student.query.all()]
            return jsonify({"students": students_list})
        except Exception as e:
            print(f'Произошла ошибка при работе с базой: {e}')
            return 500


@app.route('/api/create-student', methods=['POST'])
def create_post():
    data = request.get_json()
    student = Student(name=data.get('name'), surname=data.get('surname'), room=data.get('room'), chat_id=data.get('chat_id'))
    uploading_to_base(student)
    try:
        db.session.commit()
    except:
        print("Функция 'create_post. Ошибка при добавлении поста в базу")
        db.session.rollback()
        return jsonify({'status': 'failed'}), 400
    return jsonify({'status': '250 OK'})


def uploading_to_base(student):
    db.session.add(student)
    try:
        db.session.commit()
    except Exception as e:
        print(f"Функция 'uploading_to_base'. Ошибка при добавлении поста в базу:\n{e}")
        db.session.rollback()
        return jsonify({'status': 'failed'}), 400
    return jsonify({'status': '250 OK'})
