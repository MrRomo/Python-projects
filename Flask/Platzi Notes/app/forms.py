from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class TodoForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField()


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')
    
class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')
    