class Config():
    SECRET_KEY = '30b01a61a413b1346cb188b4ee2097521872555633ba6ac59fe33dfdafe064c9'
    EMAIL_KEY = 'oeas jwyo fdhw lvui'

class Development(Config):
    DEBUG=True

class Production(Config):
    DEBUG=False

configuracion = {
    'dev' : Development,
    'prod' : Production
}