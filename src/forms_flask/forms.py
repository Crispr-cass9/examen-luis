from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import Email, EqualTo, ValidationError, Length, DataRequired

def caracter_especial(form, field):
    if ' ' in field.data:
        raise ValidationError(message='La contraseña no puede tener espacios en blanco')

    contador_especiales = 0
    for caracter in field.data:
        if caracter in '$_-*&':
            contador_especiales+=1

    if contador_especiales==0:
        raise ValidationError(message='La contraseña debe contener como mínimo un carácter especial')
    
def custom_validation(form, field):
    if field.data == 'admin':
        raise ValidationError('El Username no puede ser admin')
    
    if not field.data[0].isAlpha():
        raise ValidationError('El Username no puede comenzar por carácteres especiales')

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20), custom_validation])

    email = EmailField('Correo', [Email(), Length(min=10, max=100), DataRequired()])
    contrasenya = PasswordField('Contraseña', validators=[Length(min=6, max=12), DataRequired(), EqualTo('confirmar', message='Las contraseñas deben coincidir')])
    confirmar = PasswordField('Confirmar contraseña', validators=[Length(min=6, max=12), DataRequired()])
    submit = SubmitField('Registrate')

class Login(FlaskForm):

    email = EmailField('Correo', validators=[Email(), Length(min=10, max=100), DataRequired()])
    contrasenya = PasswordField('Contraseña', validators=[Length(min=6, max=12), DataRequired(), caracter_especial])
    submit = SubmitField('Logearte')