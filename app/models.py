from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    telefono = db.Column(db.String(9), nullable=False)
    nombre_usuario = db.Column(db.String(30), nullable=False)
    clave_usuario = db.Column(db.String(256), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    id_tipo = db.Column(db.Integer, nullable=True)

    def __init__(self, nombre, apellido, dni, telefono, username, password, tipo_usuario):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.nombre_usuario = username
        self.clave_usuario = generate_password_hash(password)
        self.estado = True
        self.id_tipo = tipo_usuario

    def __repr__(self):
        return '<Usuario %r>' % self.nombre_usuario

    def set_clave(self, clave):
        self.clave_usuario = generate_password_hash(clave)

    def set_estado(self, estado):
        self.estado = estado

    def check_clave(self, clave):
        return check_password_hash(self.clave_usuario, clave)

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuarios'
    id_tipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<TipoUsuario %r>' % self.descripcion

class Persona(db.Model):
    __tablename__ = 'personas'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(10), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    telefono = db.Column(db.String(9), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def set_estado(self, estado):
        self.estado = estado


class Autor(db.Model):
    __tablename__ = 'autores'
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def set_estado(self, estado):
        self.estado = estado

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def set_estado(self, estado):
        self.estado = estado


class Editorial(db.Model):
    __tablename__ = 'editoriales'
    id_editorial = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)

    def set_estado(self, estado):
        self.estado = estado


class Libro(db.Model):
    __tablename__ = 'libros'
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    ruta_portada = db.Column(db.String(250), nullable=False)
    nombre_portada = db.Column(db.String(100), nullable=False)
    id_autor = db.Column(db.Integer, nullable=True)
    id_categoria = db.Column(db.Integer, nullable=True)
    id_editorial = db.Column(db.Integer, nullable=True)
    ubicacion = db.Column(db.String(50), nullable=False)
    ejemplar = db.Column(db.Integer, nullable=False)
    estado_libro = db.Column(db.Boolean, nullable=False)
    fecha_creacion = db.Column(db.DateTime)
    isbn = db.Column(db.String(13), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)


class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id_prestamo = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, nullable=True)
    id_persona = db.Column(db.Integer, nullable=True)
    fecha_devolucion = db.Column(db.DateTime, nullable=False)
    fecha_confirmacion = db.Column(db.DateTime, nullable=False)
    estado_entregado = db.Column(db.String(150), nullable=False)
    estado_recibido = db.Column(db.String(150), nullable=False)
    fecha_creacion = db.Column(db.DateTime)
    estado = db.Column(db.Boolean, nullable=False)


    def set_estado(self, estado):
        self.estado = estado

#class Catalogacion(db.Model):
