import hashlib
import random
from app import models, validate, app, db, auxiliary_metods
from flask import Flask, jsonify, redirect, url_for, request


@app.route('/account/auth', methods=['POST', 'GET'])
def account_auth():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['passwd']
        if not (validate.email(email) and validate.passwd(passwd)):
            return jsonify({'error_code': '1',
                            'error_msg': 'User authorization failed: email or password not valid.'})

        hash = hashlib.sha256(passwd.encode('utf-8'))
        passwd = hash.hexdigest()

        user = db.session.query(models.User) \
            .filter(models.User.email == email) \
            .filter(models.User.password == passwd).first()

        if user == None:
            return jsonify({'error_code': '2',
                            'error_msg': 'User authorization failed: email or password not found.'})

        # generate token key
        passwd = random.sample(list(str(passwd)), k=random.randint(32, 64))
        hash = hashlib.sha256(''.join(passwd).encode('utf-8'))
        token = hash.hexdigest()

        try:
            db.session.query(models.User).filter(models.User.id == user.id).update({'token': token})
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({'error_code': '3', 'error_msg': 'Error connect to database.'})

        return jsonify({'access_token': token})

    return jsonify({'error_code': '0',
                    'error_msg': 'User authorization failed: post parameters [email], [password] not found.'})


@app.route('/account/getInfo', methods=['POST', 'GET'])
def account_getInfo():
    if request.method == 'POST':
        token = request.form['access_token']
        if not validate.hash(token):
            return jsonify({'error_code': '1', 'error_msg': 'Access token is not valid.'})

        user = auxiliary_metods.get_user(token)

        if user == None:
            return jsonify({'error_code': '2', 'error_msg': 'User authorization failed: no access token passed.'})

        user_schema = models.UserSchema()
        output = user_schema.dump(user).data

        return jsonify({'account': output})

    return jsonify({'error_code': '0',
                    'error_msg': 'User authorization failed: post parameters [access_token] not found.'})


@app.route('/account/register', methods=['POST', 'GET'])
def account_register():
    if request.method == 'POST':
        print(request.form)
        try:
            email = request.form['email']
            date_of_birth = request.form['date_of_birth']
            last_name = request.form['last_name']
            mid_name = request.form['mid_name']
            first_name = request.form['first_name']
            phone = request.form['phone']
            sex = request.form['sex']
            # address = request.form['address']
            password = request.form['password']
            utype = 'patient'
        except:
            return jsonify({'error_code': '0',
                            'error_msg': 'Use POST parameters.'})

        # Validation EMAIL
        email = email.lower()
        if not validate.email(email):
            return jsonify(
                {'error_code': '1', 'error_msg': 'Value [email] is not valid.'})

        # Validate Phone
        if not validate.phone(phone):
            return jsonify(
                {'error_code': '2', 'error_msg': 'Value [phone] is not valid.'})

        # Check register email
        check_email = db.session.query(models.User).filter(models.User.email == email).first()
        if not check_email == None:
            return jsonify(
                {'error_code': '4', 'error_msg': 'This [email] is already in use.'})

        # Check register phone
        check_phone = db.session.query(models.User).filter(models.User.phone == phone).first()
        if not check_phone == None:
            return jsonify(
                {'error_code': '5', 'error_msg': 'This [phone] is already in use.'})

        # Validation date_of_birth
        if not validate.date(date_of_birth):
            return jsonify(
                {'error_code': '6', 'error_msg': 'Value [date_of_birth] is not valid.'})

        # Format Date
        date_of_birth = validate.format_date(date_of_birth)

        # Format and Validate NAME
        last_name = last_name.title()
        mid_name = mid_name.title()
        first_name = first_name.title()

        if not (validate.name(last_name) and validate.name(mid_name) and validate.name(first_name)):
            return jsonify(
                {'error_code': '7', 'error_msg': 'Value name is not valid.'})

        # Check Sex
        if not (sex == 'male' or sex == 'female'):
            return jsonify(
                {'error_code': '8', 'error_msg': 'Value [sex] is not valid.'})

        # Create Photo Path
        photo_path = '/user-photo/default.png'

        # Format and Validate Address
        address = ''
        '''
        address = address.title()
        if not validate.adress(address):
            return jsonify(
                {'error_code': '9', 'error_msg': 'Value [address] is not valid.'})
        '''

        # Check PASSWORD
        if not validate.passwd(password):
            return jsonify(
                {'error_code': '10', 'error_msg': 'Value [password] is not valid.'})

        hash = hashlib.sha256(password.encode('utf-8'))
        password = hash.hexdigest()
        try:
            user = models.User(email, date_of_birth, last_name, mid_name, first_name, phone,
                               sex, photo_path, address, utype, password, 'none')
            db.session.add(user)
            db.session.commit()
            return jsonify({'msg': 'Good registration.'})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'error_code': '11', 'error_msg': 'Error connect to database.'})

    return jsonify({'error_code': '0',
                    'error_msg': 'Use POST parameters.'})
