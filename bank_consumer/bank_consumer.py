from flask import Flask,request,render_template

papp = Flask(__name__)

class Account:

    def __init__(self,accNm,accBal,accTy,accAdr,accNo=0):
        self.accNo=accNo
        self.accBal=accBal
        self.accHolderName=accNm
        self.accHolderAdr=accAdr
        self.accType=accTy

    def __str__(self):
        return f'''{self.__dict__}'''

    def __repr__(self):
        return str(self)

def dummy_account():
    return Account(accNm='',accBal=0.0,accTy='',accAdr='',accNo=0)



import requests


def get_active_accounts():
    response = requests.get('http://localhost:5001/hdfc/account/')
    return response.json()

def get_active_account(accno):
    response = requests.get('http://localhost:5001/hdfc/account/{}'.format(accno))
    if response.json().get("status"):
        return False
    return response.json()


@papp.route("/producer/account/welcome/")
def show_account_page():
    return render_template('bank.html',
                           accounts = get_active_accounts(),
                           account = dummy_account())



@papp.route("/producer/account/save/",methods=["POST"])
def add_account():

    record = get_active_account(request.form["accNo"])
    userenterdinfo = Account(accNo=request.form["accNo"],accNm=request.form["accHolderName"],
                             accBal=request.form["accBal"],
                             accTy=request.form["accType"],
                             accAdr=request.form["accHolderAdr"])

    if record:
    #consumer -- To Producer --
        response = requests.put('http://localhost:5001/hdfc/account/{}'
                                .format(userenterdinfo.accNo)
                  ,json=userenterdinfo.__dict__)
        if len(response.json())>0:
            msg="Updated Successfully...!"
    else:
        response = requests.post('http://localhost:5001/hdfc/account/'
                                , json=userenterdinfo.__dict__)
        msg= response.text

    print(response.status_code)

    return render_template("bank.html",msg=msg,accounts = get_active_accounts(),
                           account=dummy_account())

@papp.route("/producer/account/edit/<int:aid>")
def fetch_for_edit(aid):
    response = requests.get("http://localhost:5001/hdfc/account/{}".format(aid))
    if response.json().__contains__("status"):
            msg = response.json()["status"]

    return render_template("bank.html", accounts=get_active_accounts(),
                           account=response.json())


@papp.route("/producer/account/delete/<int:aid>")
def fetch_for_delete(aid):
    record= get_active_account(aid)

    if record:
        response = requests.delete("http://localhost:5001/hdfc/account/{}".format(aid))
        msg=response.text
    else:
        msg="Cannot delete"
    return render_template("bank.html",msg=msg,
                           accounts=get_active_accounts(),
                           account=dummy_account())

if __name__ == '__main__':
    papp.run(debug=True,port=5000)
