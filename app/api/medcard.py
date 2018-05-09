from datetime import datetime, timedelta
from app import models, validate, app, db, auxiliary_metods
from flask import Flask, jsonify, redirect, url_for, request


########################################################################################################################

# Medcard info GET
@app.route('/medcard/info/get', methods=['POST', 'GET'])
def medcard_info_get():
    if request.method == 'POST':
        token = request.form['access_token']
        if not validate.hash(token):
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        result_query = db.session.query(models.MedcardInfo) \
            .filter(models.MedcardInfo.user_id == user.id) \
            .first()

        if result_query == None:
            try:
                medcard_info = models.MedcardInfo(user_id=user.id, blood_type='0', main_diagnosis='-',
                                                  allergic_history='-',
                                                  drug_intolerance='-',
                                                  physical_injury='-')
                db.session.add(medcard_info)
                db.session.commit()

                medcard_info_schema = models.MedcardInfoSchema()
                output = medcard_info_schema.dump(medcard_info).data

                return jsonify(
                    {'MedcardInfo': output})
            except Exception:
                return jsonify(
                    {'error_code': '3', 'error_msg': 'Try again later.'})

        medcard_info_schema = models.MedcardInfoSchema()
        output = medcard_info_schema.dump(result_query).data

        return jsonify({'MedcardInfo': output})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})


# Medcard info SET
@app.route('/medcard/info/set', methods=['POST', 'GET'])
def medcard_info_set():
    params = {}
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            params['blood_type'] = request.form['blood_type']
            if not validate.blood_type(params['blood_type']):
                return jsonify(
                    {'error_code': '3', 'error_msg': 'Value [blood_type] is not valid.'})
        except:
            pass

        try:
            params['main_diagnosis'] = request.form['main_diagnosis']
            if not validate.description(params['main_diagnosis']):
                return jsonify({'error_code': '4', 'error_msg': 'Value [main_diagnosis] is not valid.'})
        except:
            pass

        try:
            params['allergic_history'] = request.form['allergic_history']
            if not validate.description(params['allergic_history']):
                return jsonify(
                    {'error_code': '5', 'error_msg': 'Value [allergic_history] is not valid.'})
        except:
            pass

        try:
            params['drug_intolerance'] = request.form['drug_intolerance']
            if not validate.description(params['drug_intolerance']):
                return jsonify(
                    {'error_code': '6', 'error_msg': 'Value [drug_intolerance] is not valid.'})
        except:
            pass

        try:
            params['physical_injury'] = request.form['physical_injury']
            if not validate.description(params['physical_injury']):
                return jsonify(
                    {'error_code': '7', 'error_msg': 'Value [physical_injury] is not valid.'})
        except:
            pass

        if len(params) == 0:
            return jsonify(
                {'error_code': '8', 'error_msg': 'Specify at least one parameter.'})

        result_query = db.session.query(models.MedcardInfo) \
            .filter(models.MedcardInfo.user_id == user.id) \
            .first()

        if result_query == None:
            try:
                medcard_info = models.MedcardInfo(user_id=user.id, blood_type='0', main_diagnosis='-',
                                                  allergic_history='-',
                                                  drug_intolerance='-',
                                                  physical_injury='-')
                db.session.add(medcard_info)
                db.session.commit()
            except Exception:
                db.session.rollback()
                return jsonify({'error_code': '9', 'error_msg': 'Try again later.'})

        try:
            print(params)
            db.session.query(models.MedcardInfo) \
                .filter(models.MedcardInfo.user_id == user.id).update(params)
            db.session.commit()
            return jsonify({'Set': 'True'})
        except Exception:
            db.session.rollback()
            return jsonify(
                {'error_code': '9', 'error_msg': 'Try again later.'})

        return jsonify({'MedcardInfo': output})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})


########################################################################################################################

