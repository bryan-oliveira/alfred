from itsdangerous import URLSafeTimedSerializer
from app import app, mail
from flask.ext.mail import Message


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


# expiration is in seconds
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    # print "Sending mail."
    msg = Message()
    msg.recipients = [to]
    msg.subject = subject
    msg.sender = ('Alfred', 'alfred@chef-alfred.com')
    msg.html = template
    mail.send(msg)
