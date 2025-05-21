import os

from constants import ENV_STRING, DEFAULT_ENV


def env():
    return os.getenv(ENV_STRING, DEFAULT_ENV)


def properties():
    print(f'Environment: {env()}')
    variables = {}
    with open(f'env/{env()}.py') as f:
        exec(f.read(), variables)
    return variables


PROPERTIES = properties()
