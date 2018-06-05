from datetime import datetime, timedelta
from app import models, validate, app, db, ma, auxiliary_metods
from flask import Flask, jsonify, redirect, url_for, request


@app.route('/record/add', methods=['POST', 'GET'])
def record_add():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                raise Exception('Access token is not valid.')
            user = auxiliary_metods.get_user(token)
        except Exception:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        try:
            doctor_id = int(request.form['doctor_id'])
        except Exception:
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [doctor_id] is not valid, value should be a number.'})

        if doctor_id == user.id:
            return jsonify(
                {'error_code': '3', 'error_msg': 'It is impossible to enroll in the reception.'})

        check_doctor = db.session.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if check_doctor == None:
            return jsonify(
                {'error_code': '4', 'error_msg': 'Value [doctor_id] is not found.'})
        try:
            date_create = datetime.now()
            date_record = request.form['date_record']
            date_record = datetime.strptime(date_record, "%d-%m-%Y %H:%M")
        except Exception:
            return jsonify(
                {'error_code': '5', 'error_msg': 'Value [date_record] is not valid.'})

        min_interval = (datetime.now() + timedelta(days=1))
        max_interval = (datetime.now() + timedelta(days=30))
        if not date_record > min_interval and date_record < max_interval:
            return jsonify(
                {'error_code': '6', 'error_msg': 'You can not enroll in the reception now.'})

        check_time_record = db.session.query(models.Record) \
            .filter(models.Record.date_record == date_record) \
            .filter(models.Record.doctor_id == doctor_id) \
            .first()

        if not check_time_record == None:
            return jsonify(
                {'error_code': '7', 'error_msg': 'This time is already busy.'})

        try:
            record = models.Record(doctor_id=doctor_id, pacient_id=user.id, date_record=date_record,
                                   date_create=date_create)
            db.session.add(record)
            db.session.commit()
            return jsonify({'msg': 'Record successfully added.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '8', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})


@app.route('/record/get', methods=['POST', 'GET'])
def record_get():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
            user = auxiliary_metods.get_user(token)
        except Exception:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        query = db.session.query(models.Record, models.Doctor, models.User, models.Hospital, models.TypeDoctor) \
            .join(models.Doctor) \
            .join(models.User) \
            .join(models.Hospital) \
            .join(models.TypeDoctor) \
            .filter(models.Record.pacient_id == user.id) \
            .all()

        list_records = []
        for record, doctor, user, hospital, type_doctor in query:

            records_schema = models.RecordSchema()
            record_json = records_schema.dump(record).data

            doctor_schema = models.DoctorSchema()
            doctor_json = doctor_schema.dump(doctor).data

            user_schema = models.UserSchema(
                only=('last_name', 'first_name', 'mid_name', 'photo_path', 'sex'))
            user_json = user_schema.dump(user).data

            hospital_schema = models.HospitalSchema()
            hospital_json = hospital_schema.dump(hospital).data

            type_doctor_schema = models.TypeDoctorSchema()
            type_doctor_json = type_doctor_schema.dump(type_doctor).data

            list_records.append({'record': record_json, 'doctor': doctor_json, 'user': user_json,
                        'hospital': hospital_json, 'type_doctor': type_doctor_json})

        return jsonify({'records': list_records})


@app.route('/record/del', methods=['POST', 'GET'])
def record_del():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                raise('Access token is not valid.')
            user = auxiliary_metods.get_user(token)
        except Exception:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            record_id = int(request.form['record_id'])
        except Exception:
            return jsonify(
                {'error_code': '3', 'error_msg': 'Value [record_id] is not valid, value should be a number.'})

        try:
            db.session.query(models.Record).filter(models.Record.id == record_id).delete()
            db.session.commit()
            return jsonify({'Good': 'Deleted record.' , 'record_id': record_id})
        except:
            db.session.rollback()
            return jsonify({'error_code': '4', 'error_msg': 'Try again later.'})
        return jsonify({'records'})
