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