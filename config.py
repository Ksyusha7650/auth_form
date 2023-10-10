
class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://postgres:123456@localhost:5432/authorization'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "abrleva08"
    JWT_REFRESH_SECRET_KEY = "refresh_abrleva08"

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}
