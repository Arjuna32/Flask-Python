from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from converters import kg_to_lbs, lbs_to_kg

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class ConverterData:
    def __init__(self, kg , lb):
     self.kg = kg
     self.lb = lb
      



@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')
        


@app.route('/task_master', methods = ['POST', 'GET'])
def task_master():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/task_master')
            
        except:
            return 'There was an issue adding your task'
 
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('task_index.html', tasks = tasks)
  
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/task_master')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method =='POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/task_master')
        except:
            return 'There was an issue updating your task'
            
    else:
        return render_template('update.html', task = task)


@app.route('/weight_converter', methods = ['POST', 'GET'])
def weight_converter():
    if request.method == 'POST':
        kg_content = request.form['kg_content']
        lb_content = request.form['lb_content']
        if len(kg_content) > 0:
            lb_content = kg_to_lbs(float(kg_content))
        elif len(lb_content) > 0:
            kg_content = lbs_to_kg(float(lb_content))
        else:
            print("Nothing entered")
       
        cData = ConverterData(kg_content, lb_content)
        print(lb_content)
        print(kg_content)
        return  render_template('converter_index.html', cData=cData)
    else: 
        cData = ConverterData(0,0)
        return render_template('converter_index.html', cData = cData)

if __name__ == "__main__":
    app.run(debug=True)