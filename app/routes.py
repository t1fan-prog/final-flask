import traceback
from datetime import datetime, timedelta
from flask import render_template, request, jsonify
from app import app, db
from app.models import Student, Problems
from app.logger import create_logger

logger = create_logger(__name__)


@app.route('/')
def schedule():
    try:
        students = Student.query.order_by(Student.date).all()
        current_date = datetime.now().date()
    except Exception:
        logger.exception(f'Exeption occured {traceback.extract_stack()[-1][2]}', exc_info=True)
        return 500
    return render_template('schedule.html', title='Рассписание', students=students, current_date=current_date)


@app.route('/api/student', methods=['GET'])
def get_student():
    """Получение списка всех студентов. Если же есть параметр ?chat-id={id} - возвращает сущность Student с
    конкретным chat-id """
    chat_id = request.args.get('chat-id', '')
    if chat_id:
        chat_id = int(chat_id)
        chat_ids = [i[0] for i in Student.query.with_entities(Student.chat_id).all()]
        if chat_id in chat_ids:
            student = Student.query.filter_by(chat_id=chat_id).first()
            return jsonify({'http_code': 250, 'result': 'OK', 'name': student.name, 'surname': student.surname,
                            'room': student.room, 'chat_id': student.chat_id, 'date': student.date.date()})
        else:
            return jsonify({'http_code': 250, 'result': 'no such user'})
    else:
        try:
            students_list = [{'id': student.id, 'name': student.name, 'surname': student.surname, 'room': student.room,
                              'chat_id': student.chat_id, 'date': student.date} for student in Student.query.all()]
            return jsonify({"students": students_list})
        except Exception:
            logger.exception(f'Exeption occured {traceback.extract_stack()[-1][2]}', exc_info=True)
            return 500


@app.route('/api/create-student', methods=['POST'])
def create_post():
    data = request.get_json()

    latest_date_student = Student.query.order_by(Student.date.desc()).first()
    if latest_date_student:
        latest_date = latest_date_student.date.date()
        date = latest_date + timedelta(days=1)
    else:
        date = datetime.now().date()

    student = Student(name=data.get('name'), surname=data.get('surname'), room=data.get('room'),
                      chat_id=data.get('chat_id'), date=date)
    status = uploading_to_base(student)
    return status


@app.route('/api/problem', methods=['POST'])
def register_problem():
    data = request.get_json()
    chat_id = data.get('chat_id')
    student = Student.query.filter_by(chat_id=chat_id).first()
    date = datetime.now().date()
    problem = Problems(text=data.get('text'), date=date, student_id=student.id)
    status = uploading_to_base(problem)
    return status


@app.route('/api/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    query = Student.query.filter_by(chat_id=data['chat_id'])
    amount_of_students = len(Student.query.all())
    student = query.first()
    current_date = datetime.now().date()

    # Удаление студента
    query.delete()
    if student:
        # если дата дежурства удаляемого студента будет меньше текущей, то в ответе вернётся -1
        latest_duty_student = -1
        if student.date.date() >= current_date and amount_of_students > 2:
            latest_duty_student = Student.query.order_by(Student.date.desc()).first()
            latest_duty_student.date = student.date.date()

        try:
            db.session.commit()
        except Exception:
            logger.exception(f'Exeption occured {traceback.extract_stack()[-1][2]}', exc_info=True)
            db.session.rollback()
            return jsonify({'status': 'failed'}), 400
        # в ответе отравляем chat_id пользователя, для которого произошли изменения
        if latest_duty_student == -1:
            return jsonify({'status': '250 OK', 'chat_id': latest_duty_student})
        else:
            return jsonify({'status': '250 OK', 'chat_id': latest_duty_student.chat_id})
    return jsonify({'status': '255 OK'})


@app.route('/api/update', methods=['PATCH'])
def update():
    students_list = Student.query.all()
    current_date = datetime.now().date()
    for student in students_list:
        if student.date.date() < current_date:
            student.date += timedelta(days=len(students_list))
    status = commit()
    return status


def uploading_to_base(instance):
    db.session.add(instance)
    status = commit()
    return status


def commit():
    try:
        db.session.commit()
    except Exception:
        logger.exception(f'Exeption occured {traceback.extract_stack()[-1][2]}', exc_info=True)
        db.session.rollback()
        return jsonify({'status': 'failed'}), 400
    return jsonify({'status': '250 OK'})
