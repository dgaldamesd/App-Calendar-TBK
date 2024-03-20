from flask import Flask, render_template, request, redirect, url_for
from transbank.webpay.transaccion_completa.transaction import Transaction as TransaccionCompleta
from transbank.webpay.webpay_plus.transaction import Transaction as WebpayPlus
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/pay', methods=['GET'])
def pay():
    return render_template('pay.html')

@app.route('/transaccion-completa/create', methods=['POST'])
def create_transaccion_completa():
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = 20000
    return_url = request.url_root + 'transaccion-completa/commit'

    tx = TransaccionCompleta()
    response = tx.create(buy_order, session_id, amount)

    return redirect(response["url"])

@app.route('/transaccion-completa/commit', methods=['GET'])
def commit_transaccion_completa():
    token = request.args.get("token_ws")

    tx = TransaccionCompleta()
    response = tx.commit(token=token)

    return render_template('commit.html', response=response)

@app.route('/webpay-plus/create', methods=["GET"])
def create_webpay_plus():
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = 20000
    return_url = request.url_root + 'webpay-plus/commit'

    tx = WebpayPlus()
    response = tx.create(buy_order, session_id, amount, return_url)

    return redirect(response["url"])

@app.route('/webpay-plus/commit', methods=["GET"])
def commit_webpay_plus():
    token = request.args.get("token_ws")

    tx = WebpayPlus()
    response = tx.commit(token=token)

    return render_template('commit.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
