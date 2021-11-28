from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, ValidationError, Required, DataRequired

from models import Usuario


class RegisterUsuarioForm(FlaskForm):

    tipoUsuario = SelectField("Tipo Usuario", choices=[("2", "Bibliotecario"), ("1", "Administrador")])
    nombre = StringField(validators=[InputRequired(), Length(
        min=2, max=50)], render_kw={"placeholder": "Nombre"})
    apellido = StringField(validators=[InputRequired(), Length(
        min=4, max=100)], render_kw={"placeholder": "Apellidos"})
    dni = StringField(validators=[InputRequired(), Length(
        min=8, max=10)], render_kw={"placeholder": "DNI"})
    telefono = StringField(validators=[InputRequired(), Length(
        min=8, max=9)], render_kw={"placeholder": "Telefono"})
    usuario = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Nombre de Usuario"})
    clave = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Clave"})

    submit = SubmitField("Registrar Usuario")

class LoginForm(FlaskForm):
    usuario = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Nombre de Usuario"})
    clave = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Clave"})

    submit = SubmitField("Iniciar sesion")

class RegisterCategoriaForm(FlaskForm):
    descripcion = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Nombre de Categoria"})
    submit = SubmitField("Registrar Categoria")

class RegisterAutorForm(FlaskForm):
    nombre = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Nombre de Autor"})
    submit = SubmitField("Registrar Autor")

class RegisterEditorialForm(FlaskForm):
    descripcion = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Nombre de Editorial"})
    submit = SubmitField("Registrar Editorial")

class RegisterLibroForm(FlaskForm):

    tituloLibro = StringField(validators=[InputRequired(), Length(
        min=2, max=50)], render_kw={"placeholder": "Nombre de Libro"})

    ruta_portada = FileField(validators=[FileRequired()])

    nombre_portada = StringField(validators=[InputRequired(), Length(
        min=2, max=50)], render_kw={"placeholder": "Nombre de Portada"})

    ubicacion = TextAreaField(validators=[DataRequired(), Length(
        min=5, max=150,message="Al menos 15 caracteres, Maximo 250")], render_kw={"placeholder": "Ubicacion del Libro"} )

    ejemplar = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Numero de ejemplar"})

    isbn = StringField(validators=[InputRequired(), Length(
        min=4, max=13)], render_kw={"placeholder": "Codigo ISBN"})

    submit = SubmitField("Registrar Libro")


class RegisterPersonaForm(FlaskForm):
    nombre = StringField(validators=[InputRequired(), Length(
        min=2, max=50)], render_kw={"placeholder": "Nombre"})
    apellido = StringField(validators=[InputRequired(), Length(
        min=4, max=100)], render_kw={"placeholder": "Apellidos"})
    correo = StringField(validators=[InputRequired(), Length(
        min=4, max=150)], render_kw={"placeholder": "Correo"})
    codigo = StringField(validators=[InputRequired(), Length(
        min=8, max=10)], render_kw={"placeholder": "Codigo"})
    dni = StringField(validators=[InputRequired(), Length(
        min=8, max=10, message="DNI 8 digitos, Carnet de extrangeria 10")], render_kw={"placeholder": "DNI"})
    telefono = StringField(validators=[InputRequired(), Length(
        min=8, max=9)], render_kw={"placeholder": "Telefono"})
    submit = SubmitField("Registrar Persona")

class RegisterPrestamoForm(FlaskForm):
    estado_entregado = TextAreaField(validators=[DataRequired(), Length(
        min=5, max=150,message="Al menos 15 caracteres, Maximo 250")], render_kw={"placeholder": "Observaciones del prestamo"} )
    fecha_devolucion = DateField('Cual es la fecha de devolucion?',format="%Y-%m-%d", validators=[Required()])
    submit = SubmitField("Registrar Prestamo")
