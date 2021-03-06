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
def showall():
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
    sno = request.args.get('sno')
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('edit.html', todo=todo)




@app.route('/delete', methods= ['GET', 'POST'])
def delete():
    sno = request.args.get('sno')
    if request.method == 'GET':
        todo = Todo.query.filter_by(sno = sno).first()
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)