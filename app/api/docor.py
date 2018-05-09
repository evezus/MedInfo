from app import models, validate, app, db
from flask import Flask, jsonify, redirect, url_for, request


# TODO Перевіряти права
@app.route('/doctor/add', methods=['POST', 'GET'])
def doctor_add():
    if request.method == 'POST':
        try:
            hospital_id = int(request.form['hospital_id'])
        except Exception:
            return jsonify(
                {'error_code': '1', 'error_msg': 'Value [hospital_id] is not valid, value should be a number.'})

        try:
            user_id = int(request.form['user_id'])
        except Exception:
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [user_id] is not valid, value should be a number.'})

        try:
            type_doctor_id = int(request.form['type_doctor_id'])
        except Exception:
            return jsonify(
                {'error_code': '3', 'error_msg': 'Value [type_doctor_id] is not valid, value should be a number.'})

        check_hospital_id = db.session.query(models.Hospital.id).filter(
            models.Hospital.id == hospital_id).first()
        if check_hospital_id == None:
            return jsonify(
                {'error_code': '4', 'error_msg': 'Value [hospital_id] is not found.'})

        check_user_id = db.session.query(models.User.id).filter(
            models.User.id == user_id).first()
        if check_user_id == None:
            return jsonify(
                {'error_code': '5', 'error_msg': 'Value [user_id] is not found.'})

        check_type_doctor_id = db.session.query(models.TypeDoctor.id).filter(
            models.TypeDoctor.id == type_doctor_id).first()
        if check_type_doctor_id == None:
            return jsonify(
                {'error_code': '6', 'error_msg': 'Value [type_doctor_id] is not found.'})

        check_row = db.session.query(models.Doctor.id) \
            .filter(models.Doctor.hospital_id == hospital_id) \
            .filter(models.Doctor.user_id == user_id) \
            .filter(models.Doctor.type_doctor_id == type_doctor_id) \
            .first()

        if not check_row == None:
            return jsonify(
                {'error_code': '7', 'error_msg': 'Such an entry already exists'})

        try:
            doctor = models.Doctor(hospital_id=hospital_id, user_id=user_id, type_doctor_id=type_doctor_id)
            db.session.add(doctor)
            db.session.commit()
            return jsonify({'msg': 'Doctor successfully added.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '8', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})


@app.route('/doctor/addType', methods=['POST', 'GET'])
def doctor_addType():
    if request.method == 'POST':
        label = request.form['label']
        description = request.form['description']

        label = label.title()
        if not validate.description(label):
            return jsonify(
                {'error_code': '1', 'error_msg': 'Value [label] is not valid.'})

        if not validate.description(description):
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [description] is not valid.'})

        try:
            type_doctor = models.TypeDoctor(label=label, description=description)
            db.session.add(type_doctor)
            db.session.commit()
            return jsonify({'msg': 'Type Doctor successfully added.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '3', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})


@app.route('/doctor/get/<id>')
def doctor_get_id(id):
    try:
        hospital_id = int(id)
    except Exception:
        return jsonify(
            {'error_code': '1',
             'error_msg': 'Value [id] is not valid, value should be a number.'})

    try:
        doctor, user, hospital, type_doctor = db.session \
            .query(models.Doctor, models.User, models.Hospital, models.TypeDoctor) \
            .join(models.User) \
            .join(models.Hospital) \
            .join(models.TypeDoctor) \
            .filter(models.Doctor.id == id) \
            .first()
    except Exception:
        return jsonify({'error_code': '2', 'error_msg': 'Doctor does not exist.'})

    doctor_schema = models.DoctorSchema()
    doctor_json = doctor_schema.dump(doctor).data

    user_schema = models.UserSchema(
        only=('id', 'last_name', 'first_name', 'mid_name', 'photo_path', 'sex'))
    user_json = user_schema.dump(user).data

    hospital_schema = models.HospitalSchema()
    hospital_json = hospital_schema.dump(hospital).data

    type_doctor_schema = models.TypeDoctorSchema()
    type_doctor_json = type_doctor_schema.dump(type_doctor).data

    return jsonify({'doctor': doctor_json, 'user': user_json,
                    'hospital': hospital_json, 'type_doctor': type_doctor_json})


@app.route('/doctor/all')
def doctor_all():
    try:
        query = db.session \
            .query(models.Doctor, models.User, models.Hospital, models.TypeDoctor) \
            .join(models.User) \
            .join(models.Hospital) \
            .join(models.TypeDoctor) \
            .all()
    except Exception:
        return jsonify({'error_code': '1', 'error_msg': 'Doctors does not exist.'})

    doctors = []
    for doctor, user, hospital, type_doctor in query:
        doctor_schema = models.DoctorSchema()
        doctor_json = doctor_schema.dump(doctor).data

        user_schema = models.UserSchema(
            only=('id', 'last_name', 'first_name', 'mid_name', 'photo_path', 'sex'))
        user_json = user_schema.dump(user).data

        hospital_schema = models.HospitalSchema()
        hospital_json = hospital_schema.dump(hospital).data

        type_doctor_schema = models.TypeDoctorSchema()
        type_doctor_json = type_doctor_schema.dump(type_doctor).data
        doctors.append({'doctor': doctor_json, 'user': user_json,
                        'hospital': hospital_json, 'type_doctor': type_doctor_json})

    return jsonify({'count': len(query), 'doctors': doctors})


@app.route('/doctor/inHospital/<id>')
def doctor_in_hospital(id):
    try:
        hospital_id = int(id)
    except Exception:
        return jsonify(
            {'error_code': '1',
             'error_msg': 'Value [id] is not valid, value should be a number.'})

    try:
        query = db.session \
            .query(models.Doctor, models.User, models.Hospital, models.TypeDoctor) \
            .join(models.User) \
            .join(models.Hospital) \
            .join(models.TypeDoctor) \
            .filter(models.Hospital.id == id) \
            .all()
    except Exception:
        return jsonify({'error_code': '2', 'error_msg': 'Doctors does not exist.'})

    doctors = []
    for doctor, user, hospital, type_doctor in query:
        doctor_schema = models.DoctorSchema()
        doctor_json = doctor_schema.dump(doctor).data

        user_schema = models.UserSchema(
            only=('id', 'last_name', 'first_name', 'mid_name', 'photo_path', 'sex'))
        user_json = user_schema.dump(user).data

        type_doctor_schema = models.TypeDoctorSchema()
        type_doctor_json = type_doctor_schema.dump(type_doctor).data
        doctors.append({'doctor': doctor_json, 'user': user_json,
                        'type_doctor': type_doctor_json})

    return jsonify({'count': len(query), 'doctors': doctors})


