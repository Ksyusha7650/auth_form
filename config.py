from generator import generate_random_string


class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = \
        "postgresql://ksyu7650:04042002Mm!@77.222.36.9:18003/ksyu7650"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "x;4<`]G@?w=t5YrFG$XQbA(NYj;2u6wx~_by:zuYvGn[2dXD(CFU`Y/q[XZ42eLz#$RY4]C%Vky>`L6"
    JWT_REFRESH_SECRET_KEY = "B*v4)>]Gz}jK`y9UZQ*%y7gw9NEc@3HVKQT>3`'MxSmq*B&fH6e-knj9Vh_tz3]mA{n5+8SP}zbp&4<6"
    STATIC_URL = 'static/'
    # INVITATION_CODE = generate_random_string(10)
    INVITATION_CODE = 'ZTbSQykZMR'

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}
