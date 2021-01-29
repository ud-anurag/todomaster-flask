from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(120),nullable=False)
    date_created=db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

@app.route('/',methods=['GET','POST'])
def index():
    if (request.method == "POST"):
        content_cont=request.form.get("content")
        new_task=Todo(content=content_cont)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        posts=Todo.query.all()
        return render_template("index.html",posts=posts)

@app.route('/delete/<int:Id>')
def delete(Id):
    task=Todo.query.filter_by(Id=Id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:Id>',methods=['GET','POST'])
def update(Id):
    if(request.method=='POST'):
        new_content=request.form['content']
        tasks=Todo.query.filter_by(Id=Id).first()
        tasks.content=new_content
        db.session.commit()
        return redirect('/')

    else:
        tasks=Todo.query.filter_by(Id=Id).first()
        return render_template('update.html',tasks=tasks)

if (__name__ == '__main__'):
    app.run(debug=True)