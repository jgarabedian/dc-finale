from flask import Flask, render_template, flash, request, redirect, Response, abort, url_for, session
import functools
from mongo import get_activities, insert_activity, get_completed_activities, del_activity, get_activity, update_activity

# export FLASK_APP=app.py
# export FLASK_ENV=development
ADMIN_PASSWORD = 'secret'
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


@app.route('/')
def index():
    all_activities = get_activities()
    completed_activities = get_completed_activities()
    return render_template('index.html', activities=all_activities, completed_activities=completed_activities)


# login route
@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        # TODO: If using a one-way hash, you would also hash the user-submitted
        # password and do the comparison on the hashed versions.
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html')


@login_required
@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('index'))
    return render_template('logout.html')


@login_required
@app.route('/add', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST' and request.form.get('act_name'):
        form = {
            'act_name': request.form.get('act_name'),
            'act_date': request.form.get('act_date'),
            'act_location': request.form.get('act_location'),
            'act_address': request.form.get('act_address'),
            'act_friends': request.form.get('act_friends'),
            'act_notes': request.form.get('act_notes'),
            'act_category': request.form.get('act_category')
        }
        insert_activity(form)
        flash('Entered a new activity!!')
        return redirect(url_for('index'))
    return render_template('add_activity.html')


@login_required
@app.route('/update/<act_id>', methods=['GET', 'POST'])
def update(act_id):
    if request.method == 'POST':
        form = {
            'act_name': request.form.get('act_name'),
            'act_date': request.form.get('act_date'),
            'act_location': request.form.get('act_location'),
            'act_address': request.form.get('act_address'),
            'act_friends': request.form.get('act_friends'),
            'act_notes': request.form.get('act_notes'),
            'act_category': request.form.get('act_category')
        }
        update_activity(act_id, form)
        return redirect(url_for('index'))
    else:
        activity = get_activity(act_id)
        return render_template('update.html', activity=activity)


@login_required
@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    print(request.form.get('act_id'))
    if request.method == 'POST' and request.form.get('act_id'):
        act_id = request.form.get('act_id')
        del_activity(act_id)
        return redirect(url_for('index'))
    return redirect(url_for('activities'))
