from .base import * #noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="-kQO9yGUK9x0yB4ncai-17oExb8GaZdeyQ-lyW1UcCZYewJc6fM",
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


