from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, \
    IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    fullname = StringField('Name:', validators=[DataRequired()], render_kw={"placeholder": "Full Name"})
    username = StringField('User Name:', validators=[DataRequired(), Length(min=5, max=30)], render_kw={"placeholder": "User Name"})
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=30)], render_kw={"placeholder": "Password"})
    gender = SelectField('Gender:', choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField("Age:", validators=[DataRequired(), NumberRange(0, 130)], render_kw={"placeholder": "Age"})

    lowchol = BooleanField('Low Cholesterol', default=False)
    highchol = BooleanField('High Cholesterol', default=False)
    overw = BooleanField('Over Weight', default=False)
    underw = BooleanField('Under Weight', default=False)
    gluten = BooleanField('Gluten', default=False)
    nuts = BooleanField('Nuts', default=False)
    fish = BooleanField('Fish', default=False)
    sesame = BooleanField('Sesame', default=False)
    vegetarian = BooleanField('Vegetarian', default=False)
    vegan = BooleanField('Vegan', default=False)

    submit = SubmitField("Submit")
