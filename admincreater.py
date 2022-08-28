from application import db
from application.models import *



if not Users.query.filter(Users.name=='admin').first():
        from application import bcrpyt
        user1 = Users(name='admin', email='admin@ecommerce.com',address='admin address',city='city',state='state',zip='123456',password=bcrpyt.generate_password_hash('password'))
        user1.roles.append(Role(name='Admin'))
        db.session.add(user1)
        db.session.commit()