# Medcard vactination type add
@app.route('/medcard/type_vaccination/add', methods=['POST', 'GET'])
def medcard_type_vaccination_add():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            name = request.form['name']
            if not validate.description(name):
                return jsonify(
                    {'error_code': '3', 'error_msg': 'Value [name] is not valid.'})
        except:
            return jsonify({'error_code': '3', 'error_msg': 'Value [name] is not valid.'})

        try:
            description = request.form['description']
            if not validate.description(description):
                return jsonify({'error_code': '4', 'error_msg': 'Value [description] is not valid.'})
        except:
            return jsonify({'error_code': '4', 'error_msg': 'Value [description] is not valid.'})

        try:
            type_vaccination = models.TypeVaccination(name=name, description=description)
            db.session.add(type_vaccination)
            db.session.commit()
            return jsonify({'Good': 'Add type vaccination.'})
        except:
            db.session.rollback()
            return jsonify({'error_code': '5', 'error_msg': 'Try again later.'})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})


# Medcard vactination type del
@app.route('/medcard/type_vaccination/del', methods=['POST', 'GET'])
def medcard_type_vaccination_del():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)
        if user == None: return jsonify(
            {'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            id = int(request.form['id'])
        except:
            return jsonify({'error_code': '2', 'error_msg': 'Value [id] is not valid.'})

        try:
            db.session.query(models.TypeVaccination).filter(models.TypeVaccination.id == id).delete()
            db.session.commit()
            return jsonify({'Good': 'Deleted type vaccination.'})
        except:
            db.session.rollback()
            return jsonify({'error_code': '3', 'error_msg': 'Try again later.'})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})


########################################################################################################################

@app.route('/medcard/vaccination/add', methods=['POST', 'GET'])
def medcard_vaccination_add():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)
        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            type_vaccination_id = int(request.form['type_vaccination_id'])
            result = db.session.query(models.TypeVaccination.id).filter(
                models.TypeVaccination.id == type_vaccination_id).first()
            if result == None: raise Exception()
        except:
            return jsonify({'error_code': '3', 'error_msg': 'Value [type_vaccination_id] is not valid.'})

        try:
            reaction = int(request.form['reaction'])
            if not (reaction > 0 and reaction < 100): raise Exception()
        except:
            return jsonify({'error_code': '4', 'error_msg': 'Value [reaction] is not valid.'})

        try:
            date_vaccination = request.form['date_vaccination']
            date_vaccination = datetime.strptime(date_vaccination, "%d-%m-%Y %H:%M")
            if not date_vaccination < datetime.now(): raise Exception()
        except Exception as ex:
            print(ex)
            return jsonify({'error_code': '5', 'error_msg': 'Value [date_vaccination] is not valid.'})

        try:
            medcard_vaccination = models.MedcardVaccination(user_id=user.id, type_vaccination_id=type_vaccination_id,
                                                            reaction=reaction, date_vaccination=date_vaccination)
            db.session.add(medcard_vaccination)
            db.session.commit()
            id = medcard_vaccination.id
            return jsonify({'Good': 'Add vaccination.', 'id': id})
        except Exception as ex:
            print(ex)
            db.session.rollback()
            return jsonify({'error_code': '6', 'error_msg': 'Try again later.'})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})


@app.route('/medcard/vaccination/del', methods=['POST', 'GET'])
def medcard_vaccination_del():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)
        if user == None: return jsonify(
            {'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        try:
            id = int(request.form['id'])
        except:
            return jsonify({'error_code': '2', 'error_msg': 'Value [id] is not valid.'})

        try:
            db.session.query(models.MedcardVaccination).filter(models.MedcardVaccination.id == id).delete()
            db.session.commit()
            return jsonify({'Good': 'Deleted vaccination.' , 'id': id})
        except:
            db.session.rollback()
            return jsonify({'error_code': '3', 'error_msg': 'Try again later.'})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})

########################################################################################################################

@app.route('/medcard/complaints/add', methods=['POST', 'GET'])
def medcard_complaints_add():
    if request.method == 'POST':
        try:
            token = request.form['access_token']
            if not validate.hash(token):
                raise Exception('Access token is not valid.')
        except:
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)
        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

    return jsonify({'error_code': '0', 'error_msg': 'Use POST parameters.'})