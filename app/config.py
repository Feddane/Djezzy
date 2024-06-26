

class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False