# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, \
    IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email, Optional
from wtforms.fields.html5 import EmailField


class LoginForm(Form):
    username = StringField('', validators=[DataRequired(message="Missing Username.")])
    password = PasswordField('', validators=[DataRequired(message="Missing Password.")])
    remember_me = BooleanField('remember_me', default=False)


class DeleteForm(Form):
    password = PasswordField('Password:',
                             validators=[DataRequired(message="Password required to delete account.")],
                             render_kw={"placeholder": u"●●●●●●●"})
    submit = SubmitField("Delete Account")


class RegisterForm(Form):
    # User's full name
    fullname = StringField('Name:',
                           validators=[DataRequired()],
                           render_kw={"placeholder": "Alfred the Butler"})
    # User's username used to login
    username = StringField('User Name:',
                           validators=[DataRequired(), Length(min=5, max=30)],
                           render_kw={"placeholder": "alfred"})
    # User's password
    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=6, max=30)],
                             render_kw={"placeholder": u"●●●●●●●"})

    # User's email
    email = EmailField('Email address:',
                       validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "alfred@chef-alfred.com"})

    # Password confirmation
    password_conf = PasswordField('Confirm Password:',
                                  validators=[DataRequired(), Length(min=6, max=30)],
                                  render_kw={"placeholder": u"●●●●●●●"})
    # Gender
    gender = SelectField('Gender:', choices=[('M', 'Male'), ('F', 'Female')])

    # Age
    age = IntegerField("Age:",
                       validators=[DataRequired(), NumberRange(0, 130)],
                       render_kw={"placeholder": "63"})

    # User's allergies/preferences/restrictions
    lowchol = BooleanField('Low Cholesterol', default=False)
    highchol = BooleanField('High Cholesterol', default=False)
    overw = BooleanField('Over Weight', default=False)
    underw = BooleanField('Under Weight', default=False)
    gluten = BooleanField('Gluten', default=False)
    nuts = BooleanField('Nuts', default=False)
    fish = BooleanField('Pescatarian', default=False)
    sesame = BooleanField('Sesame', default=False)
    vegetarian = BooleanField('Vegetarian', default=False)
    vegan = BooleanField('Vegan', default=False)

    submit = SubmitField("Submit")


class ProfileForm(Form):

    # User's full name
    fullname = StringField('Name:',
                           validators=[DataRequired()],
                           render_kw={"placeholder": "Alfred the Butler"})

    # User's username used to login
    username = StringField('User Name:',
                           validators=[DataRequired(), Length(min=5, max=30)],
                           render_kw={"placeholder": "alfred"})

    # Old password
    password = PasswordField('Old Password:',
                             validators=[Optional(), Length(min=6, max=30)],
                             render_kw={"placeholder": u"●●●●●●●"})

    # New password
    new_password = PasswordField('New Password:',
                                 validators=[Optional(), Length(min=6, max=30)],
                                 render_kw={"placeholder": u"●●●●●●●"})

    # New password confirmation
    new_password_conf = PasswordField('Confirm New Password:',
                                      validators=[Optional(), Length(min=6, max=30)],
                                      render_kw={"placeholder": u"●●●●●●●"})

    # User's email
    email = EmailField('Email address:',
                       validators=[DataRequired(message="An email address is required."),
                                   Email(message="Please enter a valid email address.")],
                       render_kw={"placeholder": "alfred@chef-alfred.com"})

    # Gender
    gender = SelectField('Gender:', choices=[('M', 'Male'), ('F', 'Female')])

    # Age
    age = IntegerField("Age:",
                       validators=[DataRequired(message="Please enter a valid age."),
                                   NumberRange(0, 130, message=" not in valid range.")],
                       render_kw={"placeholder": "63"})

    # User's allergies/preferences/restrictions
    lowchol = BooleanField('Low Cholesterol', default=False)
    highchol = BooleanField('High Cholesterol', default=False)
    overw = BooleanField('Over Weight', default=False)
    underw = BooleanField('Under Weight', default=False)
    gluten = BooleanField('Gluten', default=False)
    nuts = BooleanField('Nuts', default=False)
    fish = BooleanField('Pescatarian', default=False)
    sesame = BooleanField('Sesame', default=False)
    vegetarian = BooleanField('Vegetarian', default=False)
    vegan = BooleanField('Vegan', default=False)

    submit = SubmitField("Update")

