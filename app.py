from flask import Flask, render_template, request, redirect, url_for #html file display krne k lie render temp
from flask_sqlalchemy import SQLAlchemy #database
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime #to have date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #databse to store task
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#databse schema for our db in python class
class Todo(db.Model):#inherits db.model for schema
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.today())

    def __repr__(self): #jab object print hoga class ka toh kya dikhna chahiye this shows
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET', 'POST']) #app ko bola h ki vo /end point pr kya show krega
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        todo = Todo(title = title) #Todo class instance
        try:
            db.session.add(todo) #adding task thru instance
            db.session.commit()#changes saved in database

        except:
            return 'There was an error'    
    
    allTodo = Todo.query.all() #to show all records
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods = ['GET', 'POST']) #app ko bola h ki vo /end point pr kya show krega
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating ur task'    
    else:
        return render_template('update.html', todo=todo)
 

@app.route('/delete/<int:sno>') #app ko bola h ki vo /end point pr kya show krega
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)#delete task
    db.session.commit()#save changes
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True) #to check whats wrong