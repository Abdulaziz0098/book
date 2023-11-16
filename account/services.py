import dataclasses
import datetime
import jwt
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from book import settings
from .models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
        )


def create_user(user_data):
    if isinstance(user_data, UserDataClass):
        data = dataclasses.asdict(user_data)
    else:
        data = user_data

    User = get_user_model()
    instance = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email')
    )
    if data.get('password') is not None:
        instance.set_password(data.get('password'))

    instance.save()

    verification_token = generate_verification_token(data.get('email'))

    send_verification_email(data.get('email'), verification_token)

    return UserDataClass.from_instance(instance)


def user_email_selector(email: str) -> "User":
    User = get_user_model()
    user = User.objects.filter(email=email).first()

    return user


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        iat=datetime.datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token


def generate_verification_token(email):
    payload = dict(
        email=email,
        exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=630),
        iat=datetime.datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token


def send_verification_email(email, token):
    verification_link = f"{settings.URL}/api/user/verify-email?token={token}"
    print(verification_link)

    # send_mail(
    #     'Verify Your Email',
    #     f'Click the following link to verify your email: {verification_link}',
    #     f'{settings.EMAIL_HOST_USER}',
    #     [email],
    #     fail_silently=False,
    # )
