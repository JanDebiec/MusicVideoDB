from flask import Blueprint, render_template, flash, redirect, url_for

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET', 'POST'])
@mod_main.route('/index', methods=['GET', 'POST'])
def index():
    messageText = ''

    return render_template('index.html',
                           message=messageText,
                           title='Home')

