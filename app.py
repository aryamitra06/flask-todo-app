from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    
@app.route("/", methods= ['GET', 'POST'])
def root():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title= title, desc= desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)


@app.route("/edit", methods= ['GET', 'POST'])
def edit():
    if request.method == 'GET':
        sno = request.args.get('sno')
        todo = Todo.query.filter_by(sno = sno).first()
    allTodo = Todo.query.all()
    return render_template('index.html', todo = todo)


@app.route("/delete", methods= ['GET', 'POST'])
def delete():
    if request.method == 'GET':
        sno = request.args.get('sno')
        todo = Todo.query.filter_by(sno = sno).first()
        db.session.delete(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)