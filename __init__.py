from flask import Flask, flash, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listasuper.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)
class listasuper(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    supermercado = db.Column(db.String(50))
    producto= db.Column(db.String(200))
    pin = db.Column(db.String(10))
    def __init__(self, nombre, supermercado, producto, pin):
        self.nombre = nombre
        self.supermercado = supermercado
        self.producto = producto
        self.pin = pin

@app.route('/')
def mostrar_todo():
    return render_template('mostrar_todo.html', listasuper=listasuper.query.all())

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['supermercado'] or not request.form['producto']:
            flash('Por favor introduzca todos los campos', 'error')
        else:
            productos = listasuper(request.form['nombre'],
                                     request.form['supermercado'],
                                     request.form['producto'],
                                     request.form['pin'])
            db.session.add(productos)
            db.session.commit()
            flash('Registro guardado con exito!')
            return redirect(url_for('mostrar_todo'))
    return render_template('nuevo.html')

if __name__ == '__main__':
    db.create_all()
    app.run()