import requests
from flask import Flask,render_template,request


app = Flask(__name__)

@app.route("/gpay/app/",methods=["POST","GET"])
def get_account_balance():
    msg=''
    if request.method=='POST':
        accNo = request.form["accNo"]
        response= requests.get('http://localhost:5001/hdfc/account/{}/check/'.format(accNo))
        if response.json().get("status"):
            msg= response.json()["status"]
        else:
            msg = response.json()["balance"]
    return render_template('paytm.html',msg=msg)


if __name__ == '__main__':
    app.run(debug=True,port=5002)
