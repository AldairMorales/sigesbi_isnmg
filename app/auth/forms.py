from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

from app.models import Usuario


class RegisterForm(FlaskForm):
    tipoUsuario = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Tipo de Usuario"})
    clave = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Clave"})

    submit = SubmitField("Registrar")

    def validar_usuario(self, usuario):
        existe_usuario = Usuario.query.filter_by(usuario=usuario.data).first()
        if existe_usuario:
            raise ValidationError("El usuario acutalmente ya existe. Porfavor elegir un nombre de usaurio diferente.")

class LoginForm(FlaskForm):
    tipo = SelectField("Operador",choices=[("+","Sumar"),("-","Resta")])
    usuario = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Nombre de Usuario"})
    clave = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Clave"})

    submit = SubmitField("Ingresar")