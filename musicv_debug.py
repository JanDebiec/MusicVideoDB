#!flask/bin/python
from app import create_app, db
from app.mod_db.models import  Performer, Show

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db , 'Show':Show, 'Performer':Performer}

app.run(debug=True)
