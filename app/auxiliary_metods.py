import string
import hashlib
import random
from . import db, models

def get_user(token):
    user = db.session \
        .query(models.User.id,
               models.User.first_name, models.User.mid_name, models.User.last_name,
               models.User.email, models.User.date_of_birth, models.User.phone,
               models.User.adress, models.User.sex, models.User.utype, models.User.photo_path) \
        .filter(models.User.token == token) \
        .first()

    return user

def id_generator(chars=string.ascii_uppercase + string.digits):
    rnd = random.sample(''.join(random.choice(chars) for _ in range(64)), k=random.randint(32, 64))
    rnd_hash = hashlib.sha256(''.join(rnd).encode('utf-8')).hexdigest()
    return rnd_hash