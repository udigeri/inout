import argparse
from app import App, Web
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify

web = Web()
flsk = web.flsk

@flsk.teardown_appcontext
def close(error):
    pass

@flsk.route('/')
def index():
    entries = [{"id":1, "title":"Initial message", "text":"Very nice app"}]
    return render_template('index.html', entries=entries)

@flsk.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != flsk.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != flsk.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@flsk.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@flsk.route('/ZA864KL')
def ZA864KL():
    flash('ZA864KL')
    flash('Parking fee 3,50 EUR')
    return redirect(url_for('index'))

@flsk.route('/BL235PP')
def BL235PP():
    flash('BL235PP')
    flash('Parking fee 1,00 EUR')
    return redirect(url_for('index'))

@flsk.route('/BY698LT')
def BY698LT():
    flash('BY698LT')
    flash('You can leave in 10 minutes')
    return redirect("https:\\www.google.com")

@flsk.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    flash('New entry was successfully posted')
    return redirect(url_for('index'))
        
@flsk.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    result = {'status': 0, 'message': 'Error'}
    try:
        result = {'status': 1, 'message': "Post Deleted"}
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)




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

    app = App(__version__, parser.parse_args())
    app.run(web)
    app.finished()
    