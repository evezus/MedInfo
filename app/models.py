from . import db, ma
from sqlalchemy import Column, Integer, String, Enum, DATETIME, Text, VARCHAR, ForeignKey, DATE


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    date_of_birth = Column(DATE, nullable=False)
    last_name = Column(String(50), nullable=False)
    mid_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone = Column(String(12), unique=True, nullable=False)
    sex = Column(Enum('male', 'female'), nullable=False)
    photo_path = Column(String(200), nullable=True)
    adress = Column(String(100), nullable=True)
    utype = Column(Enum('patient', 'doctor'),
                   default='patient')
    password = Column(String(64), nullable=False)
    token = Column(String(64), nullable=True)

    def __init__(self, email, date_of_birth, last_name, mid_name, first_name, phone,
                 sex, photo_path, adress, utype, password, token):
        self.email = email
        self.date_of_birth = date_of_birth
        self.last_name = last_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.first_name = first_name
        self.phone = phone
        self.sex = sex
        self.photo_path = photo_path
        self.adress = adress
        self.utype = utype
        self.password = password
        self.token = token

    def __repr__(self):
        return '<User id:{0} [{1} {2} {3}]>'.format(self.id, self.last_name, self.first_name, self.mid_name)


class TypeHospital(db.Model):
    __tablename__ = 'type_hospital'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Type_Hospital id:{0} name:{1} description:{2}>'.format(self.id, self.name, self.description)


class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(14), nullable=False)
    adress = Column(String(100), nullable=True)
    worktime = Column(String(50), nullable=False)
    location = Column(String(200), nullable=True)
    obeys = Column(Integer, nullable=True)
    type_hospital_id = Column(Integer, ForeignKey('type_hospital.id'))
    propert = Column(Enum('private', 'state'),
                     default='state')
    img_logo = Column(String(200), nullable=True)
    img_panorama = Column(String(200), nullable=True)
    img_small = Column(String(200), nullable=True)

    db.relationship("TypeHospital", backref=db.backref("type_hospital", uselist=False))

    def __init__(self, name, phone, adress, worktime, location, obeys,
                 type_hospital_id, propert=None, img_logo=None, img_panorama=None,
                 img_small=None):
        self.name = name
        self.phone = phone
        self.adress = adress
        self.worktime = worktime
        self.location = location
        self.obeys = obeys
        self.type_hospital_id = type_hospital_id
        self.propert = propert
        self.img_logo = img_logo
        self.img_panorama = img_panorama
        self.img_small = img_small

    def __repr__(self):
        return '<Hospital id:{0} name:{1} adress:{2}>'.format(self.id, self.name, self.adress)


