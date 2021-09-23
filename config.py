from os.path import  join,dirname,realpath
# upload_folder = '/static/img/product'
# ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
class Config (object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///products.db'
    SQLALCHEMY_TRACK_MADIFICATIONS = False
    UPLOAD_FOLDER = join(dirname(realpath(__file__)),'shop/static/img/product/')