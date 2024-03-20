from flask import Flask, Blueprint, render_template, request
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
import random
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, '/home/devasc/labs/DEVELOPERS-OFF-FUTURE/APP-Calendar-TKB/templates')

bp = Blueprint('webpay_plus', __name__)

@bp.route('/create', methods=["GET"])
def webpay_plus_create():
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = 20000
    return_url = request.url_root + 'webpay-plus/commit'

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = Transaction().create(buy_order, session_id, amount, return_url)

    print(response)

    return render_template('webpay/plus/create.html', request=create_request, response=response)

@bp.route('/commit', methods=["GET", "POST"])
def webpay_plus_commit():
    if request.method == "GET":
        token = request.args.get("token_ws")
    else:
        token = request.form.get("token_ws")
        print("commit error for token_ws: {}".format(token))
        response = {
            "error": "Transacción con errores"
        }
        return render_template('webpay/plus/commit.html', token=token, response=response)    
    
    print("commit for token_ws: {}".format(token))
    response = Transaction().commit(token=token)
    print("response: {}".format(response))
    return render_template('webpay/plus/commit.html', token=token, response=response)

@bp.route('/refund', methods=["POST"])
def webpay_plus_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    print("refund for token_ws: {} by amount: {}".format(token, amount))

    try:
        response = Transaction().refund(token, amount)
        print("response: {}".format(response))
        return render_template("webpay/plus/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)

@bp.route('/refund-form', methods=["GET"])
def webpay_plus_refund_form():
    return render_template("webpay/plus/refund-form.html")

@bp.route('/status-form', methods=['GET'])
def show_create():
    return render_template('webpay/plus/status-form.html')

@bp.route('/status', methods=['POST'])
def status():
    token_ws = request.form.get('token_ws')
    tx = Transaction()
    resp = tx.status(token_ws)
    return render_template('webpay/plus/status.html', response=resp, token=token_ws, req=request.form)

def create_app(config_class=None):
    app = Flask(__name__, template_folder=TEMPLATE_PATH)
    app.config.from_object(config_class)

    from webpay_plus import bp as webpay_plus_bp
    app.register_blueprint(webpay_plus_bp, url_prefix="/webpay-plus")

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    create_app().run()
