from flask import Flask, request, flash
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listasuper.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)



class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)
    listo = db.Column(db.Boolean, default=False)

    def __init__(self, content,precio, cantidad):
        self.content = content
        self.precio = precio
        self.cantidad = cantidad
        self.listo = False

db.create_all()


@app.route('/')
def supers_list():
    supers = Super.query.all()
    return render_template('mostrar_todo.html', supers=supers)


@app.route('/super', methods=['POST'])
def add_super():
    content = request.form.get('content')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    if not request.form['content'] or not request.form['precio']:
        flash('Debes ingresar un texto')
        return redirect('/')
    super = Super(content, precio,cantidad)
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

app.static_folder = 'static'

if __name__ == '__main__':
    db.create_all()
    app.run()