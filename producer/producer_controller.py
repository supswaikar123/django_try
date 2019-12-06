from flask import request as req, redirect,url_for
from API.bank.producer.model import app,db,Account


import random

import json

@app.route("/hdfc/account/")
def get_active_Accounts():
    acc = Account.query.filter(Account.active=='Y')
    listOfActiveAccounts =[]
    for ac in acc:
        print(ac.__dict__)
        ac.__dict__.pop('_sa_instance_state')
        listOfActiveAccounts.append(ac.__dict__)
    return json.dumps(listOfActiveAccounts)


@app.route("/hdfc/account/<int:accno>")
def get_active_single_account(accno):
    acc = Account.query.filter_by(accNo=accno).first()
    if acc:
        acc.__dict__.pop('_sa_instance_state')
        return json.dumps(acc.__dict__)
    else:
        return {"status" :"No account present.."}


@app.route("/hdfc/account/<int:aid>",methods=["PUT"])
def update_account(aid):
    request = req.get_json()
    dbacc = Account.query.filter_by(accNo=aid).first()

    dbacc.accBal=request["accBal"]
    dbacc.accType = request["accType"]
    dbacc.accHolder = request["accHolderName"]
    dbacc.accHolderAdr = request["accHolderAdr"]
    db.session.commit()
    return redirect(url_for('get_active_Accounts'))


@app.route("/hdfc/account/",methods=["POST"])
def add_account():
    request = req.get_json()
    userAccData = Account(accNo=random.randint(1111,9999),
                  accBal=request["accBal"],
                  accType=request["accType"],
                  accHolder=request["accHolderName"],
                  accHolderAdr=request["accHolderAdr"])
    db.session.add(userAccData)
    db.session.commit()
    return "Account <{}> Added Successfully...!".format(userAccData.accNo)


@app.route("/hdfc/account/<int:accno>",methods=["DELETE"])
def delete_account(accno):
    dbacc = Account.query.filter_by(accNo=accno).first()
    dbacc.active='N'
    db.session.commit()
    return "Account <{}> Deleted Successfully...!".format(dbacc.accNo)


@app.route("/hdfc/account/<int:accno>/check/",methods=["GET"])
def check_account_balance(accno):
    dbAcc=Account.query.filter_by(accNo=accno).first()
    if dbAcc and dbAcc.active=='Y':
        return {"balance" : dbAcc.accBal}
    else:
        return {"status" : "Try after sometime"}
def withdraw_amount():
    pass

def deposit_amount():
    pass


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=5001)
