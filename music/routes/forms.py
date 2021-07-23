from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

from ..db.authentication import check_email_unique, check_password

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Post')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        else:

            if not check_email_unique(self.email.data):
                self.email.errors.append('The email already exists')
                return False

            return True

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        else:

            if check_password(self.email.data, self.password.data):
                return True

            self.password.errors.append('email or password is invalid')
            return False