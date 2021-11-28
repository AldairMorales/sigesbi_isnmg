from models import Usuario
from config import db


def get_user_by_username(username):
    """ Método para retornar el usuario a partir del username. """
    return Usuario.query.filter_by(nombre_usuario=username).first()

def register_user(usuario_data):
    """ Método para registrar un usuario nuevo en la base de datos. """
    usuario = Usuario(
        nombre=usuario_data['nombre'],
        clave=usuario_data['clave'],
        tipo=usuario_data['tipo'],
    )

    usuario.set_clave(usuario_data['clave'])

    db.session.add(usuario)
    db.session.commit()