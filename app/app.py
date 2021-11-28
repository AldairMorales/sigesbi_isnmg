import os
from flask import render_template, redirect, url_for, flash, session, request
from fpdf import FPDF
from sqlalchemy import func
from config import app, db
from models import Usuario, TipoUsuario, Categoria, Editorial, Autor, Libro, Persona, Prestamo
from forms import LoginForm, RegisterUsuarioForm, RegisterCategoriaForm, RegisterEditorialForm, RegisterAutorForm,\
    RegisterLibroForm, RegisterPersonaForm, RegisterPrestamoForm
from flask_bootstrap import Bootstrap
from datetime import datetime
from functools import wraps

####################
# ERRORHANDLERS
####################

@app.errorhandler(404)
def not_found(error):
    """ Método para error 404. """
    return render_template('errors/error404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    """ Método para error 500. """
    return render_template('errors/error500.html')

####################
# ROUTES
####################

bootstrap = Bootstrap(app)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return test(*args, **kwargs)
        elif 'admin' in session:
            return test(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nombre_usuario = form.usuario.data).first()

        if usuario:
            if usuario.check_clave(form.clave.data):
                if usuario.id_tipo == 1:
                    session['admin'] = form.usuario.data
                    print("se esta ingresando como admin")
                    print(session['admin'])
                    return redirect(url_for('inicio'))
                else:
                    print("se esta ingresando como usuario")
                    session['user'] = form.usuario.data
                    print(session['user'])
                    return redirect(url_for('inicio'))
            else:
                return redirect('/?bc=True')
        else:
            return redirect('/?bc=True')
    return render_template('index.html', form=form, badCredentials=request.args.get('bc', default=False, type=bool))

@app.route('/cerrar-sesion')
def salir():
    print("Cerrando sesion")
    if 'user' in session:
        session.pop('user', None)
        print("elimino user")
    else:
        session.pop('admin', None)
        print("elimino admin")

    session.clear()
    print("Cerrando sesion")
    return redirect(url_for('index'))

@app.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    libros = db.session.query(func.count(Libro.id_libro).label('totalL')).filter_by(estado=True).first().totalL
    personas = db.session.query(func.count(Persona.id_persona).label('totalP')).filter_by(estado=True).first().totalP
    prestamosP = db.session.query(func.count(Prestamo.id_prestamo).label('totalPp')).filter_by(estado=False).first().totalPp
    prestamos = db.session.query(func.count(Prestamo.id_prestamo).label('totalPr')).first().totalPr
    usuarios = db.session.query(func.count(Usuario.id_usuario).label('totalU')).filter_by(estado=True).first().totalU

    return render_template('inicio.html', libros=libros, personas=personas, prestamos=prestamos, prestamosP=prestamosP,
                                   usuarios=usuarios)

@app.route('/registrar/tipo-usuario', methods=['GET', 'POST'])
#@login_required
def registrarTipoUsuario():
    if 'admin' in session:
        return render_template('registrar_tipo_usuario.html')
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/usuario', methods=['GET', 'POST'])
@login_required
def registrarUsuario():
    if 'admin' in session:
        form = RegisterUsuarioForm()

        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(nombre_usuario=form.usuario.data).first()
            if usuario:
                flash("nombre de usuario ya existe", category="warning")
                return render_template('registrar_usuario.html', form=form)
            else:
                try:
                    tipo = form.tipoUsuario.data
                    nombre = form.nombre.data
                    apellido = form.apellido.data
                    dni = form.dni.data
                    telefono = form.telefono.data
                    usuario = form.usuario.data
                    clave = form.clave.data

                    usuarioDB = Usuario(nombre, apellido, dni, telefono, usuario,clave,tipo)
                    db.session.add(usuarioDB)
                    db.session.commit()


                    form.nombre.data = ""
                    form.apellido.data = ""
                    form.dni.data = ""
                    form.telefono.data = ""
                    form.usuario.data = ""
                    form.clave.data = ""
                    flash("Usuario registrado correctamente", category="info")
                    return render_template('registrar_usuario.html', form=form)
                except Exception as e:
                    print(e)
                    flash("Error en registrar usuario", category="error")
                    return render_template('registrar_usuario.html', form=form)

        return render_template('registrar_usuario.html', form=form)
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/categoria', methods=['GET', 'POST'])
@login_required
def registrarCategoria():
    if 'admin' in session:
        form = RegisterCategoriaForm()

        if form.validate_on_submit():
            categoria = Categoria.query.filter_by(descripcion=form.descripcion.data).first()
            if categoria:
                flash("nombre de categoría ya existe", category="warning")
                return render_template('registrar_categoria.html', form=form)
            else:
                descripcion = form.descripcion.data

                try:
                    categoriaDB = Categoria(descripcion=descripcion)
                    db.session.add(categoriaDB)
                    db.session.commit()
                    flash("Categoria registrado correctamente", category="info")
                    form.descripcion.data = ""
                    return render_template('registrar_categoria.html', form=form)
                except Exception as e:
                    print(e)
                    flash("Error en registrar categoria", category="error")
                    return render_template('registrar_categoria.html', form=form)

        return render_template('registrar_categoria.html', form=form)
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/autor', methods=['GET', 'POST'])
@login_required
def registrarAutor():
    if 'admin' in session:
        form = RegisterAutorForm()

        if form.validate_on_submit():
            autor = Autor.query.filter_by(nombre=form.nombre.data).first()
            if autor:
                flash("El Autor ya se encuentra Registrado", category="warning")
                return render_template('registrar_autor.html', form=form)
            else:
                nombre = form.nombre.data
                estado = True
                try:
                    autorDB = Autor(nombre=nombre, estado=estado)
                    db.session.add(autorDB)
                    db.session.commit()
                    flash("Autor registrado correctamente", category="info")
                    form.nombre.data = ""
                    return render_template('registrar_autor.html', form=form)
                except Exception as e:
                    print(e)
                    flash("Error en registrar autor", category="error")
                    return render_template('registrar_autor.html', form=form)

        return render_template('registrar_autor.html', form=form)
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/editorial', methods=['GET', 'POST'])
@login_required
def registrarEditorial():
    if 'admin' in session:
        form = RegisterEditorialForm()

        if form.validate_on_submit():
            editorial = Editorial.query.filter_by(descripcion=form.descripcion.data).first()
            if editorial:
                flash("La editorial ya existe", category="warning")
                return render_template('registrar_editorial.html', form=form)
            else:
                descripcion = form.descripcion.data
                print(descripcion)
                try:
                    editorialDB = Editorial(descripcion=descripcion)
                    db.session.add(editorialDB)
                    db.session.commit()
                    flash("Editorial registrada exitosamente", category="info")
                    form.descripcion.data = ""
                    return render_template('registrar_editorial.html', form=form)
                except Exception as e:
                    print(e)
                    flash("Editorial no registrada ", category="error")
                    return render_template('registrar_editorial.html', form=form)

        return render_template('registrar_editorial.html', form=form)
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/libro', methods=['GET', 'POST'])
@login_required
def registrarLibro():

    form = RegisterLibroForm()
    categorias = db.session.query(Categoria).filter_by(estado=True).all()
    autores = db.session.query(Autor).filter_by(estado=True).all()
    editoriales = db.session.query(Editorial).filter_by(estado=True).all()

    if form.validate_on_submit():
        isbn = form.isbn.data
        libroe = Libro.query.filter_by(isbn=isbn).first()

        if libroe:
            flash("Numero de ejemplar ya existe, porfavor ingrese otro ejemplar.", category="warning")

        else:
            try:
                file_name = form.ruta_portada.data
                fecha = datetime.now()
                tiempo = fecha.strftime("%Y%m%d")
                ruta_portada = tiempo + file_name.filename
                file_name.save("static/uploads/" + ruta_portada)
                titulo = form.tituloLibro.data
                nombre_portada = form.nombre_portada.data
                id_autor = request.form['autor']
                id_categoria = request.form['categoria']
                id_editorial = request.form['editorial']

                ubicacion = form.ubicacion.data
                estado = True
                fecha_creacion = datetime.now()
                ejemplar = form.ejemplar.data
                estado_libro = True

                libroDB = Libro(titulo=titulo, ruta_portada=ruta_portada, nombre_portada=nombre_portada,
                                id_autor=id_autor, id_categoria=id_categoria, id_editorial=id_editorial,
                                ubicacion=ubicacion, ejemplar=ejemplar, estado=estado,
                                fecha_creacion=fecha_creacion, isbn=isbn, estado_libro=estado_libro)
                db.session.add(libroDB)
                db.session.commit()
                flash("Libro registrado correctamente", category="success")
                form.tituloLibro.data = ""
                form.nombre_portada.data = ""
                form.ejemplar.data = ""
                form.ubicacion.data = ""
                form.isbn.data = ""
                return redirect(url_for('registrarLibro'))

            except Exception as e:
                print(e)
                flash("Error en registro de Libro", category="error")
                return redirect(url_for('registrarLibro'))

    return render_template('registrar_libro.html', form=form, categorias=categorias, autores=autores, editoriales=editoriales)

@app.route('/registrar/persona', methods=['GET', 'POST'])
@login_required
def registrarPersona():
    if 'admin' or 'user' in session:
        form = RegisterPersonaForm()

        if form.validate_on_submit():
            persona = Persona.query.filter_by(dni=form.dni.data).first()
            if persona:
                flash("La persona ya existe", category="warning")
                return render_template('registrar_persona.html', form=form)
            else:
                print("Registro de persona")
                try:
                    nombre = form.nombre.data
                    apellido = form.apellido.data
                    correo = form.correo.data
                    codigo = form.codigo.data
                    dni = form.dni.data
                    telefono = form.telefono.data
                    estado = True
                    print(nombre, dni, estado)
                    personaDB = Persona(nombre=nombre, apellido=apellido, correo=correo, codigo=codigo, dni=dni, telefono=telefono, estado=estado)
                    db.session.add(personaDB)
                    db.session.commit()

                    flash("Persona registrada correctamente", category="success")

                    form.nombre.data = ""
                    form.apellido.data = ""
                    form.correo.data = ""
                    form.codigo.data = ""
                    form.dni.data = ""
                    form.telefono.data = ""

                    return render_template('registrar_persona.html', form=form)
                except Exception as e:
                    print(e)
                    flash("Persona no registrada ", category="error")
                    return render_template('registrar_persona.html', form=form)
        return render_template('registrar_persona.html', form=form)
    else:
        return redirect(url_for('inicio'))

@app.route('/registrar/prestamo', methods=['GET', 'POST'])
@login_required
def registrarPrestamo():
    form = RegisterPrestamoForm()
    libros = db.session.query(Libro).filter_by(estado=True).all()
    personas = db.session.query(Persona).filter_by(estado=True).all()

    if form.validate_on_submit():
        id_persona = request.form['idPersona']
        id_libro = request.form['idLibro']
        libro = Libro.query.filter_by(id_libro=id_libro).first()
        print("esta validando")
        if id_persona == "" and id_libro == "":
            flash("Faltan datos, porfavor ingrese los datos faltantes.", category="warning")
            return render_template('registrar_prestamo.html', form=form, libros=libros, personas=personas)
        else:
            try:
                fecha_devolucion = form.fecha_devolucion.data
                fecha_confirmacion = None
                estado_entregado = form.estado_entregado.data
                fecha_creacion = datetime.now()
                estado_recibido = ""
                estado = False

                prestamoDB = Prestamo(id_libro= id_libro, id_persona=id_persona, fecha_devolucion=fecha_devolucion,
                                          fecha_confirmacion=fecha_confirmacion, estado_entregado=estado_entregado,
                                          estado_recibido=estado_recibido, fecha_creacion=fecha_creacion, estado=estado)
                db.session.add(prestamoDB)
                libro.estado = False
                db.session.commit()

                form.fecha_devolucion.data = ""
                form.estado_entregado.data = ""
                flash("Prestamo registrado correctamente", category="success")
                return render_template('registrar_prestamo.html', form=form, libros=libros, personas=personas)
            except Exception as e:
                print(e)
                flash("Prestamo no registrado ", category="error")
                return render_template('registrar_prestamo.html', form=form, libros=libros, personas=personas)

    return render_template('registrar_prestamo.html', form=form, libros=libros, personas=personas)


@app.route('/registro/devolucion/<int:id>')
@login_required
def registroDevolucion(id):
    prestamosp = Prestamo.query.filter_by(id_persona=id, estado=False).all()
    personas = db.session.query(Persona).filter_by(estado=True).all()

    libros = []
    for item in prestamosp:
        titulo_libro = Libro.query.filter_by(id_libro=item.id_libro).first().titulo
        libros.append(titulo_libro)

    prestamos = zip(prestamosp, libros)

    return render_template('registrar_devolucion.html', prestamos=prestamos, personas=personas)

@app.route('/registrar/devolucion',methods=['GET', 'POST'])
@login_required
def registrarDevolucion():

    personas = db.session.query(Persona).filter_by(estado=True).all()

    if request.method == 'POST':
        id_prestamo = request.form['ideprestamo']
        estadoR = request.form['estadoRecibido']

        if estadoR == "":
            estadoR = "El estado del libro se recepcionó conforme al estado entregado."

        prestamo = Prestamo.query.filter_by(id_prestamo=id_prestamo).first()
        libro = Libro.query.filter_by(id_libro=prestamo.id_libro).first()
        prestamo.estado_recibido = estadoR
        prestamo.fecha_confirmacion = datetime.now()
        prestamo.estado = True
        libro.estado = True
        db.session.commit()
        flash("Devolucion registrada!", category="info")

    return render_template('registrar_devolucion.html', personas=personas)

####################
# ROUTES CONSULTAS
####################

@app.route('/consultar/autor', methods=['GET', 'POST'])
@login_required
def consultarAutor():
    if 'admin' in session:
        autores = db.session.query(Autor).all()
        return render_template('consultar_autor.html', autores=autores)
    else:
        return redirect(url_for('inicio'))

@app.route('/consultar/categoria', methods=['GET', 'POST'])
@login_required
def consultarCategoria():
    if 'admin' in session:
        categorias = db.session.query(Categoria).all()
        return render_template('consultar_categoria.html', categorias=categorias)
    else:
        flash("Usted no puede acceder como bibliotecario a esta zona", category="warning")
        return redirect(url_for('inicio'))

@app.route('/consultar/editorial', methods=['GET', 'POST'])
@login_required
def consultarEditorial():
    if 'admin' in session:
        editoriales = db.session.query(Editorial).all()
        return render_template('consultar_editorial.html', editoriales=editoriales)
    else:
        return redirect(url_for('inicio'))

@app.route('/consultar/libro', methods=['GET', 'POST'])
@login_required
def consultarLibro():
    librosA = db.session.query(Libro).all()
    categorias = []
    autores = []

    for item in librosA:
        categoria = Categoria.query.filter_by(id_categoria=item.id_categoria).first().descripcion
        autor = Autor.query.filter_by(id_autor=item.id_autor).first().nombre

        categorias.append(categoria)
        autores.append(autor)

    libros = zip(librosA, autores, categorias)
    print(categorias, autores)

    return render_template('consultar_libro.html', libros=libros)

@app.route('/consultar/persona', methods=['GET', 'POST'])
@login_required
def consultarPersona():
    personas = db.session.query(Persona).all()
    return render_template('consultar_persona.html', personas=personas)

@app.route('/consultar/usuario', methods=['GET', 'POST'])
@login_required
def consultarUsuario():
    if 'admin' in session:
        usuarios = db.session.query(Usuario).all()
        return render_template('consultar_usuario.html', usuarios=usuarios)
    else:
        return redirect(url_for('inicio'))

@app.route('/consultar/tipoUsuario', methods=['GET', 'POST'])
@login_required
def consultarTipoUsuario():
    if 'admin' in session:
        tiposUsuario = db.session.query(TipoUsuario).all()
        return render_template('consultar_tipoUsuario.html', tiposUsuario=tiposUsuario)
    else:
        return redirect(url_for('inicio'))


@app.route('/consultar/prestamo', methods=['GET', 'POST'])
@login_required
def consultarPrestamo():
    prestamos = db.session.query(Prestamo).all()

    personas = []
    libros = []
    for item in prestamos:
        titulo_libro = Libro.query.filter_by(id_libro=item.id_libro).first().titulo
        dni = Persona.query.filter_by(id_persona=item.id_persona).first().dni
        libros.append(titulo_libro)
        personas.append(dni)

    prestamos = zip(prestamos, libros, personas)
    return render_template('consultar_prestamo.html', prestamos=prestamos)

####################
# ROUTES EDITAR
####################
@app.route('/update/autor',methods=['GET','POST'])
@login_required
def updateAutor():
    if 'admin' in session:
        id_autor = request.form['identificador']
        nombre = request.form['nombre']

        autor = Autor.query.filter_by(id_autor=id_autor).first()
        autor.nombre = nombre
        db.session.commit()

        return redirect(url_for('consultarAutor'))
    else:
        return redirect(url_for('inicio'))

@app.route('/update/categoria',methods=['GET','POST'])
@login_required
def updateCategoria():
    if 'admin' in session:
        id_categoria = request.form['identificador']
        descripcion = request.form['descripcion']

        categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
        categoria.descripcion = descripcion
        db.session.commit()

        return redirect(url_for('consultarCategoria'))
    else:
        return redirect(url_for('inicio'))

@app.route('/update/editorial',methods=['GET','POST'])
@login_required
def updateEditorial():
    if 'admin' in session:
        id_editorial = request.form['identificador']
        descripcion = request.form['descripcion']

        editorial = Editorial.query.filter_by(id_editorial=id_editorial).first()
        editorial.descripcion = descripcion

        db.session.commit()
        return redirect(url_for('consultarEditorial'))
    else:
        return redirect(url_for('inicio'))

@app.route('/update/persona',methods=['GET','POST'])
@login_required
def updatePersona():
    if 'admin' in session:
        id_persona = request.form['identificador']
        persona = Persona.query.filter_by(id_persona=id_persona).first()

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        codigo = request.form['codigo']
        telefono = request.form['telefono']

        persona.nombre = nombre
        persona.apellido = apellido
        persona.correo = correo
        persona.codigo = codigo
        persona.telefono = telefono

        db.session.commit()
        return redirect(url_for('consultarPersona'))
    else:
        return redirect(url_for('inicio'))

@app.route('/update/usuario',methods=['GET','POST'])
@login_required
def updateUsuario():
    if 'admin' in session:
        id_usuario = request.form['identificador']
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        claveUsuario = request.form['clave']
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.telefono = telefono

        if claveUsuario != "":
            usuario.set_clave(claveUsuario)

        db.session.commit()
        return redirect(url_for('consultarUsuario'))
    else:
        return redirect(url_for('inicio'))

@app.route('/editar/libro/<int:id>')
@login_required
def editarLibro(id):
    if 'admin' in session:
        libro = Libro.query.filter_by(id_libro=id).first()
        categorias = db.session.query(Categoria).filter_by(estado=True).all()
        autores = db.session.query(Autor).filter_by(estado=True).all()
        editoriales = db.session.query(Editorial).filter_by(estado=True).all()
        return render_template('modificar_libro.html', libro=libro, autores=autores, categorias=categorias, editoriales=editoriales)
    else:
        return redirect(url_for('inicio'))

@app.route('/update/libro', methods=['GET','POST'])
@login_required
def updateLibro():
    if 'admin' in session:
        id_libro = request.form['identificador']
        libro = Libro.query.filter_by(id_libro=id_libro).first()

        tituloLibro = request.form['tituloLibro']
        if request.files['ruta_portada'].filename != "":
            file = request.files['ruta_portada']
            fecha = datetime.now()
            tiempo = fecha.strftime("%Y%m%d")
            ruta_portada = tiempo + file.filename
            file.save("static/uploads/" + ruta_portada)
        else:
            ruta_portada = libro.ruta_portada

        nombre_portada = request.form['nombre_portada']
        ubicacion = request.form['ubicacion']
        ejemplar = request.form['ejemplar']
        autor = request.form['autor']
        categoria = request.form['categoria']
        editorial = request.form['editorial']

        libro.titulo = tituloLibro
        libro.ruta_portada = ruta_portada
        libro.nombre_portada = nombre_portada
        libro.ubicacion = ubicacion
        libro.ejemplar = ejemplar
        libro.id_autor = autor
        libro.id_categoria = categoria
        libro.id_editorial = editorial

        db.session.commit()
        return redirect(url_for('consultarLibro'))
    else:
        return redirect(url_for('inicio'))


####################
# ROUTES DELETES
####################

@app.route('/delete/autor/<int:id>')
@login_required
def eliminarAutor(id):
    if 'admin' in session:
        autor = Autor.query.filter_by(id_autor=id).first()
        autor.set_estado(False)
        db.session.commit()
        flash("Autor eliminado correctamente", category="delete")
        return redirect(url_for('consultarAutor'))
    else:
        return redirect(url_for('inicio'))

@app.route('/delete/categoria/<int:id>')
@login_required
def eliminarCategoria(id):
    if 'admin' in session:
        categoria = Categoria.query.filter_by(id_categoria=id).first()
        categoria.set_estado(False)
        db.session.commit()

        flash("Categoria eliminada correctamente", category="delete")
        return redirect(url_for('consultarCategoria'))
    else:
        return redirect(url_for('inicio'))

@app.route('/delete/editorial/<int:id>')
@login_required
def eliminarEditorial(id):
    if 'admin' in session:
        editorial = Editorial.query.filter_by(id_editorial=id).first()
        editorial.set_estado(False)
        db.session.commit()

        flash("Editorial eliminada correctamente", category="delete")
        return redirect(url_for('consultarEditorial'))
    else:
        return redirect(url_for('inicio'))

@app.route('/delete/persona/<int:id>')
@login_required
def eliminarPersona(id):
    if 'admin' in session:
        persona = Persona.query.filter_by(id_persona=id).first()
        persona.set_estado(False)
        db.session.commit()
        return redirect(url_for('consultarPersona'))
    else:
        return redirect(url_for('inicio'))

@app.route('/delete/usuario/<int:id>')
@login_required
def eliminarUsuario(id):
    if 'admin' in session:
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        usuario.estado = False
        db.session.commit()
        return redirect(url_for('consultarUsuario'))
    else:
        return redirect(url_for('inicio'))

@app.route('/delete/libro/<int:id>')
@login_required
def eliminarLibro(id):
    if 'admin' in session:
        libro = Libro.query.filter_by(id_libro=id).first()
        libro.estado_libro = False
        libro.estado = False
        db.session.commit()

        return redirect(url_for('consultarLibro'))
    else:
        return redirect(url_for('inicio'))

#####################
# ROUTES ACTIVACIONES
####################

@app.route('/activar/autor/<int:id>')
@login_required
def activarAutor(id):
    if 'admin' in session:
        autor = Autor.query.filter_by(id_autor=id).first()
        autor.set_estado(True)
        db.session.commit()
        flash("Autor activado correctamente", category="info")
        return redirect(url_for('consultarAutor'))
    else:
        return redirect(url_for('inicio'))

@app.route('/activar/categoria/<int:id>')
@login_required
def activarCategoria(id):
    if 'admin' in session:
        categoria = Categoria.query.filter_by(id_categoria=id).first()
        categoria.set_estado(True)
        db.session.commit()

        flash("Categoria activado correctamente", category="info")
        return redirect(url_for('consultarCategoria'))
    else:
        return redirect(url_for('inicio'))

@app.route('/activar/editorial/<int:id>')
@login_required
def activarEditorial(id):
    if 'admin' in session:
        editorial = Editorial.query.filter_by(id_editorial=id).first()
        editorial.set_estado(True)
        db.session.commit()

        flash("Editorial activado correctamente", category="info")
        return redirect(url_for('consultarEditorial'))
    else:
        return redirect(url_for('inicio'))

@app.route('/activar/persona/<int:id>')
@login_required
def activarPersona(id):
    if 'admin' in session:
        persona = Persona.query.filter_by(id_persona=id).first()
        persona.set_estado(True)
        db.session.commit()

        flash("Persona activada correctamente", category="info")
        return redirect(url_for('consultarPersona'))
    else:
        return redirect(url_for('inicio'))

@app.route('/activar/usuario/<int:id>')
@login_required
def activarUsuario(id):
    if 'admin' in session:
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        usuario.set_estado(True)
        db.session.commit()
        flash("Usuario activado correctamente", category="info")
        return redirect(url_for('consultarUsuario'))
    else:
        return redirect(url_for('inicio'))

@app.route('/activar/libro/<int:id>')
@login_required
def activarLibro(id):
    if 'admin' in session:
        libro = Libro.query.filter_by(id_libro=id).first()
        libro.estado_libro = True
        db.session.commit()
        flash("Libro activado correctamente", category="info")
        return redirect(url_for('consultarLibro'))
    else:
        return redirect(url_for('inicio'))

####################
# ROUTES REPORTES
####################
@app.route('/reporte/prestamo', methods=['GET','POST'] )
@login_required
def reportePrestamo():
    if 'admin' in session:
        prestamos = db.session.query(Prestamo).all()
        personas = []
        libros = []
        ejemplares = []
        for item in prestamos:
            titulo_libro = Libro.query.filter_by(id_libro=item.id_libro).first().titulo
            ejemplar = Libro.query.filter_by(id_libro=item.id_libro).first().ejemplar
            dni = Persona.query.filter_by(id_persona=item.id_persona).first().dni
            libros.append(titulo_libro)
            ejemplares.append(ejemplar)
            personas.append(dni)

        prestamosR = zip(prestamos, libros, personas, ejemplares)

        if request.method == 'POST':
            fechaInicio = request.form['fechaInicio']
            fechaFin = request.form['fechaFin']

            if fechaInicio and fechaFin:
                try:

                    title = 'Reporte de Prestamos'

                    class PDF(FPDF):

                        def header(self):
                            self.set_font('Arial', 'B', 18)
                            self.set_text_color(50)
                            self.image('static/ico/prestamo.png', 10, 10, 20, 20, 'PNG')
                            self.ln(10)
                            self.cell(0, 0, title, 0, 0, 'C')
                            self.ln(8)
                            self.set_font('Arial', '', 12)
                            self.cell(0, 0, 'Fecha: ' + datetime.now().strftime('%d-%m-%Y'), 0, 0, 'R')
                            self.ln(8)
                            self.set_font('Courier', '', 12)
                            self.set_x(25)

                        def footer(self):
                            self.set_y(-15)
                            self.set_font('Arial', 'I', 9)
                            self.set_text_color(0)
                            self.ln()
                            self.cell(0, 0, 'Pagina ' + str(self.page_no()), 0, 0, 'C')

                        def thead(self):
                            self.set_font('Courier', 'B', 11)
                            self.set_draw_color(150)
                            self.set_x(25)
                            self.cell(25, 10, 'Estado', 'TB', 0, 'C')
                            self.cell(25, 10, 'DNI', 'TB', 0, 'C')
                            self.cell(25, 10, 'ISBN', 'TB', 0, 'C')
                            self.cell(110, 10, 'Libro', 'TB', 0, 'C')
                            self.cell(10, 10, 'Ejemplar', 'TB', 0, 'C')
                            self.cell(30, 10, 'Prestamo', 'TB', 0, 'C')
                            self.cell(30, 10, 'Devolucion', 'TB', 0, 'C')
                            self.ln(15)


                        def tbody(self):
                            self.set_font('Courier', '', 11)
                            self.set_draw_color(200)
                            items = db.session.query(Prestamo).filter(Prestamo.fecha_creacion.between(fechaInicio, fechaFin))

                            for item in items:
                                self.set_x(25)
                                if item.estado:
                                    self.cell(25, 6, 'Registrado', 'B', 0, 'C')
                                else:
                                    self.cell(25, 6, 'Pendiente', 'B', 0, 'C')
                                self.cell(27, 6, str(Persona.query.filter_by(id_persona=item.id_persona).first().dni), 'B', 0,
                                          'C')
                                self.cell(28, 6, str(Libro.query.filter_by(id_libro=item.id_libro).first().isbn), 'B',
                                          0, 'C')
                                self.cell(110, 6, str(Libro.query.filter_by(id_libro=item.id_libro).first().titulo), 'B',
                                          0, 'C')
                                self.cell(10, 6, str(Libro.query.filter_by(id_libro=item.id_libro).first().ejemplar), 'B',
                                          0, 'C')
                                self.cell(30, 6, str(item.fecha_creacion), 'B', 0, 'C')
                                self.cell(30, 6, str(item.fecha_confirmacion), 'B', 0, 'C')
                                self.ln(15)

                        def print(self):
                            self.add_page()
                            self.thead()
                            self.tbody()

                    pdf = PDF('L', 'mm', 'A4')
                    pdf.set_title(title)
                    pdf.set_author('SIGESBI')
                    pdf.print()
                    pdf.output('reporte_prestamos.pdf', 'F')
                    os.startfile('reporte_prestamos.pdf')

                except Exception as e:
                    print(e)
                    flash("Tiene un reporte_prestamo.pdf abierto, !porfavor cerrarlo!", category="error")
                    return redirect(url_for('reportePrestamo'))

            else:
                flash("Porfavor ingrese las fechas.", category="warning")

        return render_template('reporte_prestamo.html', prestamos=prestamosR)
    else:
        return redirect(url_for('inicio'))


@app.route('/reporte/usuarios', methods=['GET','POST'])
@login_required
def reporteUsuarios():
    if 'admin' in session:
        try:
            title = 'Reporte de Usuarios'

            class PDF(FPDF):

                def header(self):
                    self.set_font('Arial', 'B', 18)
                    self.set_text_color(50)
                    self.image('static/ico/usuario.png', 10, 10, 20, 20, 'PNG')
                    self.ln(10)
                    self.cell(0, 0, title, 0, 0, 'C')
                    self.ln(8)
                    self.set_font('Arial', '', 12)
                    self.cell(0, 0, 'Fecha: ' + datetime.now().strftime('%d-%m-%Y'), 0, 0, 'R')
                    self.ln(8)
                    self.set_font('Courier', '', 12)
                    self.set_x(25)

                def footer(self):
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 9)
                    self.set_text_color(0)
                    self.ln()
                    self.cell(0, 0, 'Pagina ' + str(self.page_no()), 0, 0, 'C')

                def thead(self):
                    self.set_font('Courier', 'B', 11)
                    self.set_draw_color(150)
                    self.set_x(25)
                    self.cell(20, 10, 'Estado', 'TB', 0, 'C')
                    self.cell(40, 10, 'Usuario', 'TB', 0, 'C')
                    self.cell(25, 10, 'Tipo Usuario', 'TB', 0, 'C')
                    self.cell(25, 10, 'DNI', 'TB', 0, 'C')
                    self.cell(45, 10, 'Nombre', 'TB', 0, 'C')
                    self.cell(80, 10, 'Apellido', 'TB', 0, 'C')
                    self.cell(30, 10, 'Telefono', 'TB', 0, 'C')
                    self.ln(15)

                def tbody(self):
                    self.set_font('Courier', '', 11)
                    self.set_draw_color(200)
                    items = db.session.query(Usuario).all()

                    for item in items:
                        self.set_x(25)
                        if item.estado:
                            self.cell(20, 6, 'Activo', 'B', 0, 'C')
                        else:
                            self.cell(20, 6, 'de baja', 'B', 0, 'C')

                        self.cell(40, 6, str(item.nombre_usuario), 'B', 0,
                                  'C')
                        if item.id_tipo == 1:
                            self.cell(25, 6, 'Administrador', 'B', 0, 'C')
                        else:
                            self.cell(25, 6, 'Bibliotecario', 'B', 0, 'C')

                        self.cell(30, 6, str(item.dni), 'B',
                                  0, 'C')
                        self.cell(40, 6, str(item.nombre), 'B',
                                  0, 'C')
                        self.cell(80, 6, str(item.apellido), 'B',
                                  0, 'C')
                        self.cell(25, 6, str(item.telefono), 'B', 0, 'C')
                        self.ln(15)

                def print(self):
                    self.add_page()
                    self.thead()
                    self.tbody()

            pdf = PDF('L', 'mm', 'A4')
            pdf.set_title(title)
            pdf.set_author('SIGESBI')
            pdf.print()
            pdf.output('reporte_usuarios.pdf', 'F')
            os.startfile('reporte_usuarios.pdf')
            return redirect(url_for('consultarUsuario'))
        except Exception as e:
            print(e)
            flash("Tiene un reporte_usuario.pdf abierto, !porfavor cerrarlo!", category="error")
            return redirect(url_for('consultarUsuario'))
    else:
        return redirect(url_for('inicio'))


####################
# MAIN APP
####################

if __name__ == '__main__':
    app.run(debug=True)
