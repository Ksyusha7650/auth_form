class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = \
        "postgresql://ksyu7650:04042002Mm!@77.222.36.9:18003/ksyu7650"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "abrleva08"
    JWT_REFRESH_SECRET_KEY = "refresh_abrleva08"
    STATIC_URL = 'static/'

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}
