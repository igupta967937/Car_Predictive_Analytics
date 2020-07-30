import pickle
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def regressing(userDetails):
    year = 2020 - int(userDetails['year'])
    price = float(userDetails['price'])
    kms = int(userDetails['kms'])
    fl = userDetails['fuel']
    sl = userDetails['seller']
    trn = userDetails['transmission']
    own = userDetails['owner']

    if fl == "Petrol":
        fuel_1 = 0
        fuel_2 = 1
    elif fl == "Diesel":
        fuel_1 = 1
        fuel_2 = 0
    else:
        fuel_1 = 0
        fuel_2 = 0

    if sl == "Dealer":
        seller = 0
    else:
        seller = 1

    if trn == "Manual":
        transmission = 1
    else:
        transmission = 0

    if own == 0:
        owner_1 = 0
        owner_2 = 0
    elif own == 1:
        owner_1 = 1
        owner_2 = 0
    else:
        owner_1 = 0
        owner_2 = 1

    file = open('Model/Prediction', 'rb')
    regressor = pickle.load(file)
    file.close()

    value = regressor.predict([[year, price, kms, fuel_1, fuel_2, seller, transmission, owner_1, owner_2]])
    return value[0]


@app.route('/getinfo', methods=['GET', 'POST'])
def getinfo():
    if request.method == 'POST':
        userDetails = request.form
        val = regressing(userDetails)
        val = round(val, 2)
    return render_template('result.html', value=val)


if __name__ == '__main__':
    app.run(debug=True)
