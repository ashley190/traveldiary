import os


def get_from_env(var_name: str) -> str:
    value = os.environ.get(var_name)

    if not value:
        raise ValueError(f"{var_name} is not set")

    return value


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "secret"
    DEBUG = False

    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_from_env("DB_URI")

    @property
    def AWS_ACCESS_KEY_ID(self):
        return get_from_env("AWS_ACCESS_KEY_ID")
    
    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return get_from_env("AWS_SECRET_ACCESS_KEY")

    @property
    def AWS_S3_BUCKET(self):
        return get_from_env("AWS_S3_BUCKET")

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        return get_from_env("JWT_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:testdb:"


environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