class TypeDoctor(db.Model):
    __tablename__ = 'type_doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)

    def __init__(self, label, description=None):
        self.label = label
        self.description = description

    def __repr__(self):
        return '<Type_Doctor id:{0} label:{1} description:{2}>'.format(self.id, self.label, self.description)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey('hospital.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    type_doctor_id = Column(Integer, ForeignKey('type_doctor.id'))

    db.relationship("Hospital", backref=db.backref("hospital", uselist=False))
    db.relationship("User", backref=db.backref("user", uselist=False))
    db.relationship("TypeDoctor", backref=db.backref("type_doctor", uselist=False))

    def __init__(self, hospital_id, user_id, type_doctor_id):
        self.hospital_id = hospital_id
        self.user_id = user_id
        self.type_doctor_id = type_doctor_id

    def __repr__(self):
        return '<Doctor id:{0} hospital_id:{1} user_id:{2} type_doctor_id:{3}>'.format(
            self.id, self.hospital_id, self.user_id, self.type_doctor_id)


class Record(db.Model):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    pacient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date_record = Column(DATETIME, nullable=False)
    date_create = Column(DATETIME, nullable=False)

    db.relationship("Doctor", backref=db.backref("doctor", uselist=False))
    db.relationship("User", backref=db.backref("user", uselist=False))

    def __init__(self, doctor_id, pacient_id, date_record, date_create):
        self.doctor_id = doctor_id
        self.pacient_id = pacient_id
        self.date_record = date_record
        self.date_create = date_create

    def __repr__(self):
        return '<Record id:{0} doctor_id:{1} pacient_id:{2} date_record:{3}>'.format(
            self.id, self.doctor_id, self.pacient_id, self.date_record)


class MedcardInfo(db.Model):
    __tablename__ = 'medcard_info'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    blood_type = Column(Text, default='-')
    main_diagnosis = Column(Text, default='-')
    allergic_history = Column(Text, default='-')
    drug_intolerance = Column(Text, default='-')
    physical_injury = Column(Text, default='-')

    db.relationship("User", backref=db.backref("user", uselist=False))

    def __init__(self, user_id, blood_type=None, main_diagnosis=None, allergic_history=None,
                 drug_intolerance=None, physical_injury=None):
        self.user_id = user_id
        self.blood_type = blood_type
        self.main_diagnosis = main_diagnosis
        self.allergic_history = allergic_history
        self.drug_intolerance = drug_intolerance
        self.physical_injury = physical_injury

    def __repr__(self):
        return '<Medcard_Info user_id:{0} blood_type:{1} main_diagnosis:{2} allergic_history:{3}  drug_intolerance:{4} physical_injury:{5}>'.format(
            self.user_id, self.blood_type, self.main_diagnosis, self.allergic_history, self.drug_intolerance,
            self.physical_injury)


class MedcardIndexes(db.Model):
    __tablename__ = 'medcard_indexes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    value = Column(Text, nullable=False)
    date_create = Column(DATETIME, nullable=False)
    utype = Column(VARCHAR(10), nullable=False)
    description = Column(Text, nullable=False)

    db.relationship("User", backref=db.backref("user", uselist=False))

    def __init__(self, doctor_id, pacient_id, date_record, date_create):
        self.doctor_id = doctor_id
        self.pacient_id = pacient_id
        self.date_record = date_record
        self.date_create = date_create

    def __repr__(self):
        return '<Record id:{0} doctor_id:{1} pacient_id:{2} date_record:{3}>'.format(
            self.id, self.doctor_id, self.pacient_id, self.date_record)


class MedcardComplaints(db.Model):
    __tablename__ = 'medcard_complaints'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    value = Column(Text, nullable=False)
    date_create = Column(DATETIME, nullable=False)
    utype = Column(VARCHAR(10), nullable=False)
    description = Column(Text, nullable=False)

    db.relationship("User", backref=db.backref("user", uselist=False))

    def __init__(self, user_id, value, date_create, utype, description):
        self.user_id = user_id
        self.value = value
        self.date_create = date_create
        self.utype = utype
        self.description = description

    def __repr__(self):
        return '<Medcard_Complaints user_id:{0} value:{1} date_create:{2} utype:{3} description:{4}>'.format(
            self.user_id, self.value, self.date_create, self.utype, self.description)


class TypeVaccination(db.Model):
    __tablename__ = 'type_vaccination'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Type_Vaccination id:{0} name:{1} description:{2}>'.format(
            self.id, self.name, self.description)


class MedcardVaccination(db.Model):
    __tablename__ = 'medcard_vaccination'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    type_vaccination_id = Column(Integer, ForeignKey('type_vaccination.id'))
    reaction = Column(Integer, nullable=False)
    date_vaccination = Column(DATETIME, nullable=False)

    db.relationship("User", backref=db.backref("user", uselist=False))
    db.relationship("TypeVaccination", backref=db.backref("type_vaccination", uselist=False))

    def __init__(self, user_id, type_vaccination_id, reaction, date_vaccination):
        self.user_id = user_id
        self.type_vaccination_id = type_vaccination_id
        self.reaction = reaction
        self.date_vaccination = date_vaccination


    def __repr__(self):
        return '<Medcard_Vaccination id:{0} user_id:{1} type_vaccination_id:{2} reaction:{3}  date_vaccination:{4}>'.format(
            self.id, self.user_id, self.type_vaccination_id, self.reaction, self.date_vaccination)


############### Schema #################
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class TypeHospitalSchema(ma.ModelSchema):
    class Meta:
        model = TypeHospital


class HospitalSchema(ma.ModelSchema):
    class Meta:
        model = Hospital
        include_fk = True


class TypeDoctorSchema(ma.ModelSchema):
    class Meta:
        model = TypeDoctor


class DoctorSchema(ma.ModelSchema):
    class Meta:
        model = Doctor


class RecordSchema(ma.ModelSchema):
    class Meta:
        model = Record


class MedcardInfoSchema(ma.ModelSchema):
    class Meta:
        model = MedcardInfo


class MedcardIndexesSchema(ma.ModelSchema):
    class Meta:
        model = MedcardIndexes


class MedcardComplaintsSchema(ma.ModelSchema):
    class Meta:
        model = MedcardComplaints


class TypeVaccinationSchema(ma.ModelSchema):
    class Meta:
        model = TypeVaccination


class MedcardVaccinationSchema(ma.ModelSchema):
    class Meta:
        model = MedcardVaccination


########################################


# Create DB
if __name__ == '__main__':
    db.create_all()
    print('Create database successfully!')
