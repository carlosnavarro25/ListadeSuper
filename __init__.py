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

# class User(db.Model):
#     email = db.Column(db.String(10), primary_key=True, unique=True)
#     password = db.Column(db.String(6))
#     def __init__(self, email, password):
#         self.email = email
#         self.password = password
#     def __repr__(self):
#         return '<User %r>' % self.email

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    precio = db.Column(db.Float)
    listo = db.Column(db.Boolean, default=False)

    def __init__(self, content,precio):
        self.content = content
        self.precio = precio
        self.listo = False

    #def __repr__(self):
    #    return '<Content %s>' % self.content
    # def __repr__(self):
    #      return '<Precio %s>' % self.precio

db.create_all()

@app.route('/')
def mostrar_todo():
    supers = Super.query.all()
    return render_template('mostrar_todo.html', listasuper=listasuper.query.all(), supers=supers)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('mostrar_todo'))
#     return render_template('login.html', error=error)



# @app.route('/super', methods=['POST'])
# def add_super():
#     content = request.form['content']
#     precio = request.form['precio']
#     if not request.form['content'] or not request.form['precio']:
#         flash('Debes ingresar un texto')
#         return redirect('/')
#     super = Super(content)
#     #super = Super(precio)
#     db.session.add(super)
#     db.session.commit()
#     flash('Registro guardado con exito!')
#     return redirect('/')

@app.route('/super', methods=['POST'])
def add_super():
    content = request.form.get('content')
    precio = request.form.get('precio')
    if precio is None or content is None:
        flash('Debes ingresar un texto')
        return redirect('/')
    super = Super(content, precio)
    db.session.add(super)
    db.session.commit()
    flash('Registro guardado con exito!')
    return redirect('/')


@app.route('/delete/<int:super_id>')
def delete_super(super_id):
    super = Super.query.get(super_id)
    if not super:

        return redirect('/')

    db.session.delete(super)
    db.session.commit()
    flash('Se borro con exito!')
    return redirect('/')


@app.route('/listo/<int:super_id>')
def resolve_super(super_id):
    super = Super.query.get(super_id)

    if not super:
        return redirect('/')
    if super.listo:
        super.listo = False
    else:
        super.listo = True

    db.session.commit()
    return redirect('/')


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