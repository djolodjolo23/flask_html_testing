from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 slashes is relative path, 4 slashes is absolute path
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) # 200 is max length
    completed = db.Column(db.Integer, default=0) # default is 0, not completed
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # default is current time
    def __repr__(self):
        return '<Task %r>' % self.id # returns task and id number

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # content is the name of the input field
        new_task = Todo(content=task_content) # create new task

        try:
            db.session.add(new_task) # add new task to db
            db.session.commit() # commit changes
            return redirect('/') # redirect to homepage
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # get all tasks from db
        return render_template('index.html', tasks=tasks) # pass tasks to index.html

    

if __name__ == "__main__":
    app.run(debug=True)