import flask
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, RadioField, BooleanField, HiddenField
from wtforms.validators import Length, Email, ValidationError, DataRequired


custom_agreement = flask.Markup('Съгласен съм с <a class="policy" target="_blank" href="termsofservice">Общите условия</a> и <a class="policy" target="_blank" href="privacypolicy">Политиката за поверителност</a>')

class ContactForm(FlaskForm):
    name = StringField('Име', validators=[Length(min=2, max=40, message='Полето трябва да съдържа между 2 и 40 символа.')])
    email = StringField('Email', validators=[Email(message='Невалиден Емайл адрес.')])
    phonenumber = StringField('Телефон')
    message = TextAreaField('Съобщение', validators=[Length(min=1)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Изпрати')


    def validate_phonenumber(form, field):
        try:
            correct = int(field.data)
            mybool = isinstance(correct, int)
            if mybool == False:
                raise ValidationError('Невалиден телефон.')
        except:
            raise ValidationError('Невалиден телефон.')


class CheckoutForm(FlaskForm):
    fname = StringField('Име*', validators=[Length(min=2, max=40, message='Полето трябва да съдържа между 2 и 40 символа.')])
    lname = StringField('Фамилия*', validators=[Length(min=2, max=40, message='Полето трябва да съдържа между 2 и 40 символа.')])
    checkoutemail = StringField('Email*', validators=[Email(message='Невалиден Емайл адрес.')])
    phone = StringField('Телефон*')
    checkoutmessage = TextAreaField('Съобщение')
    shippingmethod = RadioField('Доставяне до:', choices=[(1,'Офис на Спиди'),(2,'Офис на Еконт'),(3,'Адрес')], default=1, coerce=int)
    province = StringField('Община*', validators=[Length(min=2, max=40, message='Невалидна община.')])
    city = StringField('Град/Село*', validators=[Length(min=2, max=40, message='Невалиден град/село.')])
    agreement = BooleanField(custom_agreement)
    adress = StringField('Адрес на офис*', validators=[Length(min=2, message='Невалиден адрес.')])

    def validate_phone(form, field):
        try:
            correct = int(field.data)
            mybool = isinstance(correct, int)
            if mybool == False:
                raise ValidationError('Невалиден телефон.')
        except:
            raise ValidationError('Невалиден телефон.')

    def validate_agreement(form, field):
        try:
            validbool = field.data
            if validbool == False:
                raise ValidationError('Това поле е задължително.')
        except:
            raise ValidationError('Това поле е задължително.')


