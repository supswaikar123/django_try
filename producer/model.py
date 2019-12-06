from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@#Supr@localhost/pydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=False
db = SQLAlchemy(app)

class Account(db.Model):
    accNo = db.Column("accNo",db.Integer(),primary_key=True)
    accBal = db.Column("accBal",db.Float())
    accType = db.Column("accType",db.String(100))
    accHolder=db.Column("accHolderName",db.String(100))
    accHolderAdr=db.Column("accHolderAddress",db.String(100))
    active = db.Column('active',db.String(10),default='Y')

if __name__ == '__main__':
    db.create_all()
    ac1 = Account(accNo=1111,accBal=2929.34,accType='Saving',accHolder='ABCD',accHolderAdr='Pune')
    db.session.add(ac1)
    db.session.commit()
