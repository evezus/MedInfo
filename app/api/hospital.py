import hashlib
import random
from app import models, validate, app, db
from flask import Flask, jsonify, redirect, url_for, request


@app.route('/hospital/add', methods=['POST', 'GET'])
def hospital_add():
    if request.method == 'POST':

        try:
            name = request.form['name']
            phone = request.form['phone']
            address = request.form['adress']
            worktime = request.form['worktime']
            location = request.form['location']
            obeys = 0
            type_hospital_id = request.form['type_hospital_id']
            propert = request.form['propert']
        except Exception:
            return jsonify({'error_code': '0',
                            'error_msg': 'Use POST parameters \
                            (name,phone,address,worktime,location,type_hospital_id,propert).'})

        # Validate Name
        name = name.title()
        if not validate.description(name):
            return jsonify(
                {'error_code': '1', 'error_msg': 'Value [name] is not valid.'})

        # Validate Phone
        if not validate.phone(phone):
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [phone] is not valid.'})

        # Check register phone
        check_phone = db.session.query(models.Hospital).filter(models.Hospital.phone == phone).first()
        if not check_phone == None:
            return jsonify(
                {'error_code': '3', 'error_msg': 'This [phone] is already in use.'})

        # Format and Validate Address
        address = address.title()
        if not validate.adress(address):
            return jsonify(
                {'error_code': '4', 'error_msg': 'Value [adress] is not valid.'})

        if not validate.worktime(worktime):
            return jsonify(
                {'error_code': '5', 'error_msg': 'Value [worktime] is not valid.'})

        if not validate.location(location):
            return jsonify(
                {'error_code': '6', 'error_msg': 'Value [location] is not valid.'})

        # Validate propert
        if not (propert == 'private' or propert == 'state'):
            return jsonify(
                {'error_code': '7', 'error_msg': 'Value [propert] is not valid.'})

        # Check register type_hospital_id
        try:
            type_hospital_id = int(type_hospital_id)
        except:
            return jsonify(
                {'error_code': '8', 'error_msg': 'Value [type_hospital_id] is not valid, value should be a number.'})

        check_type_hospital_id = db.session.query(models.TypeHospital).filter(
            models.TypeHospital.id == type_hospital_id).first()
        if check_type_hospital_id == None:
            return jsonify(
                {'error_code': '9', 'error_msg': 'Value [type_hospital_id] is not found.'})

        try:
            hospital = models.Hospital(name=name, phone=phone, adress=address, worktime=worktime, location=location,
                                       obeys=obeys, type_hospital_id=type_hospital_id, propert=propert)
            db.session.add(hospital)
            db.session.commit()
            return jsonify({'msg': 'Hospital successfully added.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '10', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})


@app.route('/hospital/addType', methods=['POST', 'GET'])
def hospital_add_type():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not validate.name(name):
            return jsonify(
                {'error_code': '1', 'error_msg': 'Value [name] is not valid.'})

        if not validate.description(description):
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [description] is not valid.'})

        try:
            type_hospital = models.TypeHospital(name, description)
            id = db.session.add(type_hospital)
            db.session.commit()
            return jsonify({'msg': 'Type of hospital successfully added.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '3', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})


