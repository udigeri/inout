import argparse
from app import App, Web
from flask import Flask, request, session, redirect, url_for, \
                  abort, render_template, flash
import json
import os

web = Web()
flsk = web.flsk


@flsk.teardown_appcontext
def close(error):
    pass

@flsk.route('/')
def index():
    env = os.environ.get('HOSTNAME')
    #flash(f'Hostname {env}', category='success')

    if session.get('logged_in'):
        entries = [{"id":1, "title":"Choose your car", "text":"You will see if you need to pay"}]
    else:
        entries = [{"id":2, "title":"Container", "text":f"{env}"}]
    return render_template('index.html', entries=entries)

@flsk.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            rsp = web.getAuthentication(username, password)
            if rsp:
                error = rsp
            else:
                session['logged_in'] = True
                flash('You were logged in', category='success')
                return redirect(url_for('index'))
        else:
            error = "Missing credentials"

    return render_template('login.html', error=error)

@flsk.route('/logout')
def logout():
    if not session.get('logged_in'):
        abort(401)
    session.pop('logged_in', None)
    flash('You were logged out', category='success')
    return redirect(url_for('index'))

@flsk.route('/trx')
def trx():
    if not session.get('logged_in'):
        abort(401)
    return render_template('trx.html')

@flsk.route('/approved')
def approved():
    if not session.get('logged_in'):
        abort(401)
    flash('Approved', category='success')
    return redirect(url_for('trx'))

@flsk.route('/declined')
def declined():
    if not session.get('logged_in'):
        abort(401)
    flash('Declined', category='error')
    return redirect(url_for('trx'))



@flsk.route('/cart', methods=['GET', 'POST'])
def cart():
    if not session.get('logged_in'):
        abort(401)
    flash('Payment method(s)', category='success')
    return redirect(url_for('index'))

@flsk.route('/pay', methods=['GET', 'POST'])
def pay():
    if not session.get('logged_in'):
        abort(401)
    shopping_cart = None
    resp = web.get_cart(request.form['pp'], request.form['lpn'], request.form['amount'])
    data = json.loads(resp.text)
    for key in data:
        if key == 'cartId':
            shopping_cart = data['cartId']
        elif key == 'code':
            code = data['code']
        elif key == 'status':
            status = data['status']
 
    if resp.status_code == 200:
        for key in data:
            if key == 'cartId':
                shopping_cart = data['cartId']
                flash(f'Shopping cart: {shopping_cart}', category='success')
        resp = web.get_pay_methods(shopping_cart)
        data = json.loads(resp.text)
        method = [y[z] for x in data for y in data[x] for z in y if x=='offeredPaymentTypes' if z=='name']
        urls = [y[z] for x in data for y in data[x] for z in y if x=='offeredPaymentTypes' if z=='formUrl']
    else:
        method=[]
        urls=[]
        flash(f'Generate shopping cart failed - {status} {code}', category='error')

    return render_template('cart.html', shopping_cart=shopping_cart, len=len(method), method=method, urls=urls)


@flsk.route('/ParkPlace_1')
def ParkPlace_1():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_1", "lpn":"ZA 864KL", "amount":"250", "display_amount":"2,50"}
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_2')
def ParkPlace_2():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_2", "lpn":"BL 235PP", "amount":"1400", "display_amount":"14,00"}
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_3')
def ParkPlace_3():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_3", "lpn":"BY 698LT", "amount":"0", "display_amount":"0,00"}
    flash('BY 698LT - You can leave in 10 minutes')
    return redirect(url_for('index'))

@flsk.route('/ParkPlace_4')
def ParkPlace_4():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_4", "lpn":"FREE", "amount":"50", "display_amount":"0,80"}
    flash('You can Reserve parking place for next 2 hour')
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_5')
def ParkPlace_5():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_5", "lpn":"MG TW777", "amount":"840", "display_amount":"8,40"}
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_6')
def ParkPlace_6():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_6", "lpn":"3 SAM 123", "amount":"4200", "display_amount":"42,00"}
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_7')
def ParkPlace_7():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_7", "lpn":"FREE", "amount":"50", "display_amount":"0,50"}
    flash('You can Reserve parking place for next 1 hour')
    return render_template('pay.html', customer=customer)

@flsk.route('/ParkPlace_8')
def ParkPlace_8():
    if not session.get('logged_in'):
        abort(401)
    customer = {"id":"ParkPlace_8", "lpn":"KY 68 WZM", "amount":"11680", "display_amount":"116,80"}
    return render_template('pay.html', customer=customer)



if __name__ == "__main__":
    __version_info__ = ('0','1','0')
    __version__ = '.'.join(__version_info__)

    parser = argparse.ArgumentParser(prog="InOut",
                                        description='InOut Parking lot web',
                                        epilog='Pavol Hudák')
    parser.add_argument('-v', '--version', action='version',
                                version='%(prog)s ('+__version__+')')
    parser.add_argument('-c', '--config', dest='config_file_path',
                                action='store',
                                default="./app/config.yml",
                                help='Path to config file (default: %(default)s)')
    parser.add_argument('-e', '--env', dest='inout_env',
                                action='store',
                                default="production",
                                help='Define execution environment (default: %(default)s)')
    parser.add_argument('-p', '--port', dest='web_port',
                                action='store',
                                default="1202",
                                help='Define web server port (default: %(default)s)')

    app = App(__version__, parser.parse_args())
    app.run(web)
    app.finished()
    